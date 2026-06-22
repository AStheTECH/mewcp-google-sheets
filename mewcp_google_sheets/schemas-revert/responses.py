from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from schemas import (
    NamedRange,
    GridCoordinate,
    SheetProperties,
    FilterView,
    EmbeddedObjectPosition,
    ConditionalFormatRule,
    ProtectedRange,
    EmbeddedChart,
    BandedRange,
    DeveloperMetadata,
    DimensionGroup,
    Slicer,
    DataSource,
    DataExecutionStatus,
    Table
)

class AddNamedRangeResponse(BaseModel):
    namedRange: NamedRange = Field(..., description="The named range to add.")


class DataSourceObjectReference(BaseModel):
    sheetId: str = Field(..., description="References to a DATA_SOURCE sheet.")
    chartId: int = Field(..., description="References to a data source chart.")
    dataSourceTableAnchorCell: GridCoordinate = Field(..., description="References to a DataSourceTable anchored at the cell.")
    dataSourcePivotTableAnchorCell: GridCoordinate = Field(..., description="References to a data source PivotTable anchored at the cell.")
    dataSourceFormulaCell: GridCoordinate = Field(..., description="References to a cell containing DataSourceFormula.")


class AddSheetResponse(BaseModel):
    properties: SheetProperties = Field(..., description="The properties of the newly added sheet.")


class AddFilterViewResponse(BaseModel):
    filter: FilterView = Field(..., description="The newly added filter view.")


class DuplicateFilterViewResponse(BaseModel):
    filter: FilterView = Field(..., description="The newly created filter.")

class DuplicateSheetResponse(BaseModel):
    properties: SheetProperties = Field(..., description="The properties of the duplicate sheet.")

class FindReplaceResponse(BaseModel):
    valuesChanged: int = Field(..., description="The number of non-formula cells changed.")
    formulasChanged: int = Field(..., description="The number of formula cells changed.")
    rowsChanged: int = Field(..., description="The number of rows changed.")
    sheetsChanged: int = Field(..., description="The number of sheets changed.")
    occurrencesChanged: int = Field(..., description="The number of occurrences (possibly multiple within a cell) changed.")

class UpdateEmbeddedObjectPositionResponse(BaseModel):
    position: EmbeddedObjectPosition = Field(..., description="The new position of the embedded object.")

class UpdateConditionalFormatRuleResponse(BaseModel):
    newrule: ConditionalFormatRule = Field(..., description="The new rule that replaced the old rule (if replacing), or the rule that was moved (if moved)")
    newIndex: int = Field(..., description="The index of the new rule.")
    oldRule: Optional[ConditionalFormatRule] = Field(..., description="The old (deleted) rule. Not set if a rule was moved (because it is the same as newRule).")
    oldIndex: Optional[int] = Field(..., description="The old index of the rule. Not set if a rule was replaced (because it is the same as newIndex).")

class DeleteConditionalFormatRuleResponse(BaseModel):
    rule: ConditionalFormatRule = Field(..., description="The rule that was deleted.")

class AddProtectedRangeResponse(BaseModel):
    protectedRange: ProtectedRange = Field(..., description="The newly added protected range.")

class AddChartResponse(BaseModel):
    chart: EmbeddedChart = Field(..., description="The newly added chart.")

class AddBandingResponse(BaseModel):
    bandedRange: BandedRange = Field(..., description="The banded range that was added.")

class CreateDeveloperMetadataResponse(BaseModel):
    developerMetadata: DeveloperMetadata = Field(..., description="The developer metadata that was created.")

class UpdateDeveloperMetadataResponse(BaseModel):
    developerMetadata: DeveloperMetadata = Field(..., description="The updated developer metadata.")

class DeleteDeveloperMetadataResponse(BaseModel):
    deletedDeveloperMetadata: List[DeveloperMetadata] = Field(..., description="The metadata that was deleted.")

class AddDimensionGroupResponse(BaseModel):
    dimensionGroups: List[DimensionGroup] = Field(..., description="All groups of a dimension after adding a group to that dimension.")

class DeleteDimensionGroupResponse(BaseModel):
    dimensionGroups: List[DimensionGroup] = Field(..., description="All groups of a dimension after deleting a group from that dimension.")

class TrimWhitespaceResponse(BaseModel):
    cellsChangedCount: int = Field(..., description="The number of cells that were trimmed of whitespace.")

class DeleteDuplicatesResponse(BaseModel):
    duplicatesRemovedCount: int = Field(..., description="The number of duplicate rows removed.")

class AddSlicerResponse(BaseModel):
    slicer: Slicer = Field(..., description="The newly added slicer.")

class AddDataSourceResponse(BaseModel):
    dataSource: DataSource = Field(..., description="The data source that was created.")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="The data execution status.")

class UpdateDataSourceResponse(BaseModel):
    dataSource: DataSource = Field(..., description="The updated data source.")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="The data execution status.")

class RefreshDataSourceObjectExecutionStatus(BaseModel):
    reference: DataSourceObjectReference = Field(..., description="Reference to a data source object being refreshed.")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="The data execution status.")

