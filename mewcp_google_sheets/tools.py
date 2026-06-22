import logging
from datetime import datetime, timedelta
from typing import List
from pydantic import Field

from fastmcp import FastMCP

from .newschemas import (
    Spreadsheet,
    DeveloperMetadata,
    SheetProperties,
    ValueRange,
    UpdateValuesResponse
)

from .models import (
    BatchUpdateSpreadsheetRequest,
    CreateSpreadSheetResponse,
    ToolError,
    GetSpreadsheetQueryParams,
    GetByDataFilterRequestBody,
    SearchDeveloperMetadataRequestBody,
    SearchDeveloperMetadataResponse,
    CopyToRequestBody,
    AppendValuesQueryParams,
    AppendValuesResponse,
    BatchClearValuesRequestBody,
    BatchClearValuesResponse,
    BatchClearByDataFilterRequestBody,
    BatchClearByDataFilterResponse,
    BatchGetValuesQueryParams,
    BatchGetValuesResponse,
    BatchGetByDataFilterRequestBody,
    BatchGetByDataFilterResponse,
    BatchUpdateValuesRequestBody,
    BatchUpdateValuesResponse,
    BatchUpdateByDataFilterRequestBody,
    BatchUpdateByDataFilterResponse,
    ClearValuesResponse,
    GetValuesRequestParams,
    UpdateValuesRequestParams
)
from .service import get_service

logger = logging.getLogger("calendar-mcp-server")


class _ToolCollector:
    def __init__(self):
        self.items = []

    def tool(self, *args, **kwargs):
        def decorator(func):
            self.items.append((args, kwargs, func))
            return func

        return decorator


mcp = _ToolCollector()


def register_tools(real_mcp: FastMCP) -> None:
    for args, kwargs, func in mcp.items:
        real_mcp.tool(*args, **kwargs)(func)

# @mcp.tool(
#     name="spreadsheets_batch_update",
#     description="Applies one or more updates to the spreadsheet."
# )
# def spreadsheets_batch_update(spreadsheetId: str = Field(..., description="The spreadsheet to apply the updates to."), body: BatchUpdateSpreadsheetRequest = Field(..., description="The request body for batch updating a spreadsheet.")) -> CreateSpreadSheetResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while batch updating: {exc}", exc_info=True)
#         return {"error": str(exc)}

@mcp.tool(
    name="create_spreadsheet",
    description="Creates a spreadsheet, returning the newly created spreadsheet."
)
def create_spreadsheet(body: Spreadsheet = Field(..., description="The request body contains an instance of Spreadsheet")) -> Spreadsheet | ToolError:
    try:
        response = get_service().spreadsheets().create(body=body).execute()
        return response
    except Exception as exc:
        logger.error(f"error while creating a spreadsheet: {exc}", exc_info=True)
        return {"error": str(exc)}


