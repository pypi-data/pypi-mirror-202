import datetime
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional
from functools import partial, reduce
from asyncio import shield, to_thread, gather  # , Condition

from singer import (
    Transformer,
    CatalogEntry,
    Schema,
    get_bookmark,
    write_bookmark,
    get_offset,
    set_offset,
    clear_offset,
    set_currently_syncing,
    record_counter,
    reset_stream,
    write_schema,
    write_version,
    RecordMessage,
    write_message,
    write_state,
    get_logger)
from singer.metadata import get_standard_metadata, to_map, write, to_list

# from .client import Client
from .sync import Extractor, job_stream_timer
from .schema import load_schema
from .transform import format_response

LOGGER = get_logger()


class AbstractStream:

    # _client: Optional[Client] = None
    # _condition: Optional[Condition] = None
    # _currently_syncing: Optional[set] = None

    def __init__(
        self,
        tap_stream_id: str,
        config: Dict = {},
        schemas_dir: Optional[Path] = None,
        key_properties: List[str] = [],
        replication_method: str = 'FULL_TABLE',
        replication_key: Optional[str] = None,
        is_view: bool = False,
        database: Optional[str] = None,
        table: Optional[str] = None,
        row_count: Optional[int] = None,
        stream: Optional[str] = None,
        stream_alias: Optional[str] = None,
        format_response_function: Callable = format_response,
        format_response_params: Dict[str, Any] = {},
        parent: Dict[str, Any] = {},
        # children: List = [],
        params: Dict[str, Any] = {}
    ) -> None:
        self.format_response_function: Callable = format_response_function
        self.format_response_params: Dict[str, Any] = format_response_params
        # self.format_response_params: Dict[str, Any] = (
        #     {'replication_key': replication_key} if replication_method == 'INCREMENTAL' else {}) | format_response_params
        self.parent: Dict[str, Any] = parent
        # self.children: List = children
        self.params: Dict[str, Any] = params
        self.start_date: Optional[datetime.datetime] = datetime.datetime.strptime(config['start_date'], '%Y-%m-%dT%H:%M:%SZ') \
            if 'start_date' in config else None
        self.user_agent: Optional[str] = config.get('user_agent')

        schemas_dir = schemas_dir or Path(__file__).resolve().with_name('schemas')
        self.schema: Dict[str, Any] = load_schema(tap_stream_id, schemas_dir) if schemas_dir.joinpath(tap_stream_id + '.json').exists() \
            else load_schema(stream or tap_stream_id, schemas_dir) if schemas_dir.joinpath(str(stream) + '.json').exists() \
            else load_schema(stream_alias or tap_stream_id, schemas_dir)

        metadata: List[Any] = get_standard_metadata(
            schema=self.schema,
            schema_name=tap_stream_id,
            key_properties=key_properties,
            valid_replication_keys=replication_key,
            replication_method=replication_method)

        self.catalog_entry: CatalogEntry = CatalogEntry(
            tap_stream_id=tap_stream_id,
            stream=stream or tap_stream_id,
            stream_alias=stream_alias or stream or tap_stream_id,
            key_properties=key_properties or [],
            schema=Schema.from_dict(self.schema),
            replication_key=replication_key,
            replication_method=replication_method,
            is_view=is_view,
            database=database,
            table=table,
            row_count=row_count,
            metadata=to_list(write(to_map(metadata), (), 'selected', True))
            if tap_stream_id in config.get('selected', []) else metadata)

    def __copy__(self) -> Any:
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo: Any) -> Any:
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    @job_stream_timer
    async def get_stream(self, extractor: Extractor, *args: Optional[Any], **kwargs: Dict) -> None:
        raise NotImplementedError("Child classes of AbstractStream require `get_stream` implementation")

    async def write_schema(self, extractor: Extractor) -> None:

        extractor._currently_syncing.add(self.catalog_entry.tap_stream_id)

        await to_thread(write_schema,
                        self.catalog_entry.tap_stream_id,
                        self.catalog_entry.schema.to_dict(),
                        self.catalog_entry.key_properties,
                        bookmark_properties=self.catalog_entry.replication_key,
                        stream_alias=self.catalog_entry.stream_alias)

        # NOTE: ACTIVATE_VERSION Singer extension support https://github.com/meltano/meltano/issues/2463
        current_timestamp: int = int(datetime.datetime.now().astimezone(datetime.timezone.utc).timestamp() * 1000)
        self.version: int = get_bookmark(extractor.state, self.catalog_entry.tap_stream_id, 'version', current_timestamp) \
            if self.catalog_entry.replication_key \
            else current_timestamp

        is_stream_bookmarked: bool = extractor.state.get('bookmarks', {}).get(self.catalog_entry.tap_stream_id) is not None
        if self.catalog_entry.replication_key or not is_stream_bookmarked:
            write_bookmark(extractor.state, self.catalog_entry.tap_stream_id, 'version', self.version)

        if self.catalog_entry.replication_method == 'FULL_TABLE':
            await to_thread(write_version, self.catalog_entry.stream, self.version)

    async def write_records(self, extractor: Extractor, records: Iterable[Any]) -> None:
        LOGGER.info('Syncing stream: %s', self.catalog_entry.tap_stream_id)

        set_currently_syncing(extractor.state, self.catalog_entry.tap_stream_id)
        await to_thread(write_state, extractor.state)

        if self.catalog_entry.tap_stream_id not in extractor._currently_syncing:
            await self.write_schema(extractor)

        with Transformer() as t, record_counter(self.catalog_entry.tap_stream_id) as counter:
            for record in records:
                await to_thread(write_message,
                                RecordMessage(
                                    stream=(self.catalog_entry.stream_alias or self.catalog_entry.tap_stream_id),
                                    record=t.transform(record, self.catalog_entry.schema.to_dict(), to_map(self.catalog_entry.metadata)),
                                    time_extracted=datetime.datetime.now().astimezone(datetime.timezone.utc),
                                    version=self.version))
                counter.increment(1)


