from typing import Iterable
from singer import Catalog


def discover(streams: Iterable) -> Catalog:
    catalog: Catalog = Catalog([])

    for stream in streams:
        catalog.streams.append(stream.catalog_entry)

    return catalog