class RefreshDataSourceResponse(BaseModel):
    statuses: List[RefreshDataSourceObjectExecutionStatus] = Field(..., description="All the refresh status for the data source object references specified in the request. If isAll is specified, the field contains only those in failure status.")

class RefreshCancellationState(Enum):
    REFRESH_CANCELLATION_STATE_UNSPECIFIED = "REFRESH_CANCELLATION_STATE_UNSPECIFIED"
    CANCEL_SUCCEEDED = "CANCEL_SUCCEEDED"
    CANCEL_FAILED = "CANCEL_FAILED"

class RefreshCancellationErrorCode(Enum):
    REFRESH_CANCELLATION_ERROR_CODE_UNSPECIFIED = "REFRESH_CANCELLATION_ERROR_CODE_UNSPECIFIED"
    EXECUTION_NOT_FOUND = "EXECUTION_NOT_FOUND"
    CANCEL_PERMISSION_DENIED = "CANCEL_PERMISSION_DENIED"
    QUERY_EXECUTION_COMPLETED = "QUERY_EXECUTION_COMPLETED"
    CONCURRENT_CANCELLATION = "CONCURRENT_CANCELLATION"
    CANCEL_OTHER_ERROR = "CANCEL_OTHER_ERROR"

class RefreshCancellationStatus(BaseModel):
    state: RefreshCancellationState = Field(..., description="The state of a call to cancel a refresh in Sheets.")
    errorCode: RefreshCancellationErrorCode = Field(..., description="The error code.")

class CancelDataSourceRefreshStatus(BaseModel):
    reference: DataSourceObjectReference = Field(..., description="Reference to the data source object whose refresh is being cancelled.")
    refreshCancellationStatus: RefreshCancellationStatus = Field(..., description="The cancellation status.")

class CancelDataSourceRefreshResponse(BaseModel):
    statuses: List[CancelDataSourceRefreshStatus] = Field(..., description="The cancellation statuses of refreshes of all data source objects specified in the request. If isAll is specified, the field contains only those in failure status. Refreshing and canceling refresh the same data source object is also not allowed in the same batchUpdate.")

class AddTableResponse(BaseModel):
    table: Table = Field(..., description="Output only. The table that was added.")

class Response(BaseModel):
    addNamedRange: AddNamedRangeResponse = Field(..., description = "A reply from adding a named range.")
    addSheet: AddSheetResponse = Field(..., description = "A reply from adding a sheet.")
    addFilterView: AddFilterViewResponse = Field(..., description = "A reply from adding a filter view.")
    duplicateFilterView: DuplicateFilterViewResponse = Field(..., description = "A reply from duplicating a filter view.")
    duplicateSheet: DuplicateSheetResponse = Field(..., description = "A reply from duplicating a sheet.")
    findReplace: FindReplaceResponse = Field(..., description = "A reply from doing a find/replace.")
    updateEmbeddedObjectPosition: UpdateEmbeddedObjectPositionResponse = Field(..., description = "A reply from updating an embedded object's position.")
    updateConditionalFormatRule: UpdateConditionalFormatRuleResponse = Field(..., description = "A reply from updating a conditional format rule.")
    deleteConditionalFormatRule: DeleteConditionalFormatRuleResponse = Field(..., description = "A reply from deleting a conditional format rule.")
    addProtectedRange: AddProtectedRangeResponse = Field(..., description = "A reply from adding a protected range.")
    addChart: AddChartResponse = Field(..., description = "A reply from adding a chart.")
    addBanding: AddBandingResponse = Field(..., description = "A reply from adding a banded range.")
    createDeveloperMetadata: CreateDeveloperMetadataResponse = Field(..., description = "A reply from creating a developer metadata entry.")
    updateDeveloperMetadata: UpdateDeveloperMetadataResponse = Field(..., description = "A reply from updating a developer metadata entry.")
    deleteDeveloperMetadata: DeleteDeveloperMetadataResponse = Field(..., description = "A reply from deleting a developer metadata entry.")
    addDimensionGroup: AddDimensionGroupResponse = Field(..., description = "A reply from adding a dimension group.")
    deleteDimensionGroup: DeleteDimensionGroupResponse = Field(..., description = "A reply from deleting a dimension group.")
    trimWhitespace: TrimWhitespaceResponse = Field(..., description = "A reply from trimming whitespace.")
    deleteDuplicates: DeleteDuplicatesResponse = Field(..., description = "A reply from removing rows containing duplicate values.")
    addSlicer: AddSlicerResponse = Field(..., description = "A reply from adding a slicer.")
    addDataSource: AddDataSourceResponse = Field(..., description = "A reply from adding a data source.")
    updateDataSource: UpdateDataSourceResponse = Field(..., description = "A reply from updating a data source.")
    refreshDataSource: RefreshDataSourceResponse = Field(..., description = "A reply from refreshing data source objects.")
    cancelDataSourceRefresh: CancelDataSourceRefreshResponse = Field(..., description = "A reply from cancelling data source object refreshes.")
    addTable: AddTableResponse = Field(..., description = "A reply from adding a table.")
