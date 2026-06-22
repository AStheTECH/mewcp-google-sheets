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
    UpdateValuesResponse,
    ValueRange,
    Dimension,
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


class BatchGetValuesQueryParams(BaseModel):
    ranges: List[str] = Field(..., description="The A1 notation or R1C1 notation of the range to retrieve values from.")
    majorDimension: Dimension = Field(..., description="The major dimension that results should use.")
    valueRenderOption: ValueRenderOption = Field(..., description="How values should be represented in the output. The default render option is ValueRenderOption.FORMATTED_VALUE.")
    dateTimeRenderOption: DateTimeRenderOption = Field(..., description="How dates, times, and durations should be represented in the output. This is ignored if valueRenderOption is FORMATTED_VALUE. The default dateTime render option is SERIAL_NUMBER.")

class BatchGetValuesResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The ID of the spreadsheet the data was retrieved from.")
    valueRanges: List[ValueRange] = Field(..., description="The requested values. The order of the ValueRanges is the same as the order of the requested ranges.")

class BatchGetByDataFilterRequestBody(BaseModel):
    dataFilters: List[DataFilter] = Field(..., description="The data filters used to match the ranges of values to retrieve. Ranges that match any of the specified data filters are included in the response.")
    majorDimension: Dimension = Field(..., description="The major dimension that results should use.")
    valueRenderOption: ValueRenderOption = Field(..., description="How values should be represented in the output. The default render option is FORMATTED_VALUE.")
    dateTimeRenderOption: DateTimeRenderOption = Field(..., description="How dates, times, and durations should be represented in the output. This is ignored if valueRenderOption is FORMATTED_VALUE. The default dateTime render option is SERIAL_NUMBER.")

class MatchedValueRange(BaseModel):
    valueRange: ValueRange = Field(..., description="The values matched by the DataFilter.")
    dataFilters: List[DataFilter] = Field(..., description="The DataFilters from the request that matched the range of values.")

class BatchGetByDataFilterResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The ID of the spreadsheet the data was retrieved from.")
    valueRanges: List[MatchedValueRange] = Field(..., description="The requested values with the list of data filters that matched them.")

class BatchUpdateValuesRequestBody(BaseModel):
    valueInputOption: ValueInputOption = Field(..., description="How the input data should be interpreted.")
    data: List[ValueRange] = Field(..., description="The new values to apply to the spreadsheet.")
    includeValuesInResponse: bool = Field(..., description="Determines if the update response should include the values of the cells that were updated. By default, responses do not include the updated values. The updatedData field within each of the BatchUpdateValuesResponse.responses contains the updated values. If the range to write was larger than the range actually written, the response includes all values in the requested range (excluding trailing empty rows and columns).")
    responseValueRenderOption: ValueRenderOption = Field(..., description="Determines how values in the response should be rendered. The default render option is FORMATTED_VALUE.")
    responseDateTimeRenderOption: DateTimeRenderOption = Field(..., description="Determines how dates, times, and durations in the response should be rendered. This is ignored if responseValueRenderOption is FORMATTED_VALUE. The default dateTime render option is SERIAL_NUMBER.")

class BatchUpdateValuesResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The spreadsheet the updates were applied to.")
    totalUpdatedRows: int = Field(..., description="The total number of rows where at least one cell in the row was updated.")
    totalUpdatedColumns: int = Field(..., description="The total number of columns where at least one cell in the column was updated.")
    totalUpdatedCells: int = Field(..., description="The total number of cells updated.")
    totalUpdatedSheets: int = Field(..., description="The total number of sheets where at least one cell in the sheet was updated.")
    responses: List[UpdateValuesResponse] = Field(..., description="One UpdateValuesResponse per requested range, in the same order as the requests appeared.")

class DataFilterValueRange(BaseModel):
    dataFilter: DataFilter = Field(..., description="The data filter describing the location of the values in the spreadsheet.")
    majorDimension: Dimension = Field(..., description="The major dimension of the values.")
    values: List = Field(..., description="The data to be written. If the provided values exceed any of the ranges matched by the data filter then the request fails. If the provided values are less than the matched ranges only the specified values are written, existing values in the matched ranges remain unaffected.")

