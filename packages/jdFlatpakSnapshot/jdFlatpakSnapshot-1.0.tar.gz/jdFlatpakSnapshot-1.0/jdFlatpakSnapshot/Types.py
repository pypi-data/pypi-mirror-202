from typing import Optional, TypedDict


class SnapshotDictEntry(TypedDict):
    name: str
    filename: str
    timestamp: int
    commit: Optional[str]


class ExportedFileManifest(TypedDict):
    version: int
    app_version: str
    type: str
    app_id: str
