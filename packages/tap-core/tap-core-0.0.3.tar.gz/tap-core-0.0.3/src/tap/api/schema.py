from pathlib import Path
from typing import Any, Dict, Optional
import json
from singer import resolve_schema_references


def load_schema(tap_stream_id: str, schemas_dir: Optional[Path] = None) -> Dict:

    schema: Dict[str, Any] = json.loads((schemas_dir or Path(__file__).with_name('schemas')).joinpath(tap_stream_id + '.json').read_text(encoding='utf-8'))

    return resolve_schema_references(schema, {
        stream_id: load_schema(stream_id)
        for stream_id in schema.pop('tap_schema_dependencies', [])})