# @mcp.tool(
#     name="get_spreadsheet",
#     description="Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID."
# )
# def get_spreadsheet(spreadsheetId: str = Field(..., description="The spreadsheet to request."), queryParams: GetSpreadsheetQueryParams = Field(..., description="Query Parameters")) -> Spreadsheet | ToolError:
#     try:
#         response = get_service().spreadsheets().get(spreadsheetId=spreadsheetId, params=queryParams).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while getting a spreadsheet: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="getByDataFilter_spreadsheet",
#     description="Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID.This method differs from spreadsheets.get in that it allows selecting which subsets of spreadsheet data to return by specifying a dataFilters parameter. Multiple DataFilters can be specified. Specifying one or more data filters returns the portions of the spreadsheet that intersect ranges matched by any of the filters."
# )
# def getByDataFilter_spreadsheet(spreadsheetId: str = Field(..., description="The spreadsheet to request."), body = GetByDataFilterRequestBody) -> Spreadsheet | ToolError:
#     try:
#         response = get_service().spreadsheets().getByDataFilter(spreadsheetId = spreadsheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while getting the spreadsheet by data filter: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="get_developerMetadata",
#     description="Returns the developer metadata with the specified ID. The caller must specify the spreadsheet ID and the developer metadata's unique metadataId"
# )
# def get_developerMetadata(spreadsheetId: str = Field(..., description="The spreadsheet to request."), metadataId : str = Field(..., description="The ID of the developer metadata to retrieve.")) -> DeveloperMetadata | ToolError:
#     try:
#         response = get_service().spreadsheets().getByDataFilter(spreadsheetId = spreadsheetId, metadataId= metadataId).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while getting the developer metadata: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="search_developerMetadata",
#     description="Returns all developer metadata matching the specified DataFilter"
# )
# def search_developerMetadata(spreadsheetId: str = Field(..., description="The ID of the spreadsheet to retrieve metadata from."), params: SearchDeveloperMetadataRequestBody = Field(..., description="Search Developer Metadata Request Body")) -> SearchDeveloperMetadataResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().developerMetadata().search(spreadsheetId = spreadsheetId, body = params).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while searching the developer metadata: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="copyTo_sheets",
#     description="Copies a single sheet from a spreadsheet to another spreadsheet. Returns the properties of the newly created sheet."
# )
# def copyTo_sheets(spreadsheetId: str = Field(..., description="The ID of the spreadsheet containing the sheet to copy."), sheetId: str = Field(..., description="The ID of the sheet to copy."), body: CopyToRequestBody = Field(..., description="The request body contains data with destination spreadsheet Id")) -> SheetProperties | ToolError:
#     try:
#         response = get_service().spreadsheets().sheets().copyTo(spreadsheetId = spreadsheetId, sheetId = sheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while copying the sheet: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="append_values_spreadsheets",
#     description="Appends values to a spreadsheet. The input range is used to search for existing data and find a 'table' within that range. Values will be appended to the next row of the table, starting with the first column of the table."
# )
# def append_values_spreadsheets(spreadsheetId: str = Field(..., description="The ID of the spreadsheet to update."), range: str = Field(..., description="The A1 notation of a range to search for a logical table of data. Values are appended after the last row of the table."), params: AppendValuesQueryParams = Field(..., description="Query Parameters to append values to spreadsheet"), body: ValueRange = Field(..., description="The request body contains an instance of ValueRange.")) -> AppendValuesResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().append(spreadsheetId = spreadsheetId, range = range, params = params, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while appending values to the spreadsheet: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="batchClear_values_spreadsheets",
#     description="Clears one or more ranges of values from a spreadsheet. The caller must specify the spreadsheet ID and one or more ranges. Only values are cleared -- all other properties of the cell (such as formatting and data validation) are kept."
# )
# def batchClear_values_spreadsheets(spreadsheetId: str = Field(..., description="The ID of the spreadsheet to update."), body: BatchClearValuesRequestBody = Field(..., description="The request body contains the ranges to clear")) -> BatchClearValuesResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().batchClear(spreadsheetId = spreadsheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while batch clearing values from ranges supplied: {exc}", exc_info=True)
#         return {"error": str(exc)}


# @mcp.tool(
#     name="batchClearByDataFilter_values_spreadsheets",
#     description="Clears one or more ranges of values from a spreadsheet. For more information, see Read, write, and search metadata. The caller must specify the spreadsheet ID and one or more DataFilters. Ranges matching any of the specified data filters will be cleared. Only values are cleared -- all other properties of the cell (such as formatting, data validation, etc.) are kept."
# )
# def batchClearByDataFilter_values_spreadsheets(spreadsheetId: str = Field(..., description="The ID of the spreadsheet to update."), body: BatchClearByDataFilterRequestBody = Field(..., description="The request body contains the data filters used to determine the ranges to clear")) -> BatchClearByDataFilterResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().batchClearByDataFilter(spreadsheetId = spreadsheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while batch clearing values based on data filters supplied: {exc}", exc_info=True)
#         return {"error": str(exc)}


