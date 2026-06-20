from enum import Enum
from schemas import (
    Request,
    Response,
    Spreadsheet,
    DataFilter,
    DeveloperMetadata,
    ValueInputOption,
    ValueRenderOption,
    DateTimeRenderOption,
    UpdateValuesResponse
)
from typing import List, TypedDict
from pydantic import BaseModel, Field


class ToolError(TypedDict):
    error: str

class BatchUpdateSpreadsheetRequest(BaseModel):
    requests: List[Request] = Field(
        ...,
        description="A list of updates to apply to the spreadsheet. Requests will be applied in the order they are specified. If any request is not valid, no requests will be applied.",
    )
    includeSpreadsheetInResponse: bool = Field(
        ...,
        description="Determines if the update response should include the spreadsheet resource.",
    )
    responseRanges: List[str] = Field(
        ...,
        description="Limits the ranges included in the response spreadsheet. Meaningful only if includeSpreadsheetInResponse is 'true'.",
    )
    responseIncludeGridData: bool = Field(
        ...,
        description="True if grid data should be returned. Meaningful only if includeSpreadsheetInResponse is 'true'. This parameter is ignored if a field mask was set in the request.",
    )


class CreateSpreadSheetResponse(BaseModel):
    spreadsheetId: str = Field(
        ..., description="The spreadsheet the updates were applied to."
    )
    replies: List[Response] = Field(
        ...,
        description="The reply of the updates. This maps 1:1 with the updates, although replies to some requests may be empty.",
    )
    updatedSpreadsheet: Spreadsheet = Field(
        ...,
        description="The spreadsheet after updates were applied. This is only set if BatchUpdateSpreadsheetRequest.include_spreadsheet_in_response is true",
    )

class GetSpreadsheetQueryParams(BaseModel):
    ranges: List[str] = Field(..., description="The ranges to retrieve from the spreadsheet.")
    includeGridData: bool = Field(..., description="True if grid data should be returned. This parameter is ignored if a field mask was set in the request.")
    excludeTablesInBandedRanges: bool = Field(..., description="True if tables should be excluded in the banded ranges. False if not set.")

class GetByDataFilterRequestBody(BaseModel):
    dataFilters: List[DataFilter] = Field(..., description="The DataFilters used to select which ranges to retrieve from the spreadsheet.")
    includeGridData: bool = Field(..., description="True if grid data should be returned. This parameter is ignored if a field mask was set in the request.")
    excludeTablesInBandedRanges: bool = Field(..., description="True if tables should be excluded in the banded ranges. False if not set.")

class SearchDeveloperMetadataRequestBody(BaseModel):
    dataFilters: List[DataFilter] = Field(..., description="The data filters describing the criteria used to determine which DeveloperMetadata entries to return. DeveloperMetadata matching any of the specified filters are included in the response.")

class MatchedDeveloperMetadata(BaseModel):
    developerMetadata: DeveloperMetadata = Field(..., description="The developer metadata matching the specified filters.")
    dataFilters: List[DataFilter] = Field(..., description="All filters matching the returned developer metadata.")

class SearchDeveloperMetadataResponse(BaseModel):
    matchedDeveloperMetadata: List[MatchedDeveloperMetadata] = Field(..., description="The metadata matching the criteria of the search request.")

class CopyToRequestBody(BaseModel):
    destinationSpreadsheetId: str = Field(..., description="The ID of the spreadsheet to copy the sheet to.")

class InsertDataOption(Enum):
    OVERWRITE = "OVERWRITE"
    INSERT_ROWS = "INSERT_ROWS"
class AppendValuesQueryParams(BaseModel):
    valueInputOption: ValueInputOption = Field(..., description="How the input data should be interpreted.")
    insertDataOption: InsertDataOption = Field(..., description="How the input data should be inserted.")
    includeValuesInResponse: bool = Field(..., description="Determines if the update response should include the values of the cells that were appended. By default, responses do not include the updated values.")
    responseValueRenderOption: ValueRenderOption = Field(..., description="Determines how values in the response should be rendered. The default render option is FORMATTED_VALUE.")
    responseDateTimeRenderOption: DateTimeRenderOption = Field(..., description="Determines how dates, times, and durations in the response should be rendered. This is ignored if responseValueRenderOption is FORMATTED_VALUE. The default dateTime render option is SERIAL_NUMBER.")

class AppendValuesResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The spreadsheet the updates were applied to.")
    tableRange: str = Field(..., description="The range (in A1 notation) of the table that values are being appended to (before the values were appended). Empty if no table was found.")
    updates: UpdateValuesResponse = Field(..., description="Information about the updates that were applied.")

class BatchClearValuesRequestBody(BaseModel):
    ranges: List[str] = Field(..., description="The ranges to clear, in A1 notation or R1C1 notation.")

class BatchClearValuesResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The spreadsheet the updates were applied to.")
    clearedRanges: List[str] = Field(..., description="The ranges that were cleared, in A1 notation. If the requests are for an unbounded range or a range larger than the bounds of the sheet, this is the actual ranges that were cleared, bounded to the sheet's limits.")

class BatchClearByDataFilterRequestBody(BaseModel):
    dataFilters: List[DataFilter] = Field(..., description="The DataFilters used to determine which ranges to clear.")

class BatchClearByDataFilterResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The spreadsheet the updates were applied to.")
    clearedRanges: List[str] = Field(..., description="The ranges that were cleared, in A1 notation. If the requests are for an unbounded range or a range larger than the bounds of the sheet, this is the actual ranges that were cleared, bounded to the sheet's limits.")
