from pathlib import Path
from typing import Callable, Set, Optional
from asyncio import run

from .sync import set_streams, sync, CONFIG_KEYS_REQUIRED


def main(schemas_dir: Optional[Path] = None, set_streams: Callable = set_streams, config_keys_required: Set[str] = CONFIG_KEYS_REQUIRED) -> None:
    run(sync(schemas_dir, set_streams, config_keys_required))


# def cli(*,
#         config: str = 'config.json',
#         discover: str = None,
#         catalog: str = 'catalog.json',
#         state: str = 'state.json'
#         schemas_dir: str = None
#     ) -> Extractor:

#     LOGGER.setLevel(LEVELS_MAPPING.get(log_level))
#     with open(config) as config_io, open(catalog) as catalog_io, open(state) as state_io:
#         config_json = json.load(config_io)
#         catalog_json = json.load(catalog_io)
#         state_json = json.load(state_io)

#     streams: Dict = set_streams(config_json)

#     return Extractor(
#         config=config_json,
#         streams=streams,
#         state=state_json,
#         catalog=catalog_json,
#         schemas_dir=schemas_dir
#     )
