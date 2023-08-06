from typing import Any, Dict, List


def format_response(response: List, params: Dict = {}) -> Any:
    return [r for r in response]


def format_response_replication(response: List, params: Dict, replication_value: int = 0) -> Any:
    # LOGGER.info({'params': params, 'replication_value': replication_value, 'response': response})
    # return [r for i in ((response,) if isinstance(response, dict) else response)
    return [r for i in response
            for r in i.get(params.get('path'), {}).values()]


def format_response_sub_stream(response: List, params: Dict, replication_value: int = 0, parent_record: Dict = {}) -> List:
    # LOGGER.info({'params': params, 'replication_value': replication_value, 'response': response})
    # TODO: filter out unbounded preceding
    return [r for i in response
            for r in i.get(params.get('path'), i)]