# @mcp.tool(
#     name="batchGet_values_spreadsheets",
#     description="Returns one or more ranges of values from a spreadsheet. The caller must specify the spreadsheet ID and one or more ranges."
# )
# def batchGet_values_spreadsheets(spreadsheetId: str, params = BatchGetValuesQueryParams) -> BatchGetValuesResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, params = params).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while getting batch values: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="batchGetByDataFilter_values_spreadsheets",
#     description="Returns one or more ranges of values that match the specified data filters. For more information, see Read, write, and search metadata. The caller must specify the spreadsheet ID and one or more DataFilters. Ranges that match any of the data filters in the request will be returned."
# )
# def batchGetByDataFilter_values_spreadsheets(spreadsheetId: str, body: BatchGetByDataFilterRequestBody) -> BatchGetByDataFilterResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().batchGetByDataFilter(spreadsheetId= spreadsheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while getting batch values by data filter: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="batchUpdate_values_spreadsheets",
#     description="Sets values in one or more ranges of a spreadsheet. The caller must specify the spreadsheet ID, a valueInputOption, and one or more ValueRanges."
# )
# def batchUpdate_values_spreadsheets(spreadsheetId: str, body: BatchUpdateValuesRequestBody) -> BatchUpdateValuesResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().batchUpdate(spreadsheetId= spreadsheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while updating batch values: {exc}", exc_info=True)
#         return {"error": str(exc)}


# @mcp.tool(
#     name="batchUpdateByDataFilter_values_spreadsheets",
#     description="Sets values in one or more ranges of a spreadsheet. For more information, see Read, write, and search metadata. The caller must specify the spreadsheet ID, a valueInputOption, and one or more DataFilterValueRanges."
# )
# def batchUpdateByDataFilter_values_spreadsheets(spreadsheetId: str, body: BatchUpdateByDataFilterRequestBody) -> BatchUpdateByDataFilterResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().batchUpdateByDataFilter(spreadsheetId= spreadsheetId, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while updating batch values by data filter: {exc}", exc_info=True)
#         return {"error": str(exc)}



# @mcp.tool(
#     name="clear_values_spreadsheets",
#     description="Clears values from a spreadsheet. The caller must specify the spreadsheet ID and range. Only values are cleared -- all other properties of the cell (such as formatting, data validation, etc..) are kept."
# )
# def clear_values_spreadsheets(spreadsheetId: str, range: str) -> ClearValuesResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().clear(spreadsheetId= spreadsheetId, range= range).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while clearing values from spreadsheet: {exc}", exc_info=True)
#         return {"error": str(exc)}



# @mcp.tool(
#     name="get_values_spreadsheets",
#     description="Returns a range of values from a spreadsheet. The caller must specify the spreadsheet ID and a range."
# )
# def get_values_spreadsheets(spreadsheetId: str, range: str, params: GetValuesRequestParams) -> ValueRange | ToolError:
#     try:
#         response = get_service().spreadsheets().values().get(spreadsheetId= spreadsheetId, range= range, params = params).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while getting values from spreadsheet: {exc}", exc_info=True)
#         return {"error": str(exc)}

# @mcp.tool(
#     name="update_values_spreadsheets",
#     description="Sets values in a range of a spreadsheet. The caller must specify the spreadsheet ID, range, and a valueInputOption."
# )
# def update_values_spreadsheets(spreadsheetId: str, range: str, params: UpdateValuesRequestParams, body: ValueRange) -> UpdateValuesResponse | ToolError:
#     try:
#         response = get_service().spreadsheets().values().get(spreadsheetId= spreadsheetId, range= range, params = params, body = body).execute()
#         return response
#     except Exception as exc:
#         logger.error(f"error while updating values in spreadsheet: {exc}", exc_info=True)
#         return {"error": str(exc)}

