from schemas import (
    Request,
    Response,
    Spreadsheet,
    DataFilter,
    DeveloperMetadata
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