class BatchUpdateByDataFilterRequestBody(BaseModel):
    valueInputOption: ValueInputOption = Field(..., description="How the input data should be interpreted.")
    data: List[DataFilterValueRange] = Field(..., description="The new values to apply to the spreadsheet. If more than one range is matched by the specified DataFilter the specified values are applied to all of those ranges.")
    includeValuesInResponse: bool = Field(..., description="Determines if the update response should include the values of the cells that were updated. By default, responses do not include the updated values. The updatedData field within each of the BatchUpdateValuesResponse.responses contains the updated values. If the range to write was larger than the range actually written, the response includes all values in the requested range (excluding trailing empty rows and columns).")
    responseValueRenderOption: ValueRenderOption = Field(..., description="Determines how values in the response should be rendered. The default render option is FORMATTED_VALUE.")
    responseDateTimeRenderOption: DateTimeRenderOption = Field(..., description="Determines how dates, times, and durations in the response should be rendered. This is ignored if responseValueRenderOption is FORMATTED_VALUE. The default dateTime render option is SERIAL_NUMBER.")

class UpdateValuesByDataFilterResponse(BaseModel):
    updatedRange: str = Field(..., description="The range (in A1 notation) that updates were applied to.")
    updatedRows: int = Field(..., description="The number of rows where at least one cell in the row was updated.")
    updatedColumns: int = Field(..., description="The number of columns where at least one cell in the column was updated.")
    updatedCells: int = Field(..., description="The number of cells updated.")
    dataFilter: DataFilter = Field(..., description="The data filter that selected the range that was updated.")
    updatedData: ValueRange = Field(..., description="The values of the cells in the range matched by the dataFilter after all updates were applied. This is only included if the request's includeValuesInResponse field was true.")

class BatchUpdateByDataFilterResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The spreadsheet the updates were applied to.")
    totalUpdatedRows: int = Field(..., description="The total number of rows where at least one cell in the row was updated.")
    totalUpdatedColumns: int = Field(..., description="The total number of columns where at least one cell in the column was updated.")
    totalUpdatedCells: int = Field(..., description="The total number of cells updated.")
    totalUpdatedSheets: int = Field(..., description="The total number of sheets where at least one cell in the sheet was updated.")
    responses: List[UpdateValuesByDataFilterResponse] = Field(..., description="The response for each range updated.")

class ClearValuesResponse(BaseModel):
    spreadsheetId: str = Field(..., description="The spreadsheet the updates were applied to.")
    clearedRange: str = Field(..., description="The range (in A1 notation) that was cleared. (If the request was for an unbounded range or a range larger than the bounds of the sheet, this will be the actual range that was cleared, bounded to the sheet's limits.)")

class GetValuesRequestParams(BaseModel):
    majorDimension: Dimension = Field(..., description="The major dimension that results should use.")
    valueRenderOption: ValueRenderOption = Field(..., description="How values should be represented in the output. The default render option is FORMATTED_VALUE.")
    dateTimeRenderOption: DateTimeRenderOption = Field(..., description="How dates, times, and durations should be represented in the output. This is ignored if valueRenderOption is FORMATTED_VALUE. The default dateTime render option is SERIAL_NUMBER.")

class UpdateValuesRequestParams(BaseModel):
    valueInputOption: ValueInputOption = Field(..., description="How the input data should be interpreted.")
    includeValuesInResponse: bool = Field(..., description="Determines if the update response should include the values of the cells that were updated. By default, responses do not include the updated values. If the range to write was larger than the range actually written, the response includes all values in the requested range (excluding trailing empty rows and columns).")
    responseValueRenderOption: ValueRenderOption = Field(..., description="Determines how values in the response should be rendered. The default render option is FORMATTED_VALUE.")
    responseDateTimeRenderOption: DateTimeRenderOption = Field(..., description="Determines how dates, times, and durations in the response should be rendered. This is ignored if responseValueRenderOption is FORMATTED_VALUE. The default dateTime render option is SERIAL_NUMBER.")
