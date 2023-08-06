from __future__ import annotations

from vectice.models.resource.metadata.base import (
    DatasetSourceType,
    DatasetSourceUsage,
    Metadata,
)
from vectice.models.resource.metadata.column_metadata import DBColumn


class DBMetadata(Metadata):
    """Class that describes metadata of dataset that comes from a database."""

    def __init__(
        self,
        dbs: list[MetadataDB],
        size: int,
        usage: DatasetSourceUsage | None = None,
        origin: str | None = None,
    ):
        """Initialize a DBMetadata instance.

        Parameters:
            dbs: The list of databases.
            size: The size of the metadata.
            usage: The usage of the metadata.
            origin: The origin of the metadata.
        """
        super().__init__(size=size, type=DatasetSourceType.DB, usage=usage, origin=origin)
        self.dbs = dbs

    def asdict(self) -> dict:
        return {
            "dbs": [db.asdict() for db in self.dbs],
            "size": self.size,
            "filesCount": None,
            "files": [],
            "type": self.type.value,
            "usage": self.usage.value if self.usage else None,
            "origin": self.origin,
        }


class MetadataDB:
    def __init__(self, name: str, columns: list[DBColumn], rows_number: int, size: int | None = None):
        """Initialize a MetadataDB instance.

        Parameters:
            name: The name of the table.
            columns: The columns that compose the table.
            rows_number: The number of row of the table.
            size: The size of the table.
        """
        self.name = name
        self.size = size
        self.rows_number = rows_number
        self.columns = columns

    def asdict(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "rowsNumber": self.rows_number,
            "columns": [column.asdict() for column in self.columns],
        }