class SubStream(AbstractStream):

    @job_stream_timer
    async def get_stream(self, extractor: Extractor, parent_records: list) -> None:
        replication_key: str = self.catalog_entry.replication_key
        replication_value = get_bookmark(extractor.state, self.catalog_entry.tap_stream_id, replication_key, 0)
        parent_key_properties: List[str] = self.parent.get('key_properties', [])
        endpoint: str = self.params.get('endpoint', '')

        records_raw: list = [record for records in await gather(*[
            shield(extractor._client.get_records(
                self.catalog_entry.tap_stream_id,
                **(self.params | {
                    'endpoint': endpoint.format(**{k: parent_record.get(k) for k in parent_key_properties}),
                    'format_response': ({
                        'params': self.format_response_params,
                        'function': partial(
                            self.format_response_function,
                            params=self.format_response_params,
                            replication_value=replication_value,
                            parent_record=parent_record)})['function']})))
            for parent_record in parent_records
            if reduce(lambda x, k: x and parent_record.get(k) is not None, parent_key_properties, True)])
            if records is not None
            for record in records]

        records = (r for r in records_raw if int(r.get(replication_key, 2e9)) > replication_value) \
            if self.catalog_entry.replication_method == 'INCREMENTAL' \
            else records_raw

        async with extractor._condition:
            await self.write_records(extractor, records)
            # if extractor.catalog.get_stream(self.tap_stream_id).replication_method == 'FULL_TABLE':
            reset_stream(extractor.state, self.catalog_entry.tap_stream_id)
            await to_thread(write_state, extractor.state)


class Stream(AbstractStream):

    @job_stream_timer
    async def get_stream(self, extractor: Extractor, *args: Optional[Any], **kwargs: Dict) -> None:
        params: Dict[str, Any] = deepcopy(self.params)
        replication_key: str = self.catalog_entry.replication_key
        replication_value = get_bookmark(extractor.state, self.catalog_entry.tap_stream_id, replication_key, 0)
        filters: Dict[str, Any] = params.pop('params', {}) | ({
            replication_key: replication_value} if replication_key else {})
        format_response_params: Dict[str, Any] = {
            'params': self.format_response_params,
            'function': partial(
                self.format_response_function,
                params=self.format_response_params,
                replication_value=replication_value)
        } | params.pop('format_response', {})

        records_raw: list = await extractor._client.get_records(
            self.catalog_entry.tap_stream_id, params=filters, format_response=format_response_params['function'], *args, **params)
        records = [r for r in records_raw if r.get(replication_key, 2e9) > replication_value] \
            if self.catalog_entry.replication_method == 'INCREMENTAL' \
            else records_raw

        async with extractor._condition:
            await self.write_records(extractor, records)

            if replication_key is not None and any(records):
                write_bookmark(
                    extractor.state, self.catalog_entry.tap_stream_id, replication_key,
                    max(records, key=lambda r: r.get(replication_key)).get(replication_key))
            if self.catalog_entry.replication_method == 'FULL_TABLE':
                reset_stream(extractor.state, self.catalog_entry.tap_stream_id)

                await to_thread(write_version, self.catalog_entry.stream, self.version)

            await to_thread(write_state, extractor.state)

        for sub_stream_tap_stream_id, _ in filter(
            lambda s: s[1].parent.get('tap_stream_id') == self.catalog_entry.tap_stream_id,
                extractor.streams.items()):
            await extractor.streams[sub_stream_tap_stream_id].get_stream(extractor, records)


