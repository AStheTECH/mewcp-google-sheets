from enum import Enum

from .developer_metadata import (
    DeveloperMetadataLocation,
    DeveloperMetadataLocationType,
    DeveloperMetadataVisibility,
)
from .other import GridRange
from pydantic import BaseModel, Field
from .values import ValueRange


class DateTimeRenderOption(Enum):
    SERIAL_NUMBER = "SERIAL_NUMBER"
    FORMATTED_STRING = "FORMATTED_STRING"


class DeveloperMetadataLocationMatchingStrategy(Enum):
    DEVELOPER_METADATA_LOCATION_MATCHING_STRATEGY_UNSPECIFIED = (
        "DEVELOPER_METADATA_LOCATION_MATCHING_STRATEGY_UNSPECIFIED"
    )
    EXACT_LOCATION = "EXACT_LOCATION"
    INTERSECTING_LOCATION = "INTERSECTING_LOCATION"


class Dimension(Enum):
    DIMENSION_UNSPECIFIED = "DIMENSION_UNSPECIFIED"
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"


class ErrorCode(Enum):
    ERROR_CODE_UNSPECIFIED = "ERROR_CODE_UNSPECIFIED"
    DOCUMENT_TOO_LARGE_TO_EDIT = "DOCUMENT_TOO_LARGE_TO_EDIT"
    DOCUMENT_TOO_LARGE_TO_LOAD = "DOCUMENT_TOO_LARGE_TO_LOAD"


class UpdateValuesResponse(BaseModel):
    spreadsheetId: str = Field(
        ..., description="The spreadsheet the updates were applied to."
    )
    updatedRange: str = Field(
        ..., description="The range (in A1 notation) that updates were applied to."
    )
    updatedRows: int = Field(
        ...,
        description="The number of rows where at least one cell in the row was updated.",
    )
    updatedColumns: int = Field(
        ...,
        description="The number of columns where at least one cell in the column was updated.",
    )
    updatedCells: int = Field(..., description="The number of cells updated.")
    updatedData: ValueRange = Field(
        ...,
        description="The values of the cells after updates were applied. This is only included if the request's includeValuesInResponse field was true.",
    )


class ErrorDetails(BaseModel):
    errorCode: ErrorCode = Field(
        ..., description="Specific error code indicating what went wrong."
    )


class DimensionRange(BaseModel):
    sheetId: int = Field(..., description="The sheet this span is on.")
    dimension: Dimension = Field(..., description="The dimension of the span.")
    startIndex: int = Field(
        ..., description="The start (inclusive) of the span, or not set if unbounded."
    )
    endIndex: int = Field(
        ..., description="The end (exclusive) of the span, or not set if unbounded."
    )


class DeveloperMetadataLookup(BaseModel):
    locationType: DeveloperMetadataLocationType = Field(
        ...,
        description="Limits the selected developer metadata to those entries which are associated with locations of the specified type. For example, when this field is specified as ROW this lookup only considers developer metadata associated on rows. If the field is left unspecified, all location types are considered. This field cannot be specified as SPREADSHEET when the locationMatchingStrategy is specified as INTERSECTING or when the metadataLocation is specified as a non-spreadsheet location. Spreadsheet metadata cannot intersect any other developer metadata location. This field also must be left unspecified when the locationMatchingStrategy is specified as EXACT.",
    )
    metadataLocation: DeveloperMetadataLocation = Field(
        ...,
        description="Limits the selected developer metadata to those entries associated with the specified location. This field either matches exact locations or all intersecting locations according the specified locationMatchingStrategy.",
    )
    locationMatchingStrategy: DeveloperMetadataLocationMatchingStrategy = Field(
        ...,
        description="Determines how this lookup matches the location. If this field is specified as EXACT, only developer metadata associated on the exact location specified is matched. If this field is specified to INTERSECTING, developer metadata associated on intersecting locations is also matched. If left unspecified, this field assumes a default value of INTERSECTING. If this field is specified, a metadataLocation must also be specified.",
    )
    metadataId: int = Field(
        ...,
        description="Limits the selected developer metadata to that which has a matching DeveloperMetadata.metadata_id.",
    )
    metadataKey: str = Field(
        ...,
        description="Limits the selected developer metadata to that which has a matching DeveloperMetadata.metadata_key.",
    )
    metadataValue: str = Field(
        ...,
        description="Limits the selected developer metadata to that which has a matching DeveloperMetadata.metadata_value.",
    )
    visibility: DeveloperMetadataVisibility = Field(
        ...,
        description="Limits the selected developer metadata to that which has a matching DeveloperMetadata.visibility. If left unspecified, all developer metadata visible to the requesting project is considered.",
    )


class DataFilter(BaseModel):
    developerMetadataLookup: DeveloperMetadataLookup = Field(
        ...,
        description="Selects data associated with the developer metadata matching the criteria described by this DeveloperMetadataLookup.",
    )
    a1Range: str = Field(
        ..., description="Selects data that matches the specified A1 range."
    )
    gridRange: GridRange = Field(
        ...,
        description="Selects data that matches the range described by the GridRange.",
    )

class ValueInputOption(Enum):
    INPUT_VALUE_OPTION_UNSPECIFIED = "INPUT_VALUE_OPTION_UNSPECIFIED"
    RAW = "RAW"
    USER_ENTERED = "USER_ENTERED"

class ValueRenderOption(Enum):
    FORMATTED_VALUE = "FORMATTED_VALUE"
    UNFORMATTED_VALUE = "UNFORMATTED_VALUE"
    FORMULA = "FORMULA"
