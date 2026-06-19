from enum import Enum
from pydantic import BaseModel, Field

from .api_types import (
    DimensionRange
)

class DeveloperMetadataLocationType(Enum):
    DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED = "DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED"
    ROW = "ROW"
    COLUMN = "COLUMN"
    SHEET = "SHEET"
    SPREADSHEET = "SPREADSHEET"

class DeveloperMetadataLocation(BaseModel):
    locationType: DeveloperMetadataLocationType = Field(..., description="The type of location this object represents. This field is read-only.")
    spreadsheet: bool = Field(..., description="True when metadata is associated with an entire spreadsheet.")
    sheetId: int = Field(..., description="The ID of the sheet when metadata is associated with an entire sheet.")
    dimensionRange: DimensionRange = Field(..., description="Represents the row or column when metadata is associated with a dimension. The specified DimensionRange must represent a single row or column. It cannot be unbounded or span multiple rows or columns.")



class DeveloperMetadataVisibility(Enum):
    DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED = "DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED"
    DOCUMENT = "DOCUMENT"
    PROJECT = "PROJECT"


class DeveloperMetadata(BaseModel):
    metadataId: int = Field(..., description="The spreadsheet-scoped unique ID that identifies the metadata. IDs may be specified when metadata is created, otherwise one will be randomly generated and assigned. Must be positive.")
    metadataKey: str = Field(..., description="The metadata key. There may be multiple metadata in a spreadsheet with the same key. Developer metadata must always have a key specified.")
    metadataValue: str = Field(..., description="Data associated with the metadata's key.")
    location: DeveloperMetadataLocation = Field(..., description="The location where the metadata is associated.")
    visibility: DeveloperMetadataVisibility = Field(..., description="The metadata visibility. Developer metadata must always have visibility specified.")