class StreamPages(AbstractStream):

    @job_stream_timer
    async def get_stream(self, extractor: Extractor, *args: Optional[Any], **kwargs: Dict) -> None:
        params: Dict[str, Any] = deepcopy(self.params)
        replication_key: str = self.catalog_entry.replication_key
        replication_value = get_bookmark(extractor.state, self.catalog_entry.tap_stream_id, replication_key, 0)
        # replication_value = get_bookmark(extractor.state, self.catalog_entry.tap_stream_id, replication_key, int(self.start_date.timestamp()))
        # LOGGER.info({'format_response_params': self.format_response_params, 'replication_value': replication_value})
        format_response: Dict[str, Any] = {
            'params': self.format_response_params,
            'function': partial(
                self.format_response_function,
                params=self.format_response_params,
                replication_value=replication_value)
        } | params.pop('format_response', {})
        offset_key = self.params.get('offset_key')
        limit_key = self.params.get('limit_key')
        curr_offset = get_offset(extractor.state, self.catalog_entry.tap_stream_id, {}).get('offset', 0)
        filters = {offset_key: curr_offset} | params.pop('params', {}) | ({
            replication_key: replication_value} if replication_key else {})

        while any(filters):
            response = await extractor._client.get(self.catalog_entry.tap_stream_id, params=filters, *args, **params),
            records_raw = format_response['function'](response) if callable(format_response['function']) else []
            records = [r for r in records_raw if r.get(replication_key, 2e9) > replication_value] \
                if self.catalog_entry.replication_method == 'INCREMENTAL' \
                else records_raw

            async with extractor._condition:
                set_offset(extractor.state, self.catalog_entry.tap_stream_id, 'offset', filters[offset_key])
                await self.write_records(extractor, records)
                if replication_key and records:
                    write_bookmark(
                        extractor.state,
                        self.catalog_entry.tap_stream_id,
                        replication_key,
                        max(records + [filters],
                            key=lambda r: r.get(replication_key)).get(replication_key))
                await to_thread(write_state, extractor.state)

            for sub_stream_tap_stream_id, _ in filter(
                lambda s: s[1].parent.get('tap_stream_id') == self.catalog_entry.tap_stream_id,
                    extractor.streams.items()):
                await extractor.streams[sub_stream_tap_stream_id].get_stream(extractor, records)

            # if any(records) and len(records) >= filters[limit_key]:
            if len(records_raw) > 0:
                filters[offset_key] += filters[limit_key]
            else:
                filters = {}

        if self.catalog_entry.replication_method == 'FULL_TABLE':
            await to_thread(write_version, self.catalog_entry.stream, self.version)

        # if extractor.catalog.get_stream(self.tap_stream_id).replication_method == 'FULL_TABLE':
        async with extractor._condition:
            clear_offset(extractor.state, self.catalog_entry.tap_stream_id)

    # async def get_cursors(self, curr_offset: int = 0, *args: Optional[Any], **kwargs: Dict) -> AsyncGenerator:
    #     format_response = kwargs['format_response']
    #     limit_key = kwargs['limit_key'] if 'limit_key' in kwargs else None
    #     next_token_key = kwargs['next_token_key'] if 'next_token_key' in kwargs else None
    #     params: Dict = {limit_key: self.page_limit} | kwargs.pop('params', {})
    #     filters: Dict = params

    #     while any(filters):
    #         response = await self.get(tap_stream_id, params=filters, *args, **kwargs),
    #         records = format_response['function'](response, format_response['params']) if callable(format_response['function']) else []

    #         yield curr_offset, records

    #         if len(records) > 0 and response.get(next_token_key, None) is not None:  # type: ignore
    #             filters = params | {next_token_key: response[next_token_key]}  # type: ignore
    #             curr_offset += filters[limit_key]
    #         else:
    #             filters = {}
