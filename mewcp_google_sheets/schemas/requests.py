from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from schemas import (
    SpreadsheetProperties,
    SheetProperties,
    DimensionProperties,
    DimensionRange,
    DataSourceColumnReference,
    NamedRange,
    GridRange,
    CellData,
    Dimension,
    GridCoordinate,
    Border,
    RowData,
    FilterView,
    EmbeddedObjectPosition,
    ConditionalFormatRule,
    SortSpec,
    DataValidationRule,
    BasicFilter,
    ProtectedRange,
    EmbeddedChart,
    ChartSpec,
    BandedRange,
    DeveloperMetadata,
    DataFilter,
    DimensionGroup,
    EmbeddedObjectBorder,
    Slicer,
    SlicerSpec,
    DataSource,
    Table
)

class UpdateSpreadsheetPropertiesRequest(BaseModel):
    properties: SpreadsheetProperties = Field(
        ..., description="The properties to update."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root 'properties' is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class UpdateSheetPropertiesRequest(BaseModel):
    properties: SheetProperties = Field(..., description="The properties to update.")
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root properties is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class DataSourceSheetDimensionRange(BaseModel):
    sheetId: int = Field(
        ..., description="The ID of the data source sheet the range is on."
    )
    columnReferences: List[DataSourceColumnReference] = Field(
        ..., description="The columns on the data source sheet."
    )

class UpdateDimensionPropertiesRequest(BaseModel):
    properties: DimensionProperties = Field(..., description="Properties to update.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root properties is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")
    range: DimensionRange = Field(..., description="The rows or columns to update.")
    dataSourceSheetRange: DataSourceSheetDimensionRange = Field(..., description="The columns on a data source sheet to update.")



class UpdateNamedRangeRequest(BaseModel):
    namedRange: NamedRange = Field(..., description="The named range to update with the new properties.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root namedRange is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")

class RepeatCellRequest(BaseModel):
    range: GridRange = Field(..., description="The range to repeat the cell in.")
    cell: CellData = Field(..., description="The data to write.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root cell is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class AddNamedRangeRequest(BaseModel):
    namedRange: NamedRange = Field(..., description="The named range to add. The namedRangeId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a range that already exists.)")


class DeleteNamedRangeRequest(BaseModel):
    namedRangeId: str = Field(..., description="The ID of the named range to delete.")


class AddSheetRequest(BaseModel):
    properties: SheetProperties = Field(..., description="The properties the new sheet should have. All properties are optional. The sheetId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a sheet that already exists.)")


class DeleteSheetRequest(BaseModel):
    sheetId: int = Field(..., description="The ID of the sheet to delete.")


class SourceAndDestination(BaseModel):
    source: GridRange = Field(..., description="The location of the data to use as the source of the autofill.")
    dimension: Dimension = Field(..., description="The dimension that data should be filled into.")
    fillLength: int = Field(..., description="The number of rows or columns that data should be filled into. Positive numbers expand beyond the last row or last column of the source. Negative numbers expand before the first row or first column of the source.")

class AutoFillRequest(BaseModel):
    useAlternateSeries: bool = Field(..., description="True if we should generate data with the 'alternate' series. This differs based on the type and amount of source data.")
    range: GridRange = Field(..., description="The range to autofill. This will examine the range and detect the location that has data and automatically fill that data in to the rest of the range.")
    sourceAndDestination: SourceAndDestination = Field(..., description="The source and destination areas to autofill. This explicitly lists the source of the autofill and where to extend that data.")


class PasteType(Enum):
    PASTE_NORMAL = "PASTE_NORMAL"
    PASTE_VALUES = "PASTE_VALUES"
    PASTE_FORMAT = "PASTE_FORMAT"
    PASTE_NO_BORDERS = "PASTE_NO_BORDERS"
    PASTE_FORMULA = "PASTE_FORMULA"
    PASTE_DATA_VALIDATION = "PASTE_DATA_VALIDATION"
    PASTE_CONDITIONAL_FORMATTING = "PASTE_CONDITIONAL_FORMATTING"

class CutPasteRequest(BaseModel):
    source: GridRange = Field(..., description="The source data to cut.")
    destination: GridCoordinate = Field(..., description="The top-left coordinate where the data should be pasted.")
    pasteType: PasteType = Field(..., description="What kind of data to paste. All the source data will be cut, regardless of what is pasted.")


class PasteOrientation(Enum):
    NORMAL = "NORMAL"
    TRANSPOSE = "TRANSPOSE"

class CopyPasteRequest(BaseModel):
    source: GridRange = Field(..., description="The source range to copy.")
    destination: GridRange = Field(..., description="The location to paste to. If the range covers a span that's a multiple of the source's height or width, then the data will be repeated to fill in the destination range. If the range is smaller than the source range, the entire source data will still be copied (beyond the end of the destination range).")
    pasteType: PasteType = Field(..., description="What kind of data to paste.")
    pasteOrientation: PasteOrientation = Field(..., description="How that data should be oriented when pasting.")


class MergeType(Enum):
    MERGE_ALL = "MERGE_ALL"
    MERGE_COLUMNS = "MERGE_COLUMNS"
    MERGE_ROWS = "MERGE_ROWS"

class MergeCellsRequest(BaseModel):
    range: GridRange = Field(..., description="The range of cells to merge.")
    mergeType: MergeType = Field(..., description="How the cells should be merged.")



class UnmergeCellsRequest(BaseModel):
    range: GridRange = Field(..., description="The range within which all cells should be unmerged. If the range spans multiple merges, all will be unmerged. The range must not partially span any merge.")

class UpdateBordersRequest(BaseModel):
    range: GridRange = Field(..., description="The range whose borders should be updated.")
    top: Border = Field(..., description="The border to put at the top of the range.")
    bottom: Border = Field(..., description="The border to put at the bottom of the range.")
    left: Border = Field(..., description="The border to put at the left of the range.")
    right: Border = Field(..., description="The border to put at the right of the range.")
    innerHorizontal: Border = Field(..., description="The horizontal border to put within the range.")
    innerVertical: Border = Field(..., description="The vertical border to put within the range.")


class UpdateCellsRequest(BaseModel):
    rows: List[RowData] = Field(..., description="The data to write.")
    fields: str = Field(..., description="The fields of CellData that should be updated. At least one field must be specified. The root is the CellData; 'row.values.' should not be specified. A single '*' can be used as short-hand for listing every field.")
    start: GridCoordinate = Field(..., description="The coordinate to start writing data at. Any number of rows and columns (including a different number of columns per row) may be written.")
    range: GridRange = Field(..., description="The range to write data to. If the data in rows does not cover the entire requested range, the fields matching those set in fields will be cleared.")


class AddFilterViewRequest(BaseModel):
    filter: FilterView = Field(..., description="The filter to add. The filterViewId field is optional. If one is not set, an ID will be randomly generated. (It is an error to specify the ID of a filter that already exists.)")


class AppendCellsRequest(BaseModel):
    sheetId: int = Field(..., description="The sheet ID to append the data to.")
    rows: List[RowData] = Field(..., description="The data to append.")
    fields: str = Field(..., description="The fields of CellData that should be updated. At least one field must be specified. The root is the CellData; 'row.values.' should not be specified. A single '*' can be used as short-hand for listing every field.")
    tableId: str = Field(..., description="The ID of the table to append data to. The data will be only appended to the table body.")


class ClearBasicFilterRequest(BaseModel):
    sheetId: int = Field(..., description="The sheet ID on which the basic filter should be cleared.")


class DeleteDimensionRequest(BaseModel):
    range: DimensionRange = Field(..., description="The dimensions to delete from the sheet.")

class DeleteEmbeddedObjectRequest(BaseModel):
    objectId: int = Field(..., description="The ID of the embedded object to delete.")

class DeleteFilterViewRequest(BaseModel):
    filterId: int = Field(..., description="The ID of the filter to delete.")

class DuplicateFilterViewRequest(BaseModel):
    filterId: int = Field(..., description="The ID of the filter being duplicated.")

class DuplicateSheetRequest(BaseModel):
    sourceSheetId: int = Field(..., description="The sheet to duplicate.")
    insertSheetIndex: int = Field(..., description="The zero-based index where the new sheet should be inserted. The index of all sheets after this are incremented.")
    newSheetId: int = Field(..., description="If set, the ID of the new sheet. If not set, an ID is chosen. If set, the ID must not conflict with any existing sheet ID. If set, it must be non-negative.")
    newSheetName: str = Field(..., description="The name of the new sheet. If empty, a new name is chosen for you.")

class FindReplaceRequest(BaseModel):
    find: str = Field(..., description="The value to search.")
    replacement: str = Field(..., description="The value to use as the replacement.")
    matchCase: bool = Field(..., description="True if the search is case sensitive.")
    matchEntireCell: bool = Field(..., description="True if the find value should match the entire cell.")
    searchByRegex: bool = Field(..., description="True if the find value is a regex.")
    includeFormulas: bool = Field(..., description="True if the search should include cells with formulas. False to skip cells with formulas.")
    range: GridRange = Field(..., description="The range to find/replace over.")
    sheetId: int = Field(..., description="The sheet to find/replace over.")
    allSheets: bool = Field(..., description="True to find/replace over all sheets.")


class InsertDimensionRequest(BaseModel):
    range: DimensionRange = Field(..., description="The dimensions to insert. Both the start and end indexes must be bounded.")
    inheritFromBefore: bool = Field(..., description="Whether dimension properties should be extended from the dimensions before or after the newly inserted dimensions. True to inherit from the dimensions before (in which case the start index must be greater than 0), and false to inherit from the dimensions after.")


class InsertRangeRequest(BaseModel):
    range: GridRange = Field(..., description="The range to insert new cells into. The range is constrained to the current sheet boundaries.")
    shiftDimension: Dimension = Field(..., description="The dimension which will be shifted when inserting cells. If ROWS, existing cells will be shifted down. If COLUMNS, existing cells will be shifted right.")


class MoveDimensionRequest(BaseModel):
    source: DimensionRange =  Field(..., description="The source dimensions to move.")
    destinationIndex: int =  Field(..., description="The zero-based start index of where to move the source data to, based on the coordinates before the source data is removed from the grid. Existing data will be shifted down or right (depending on the dimension) to make room for the moved dimensions. The source dimensions are removed from the grid, so the the data may end up in a different index than specified.")


class UpdateEmbeddedObjectPositionRequest(BaseModel):
    objectId: int = Field(..., description="The ID of the object to moved.")
    newPosition: EmbeddedObjectPosition = Field(..., description="An explicit position to move the embedded object to. If newPosition.sheetId is set, a new sheet with that ID will be created. If newPosition.newSheet is set to true, a new sheet will be created with an ID that will be chosen for you.")
    fields: str = Field(..., description="The fields of OverlayPosition that should be updated when setting a new position. Used only if newPosition.overlayPosition is set, in which case at least one field must be specified. The root newPosition.overlayPosition is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class PasteDataRequest(BaseModel):
    coordinate: GridCoordinate = Field(..., description="The coordinate at which the data should start being inserted.")
    data: str = Field(..., description="The data to insert.")
    type: PasteType = Field(..., description="How the data should be pasted.")
    delimiter: str = Field(..., description="The delimiter in the data.")
    html: bool = Field(..., description="True if the data is HTML.")


class DelimiterType(Enum):
    DELIMITER_TYPE_UNSPECIFIED = "DELIMITER_TYPE_UNSPECIFIED"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    PERIOD = "PERIOD"
    SPACE = "SPACE"
    CUSTOM = "CUSTOM"
    AUTODETECT = "AUTODETECT"

class TextToColumnsRequest(BaseModel):
    source: GridRange = Field(..., description="The source data range. This must span exactly one column.")
    delimiter: str = Field(..., description="The delimiter to use. Used only if delimiterType is CUSTOM.")
    delimiterType: DelimiterType = Field(..., description="The delimiter type to use.")

class UpdateFilterViewRequest(BaseModel):
    filter: FilterView = Field(..., description="The new properties of the filter view.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root filter is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class DeleteRangeRequest(BaseModel):
    range: GridRange = Field(..., description="The range of cells to delete.")
    shiftDimension: Dimension = Field(..., description="The dimension from which deleted cells will be replaced with. If ROWS, existing cells will be shifted upward to replace the deleted cells. If COLUMNS, existing cells will be shifted left to replace the deleted cells.")


class AppendDimensionRequest(BaseModel):
    sheetId: int = Field(..., description="The sheet to append rows or columns to.")
    dimension: Dimension = Field(..., description="Whether rows or columns should be appended.")
    length: int = Field(..., description="The number of rows or columns to append.")


class AddConditionalFormatRuleRequest(BaseModel):
    rule: ConditionalFormatRule = Field(..., description="The rule to add.")
    index: int = Field(..., description="The zero-based index where the rule should be inserted.")


class UpdateConditionalFormatRuleRequest(BaseModel):
    index: int = Field(..., description="The zero-based index of the rule that should be replaced or moved.")
    sheetId: int = Field(..., description="The zero-based index of the rule that should be replaced or moved.")
    rule: ConditionalFormatRule = Field(..., description="The rule that should replace the rule at the given index.")
    newIndex: int = Field(..., description="The zero-based new index the rule should end up at.")


class DeleteConditionalFormatRuleRequest(BaseModel):
    index: int = Field(..., description="The zero-based index of the rule to be deleted.")
    sheetId: int = Field(..., description="The sheet the rule is being deleted from.")


class SortRangeRequest(BaseModel):
    range: GridRange = Field(..., description="The range to sort.")
    sortSpecs: List[SortSpec] = Field(..., description="The sort order per column. Later specifications are used when values are equal in the earlier specifications.")


class SetDataValidationRequest(BaseModel):
    range: GridRange = Field(..., description="The range the data validation rule should apply to.")
    rule: DataValidationRule = Field(..., description="The data validation rule to set on each cell in the range, or empty to clear the data validation in the range.")
    filteredRowsIncluded: Optional[bool] = Field(..., description="If true, the data validation rule will be applied to the filtered rows as well.")

class SetBasicFilterRequest(BaseModel):
    filter: BasicFilter = Field(..., description="The filter to set.")

class AddProtectedRangeRequest(BaseModel):
    protectedRange: ProtectedRange = Field(..., description="The protected range to be added. The protectedRangeId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a range that already exists.)")


class UpdateProtectedRangeRequest(BaseModel):
    protectedRange: ProtectedRange = Field(..., description="The protected range to update with the new properties.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root protectedRange is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class DeleteProtectedRangeRequest(BaseModel):
    protectedRangeId: int = Field(..., description="The ID of the protected range to delete.")


class AutoResizeDimensionsRequest(BaseModel):
    dimensions: DimensionRange = Field(..., description="The dimensions to automatically resize.")
    dataSourceSheetDimensions: DataSourceSheetDimensionRange = Field(..., description="The dimensions on a data source sheet to automatically resize.")


class AddChartRequest(BaseModel):
    chart: EmbeddedChart = Field(..., description="The chart that should be added to the spreadsheet, including the position where it should be placed. The chartId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of an embedded object that already exists.)")


class UpdateChartSpecRequest(BaseModel):
    chartId: int = Field(..., description="The ID of the chart to update.")
    spec: ChartSpec = Field(..., description="The specification to apply to the chart.")


class UpdateBandingRequest(BaseModel):
    bandedRange: BandedRange = Field(..., description="The banded range to update with the new properties.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root bandedRange is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class AddBandingRequest(BaseModel):
    bandedRange: BandedRange = Field(..., description="The banded range to add. The bandedRangeId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a range that already exists.)")



class DeleteBandingRequest(BaseModel):
    bandedRangeId: int = Field(..., description="The ID of the banded range to delete.")


class CreateDeveloperMetadataRequest(BaseModel):
    developerMetadata: DeveloperMetadata = Field(..., description="The developer metadata to create.")

class UpdateDeveloperMetadataRequest(BaseModel):
    dataFilters: List[DataFilter] = Field(..., description="The filters matching the developer metadata entries to update.")
    developerMetadata: DeveloperMetadata = Field(..., description="The value that all metadata matched by the data filters will be updated to.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root developerMetadata is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class DeleteDeveloperMetadataRequest(BaseModel):
    dataFilter: DataFilter = Field(..., description="The data filter describing the criteria used to select which developer metadata entry to delete.")


class RandomizeRangeRequest(BaseModel):
    range: GridRange = Field(..., description="The range to randomize.")


class AddDimensionGroupRequest(BaseModel):
    range: DimensionRange = Field(..., description="The range over which to create a group.")

class DeleteDimensionGroupRequest(BaseModel):
    range: DimensionRange = Field(..., description="The range of the group to be deleted.")


class UpdateDimensionGroupRequest(BaseModel):
    dimensionGroup: DimensionGroup = Field(..., description="The group whose state should be updated. The range and depth of the group should specify a valid group on the sheet, and all other fields updated.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root dimensionGroup is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")

class TrimWhitespaceRequest(BaseModel):
    range: GridRange = Field(..., description="The range whose cells to trim.")


class DeleteDuplicatesRequest(BaseModel):
    range: GridRange = Field(..., description="The range to remove duplicates rows from.")
    comparisonColumns: List[DimensionRange] = Field(..., description="The columns in the range to analyze for duplicate values. If no columns are selected then all columns are analyzed for duplicates.")


class UpdateEmbeddedObjectBorderRequest(BaseModel):
    objectId: int = Field(..., description="The ID of the embedded object to update.")
    border: EmbeddedObjectBorder = Field(..., description="The border that applies to the embedded object.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root border is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class AddSlicerRequest(BaseModel):
    slicer: Slicer = Field(..., description="The slicer that should be added to the spreadsheet, including the position where it should be placed. The slicerId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a slicer that already exists.)")


class UpdateSlicerSpecRequest(BaseModel):
    slicerId: int = Field(..., description="The id of the slicer to update.")
    spec: SlicerSpec = Field(..., description="The specification to apply to the slicer.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root SlicerSpec is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class AddDataSourceRequest(BaseModel):
    dataSource: DataSource = Field(..., description="The data source to add.")

class UpdateDataSourceRequest(BaseModel):
    dataSource: DataSource = Field(..., description="The data source to update.")
    fields: str = Field(..., description="The fields that should be updated. At least one field must be specified. The root dataSource is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")


class DeleteDataSourceRequest(BaseModel):
    dataSourceId: str = Field(..., description="The ID of the data source to delete.")

class DataSourceObjectReference(BaseModel):
    sheetId: str = Field(..., description="References to a DATA_SOURCE sheet.")
    chartId: int = Field(..., description="References to a data source chart.")
    dataSourceTableAnchorCell: GridCoordinate = Field(..., description="References to a DataSourceTable anchored at the cell.")
    dataSourcePivotTableAnchorCell: GridCoordinate = Field(..., description="References to a data source PivotTable anchored at the cell.")
    dataSourceFormulaCell: GridCoordinate = Field(..., description="References to a cell containing DataSourceFormula.")

class DataSourceObjectReferences(BaseModel):
    references: List[DataSourceObjectReference] = Field(..., description="The references.")

class RefreshDataSourceRequest(BaseModel):
    force: bool = Field(..., description="Refreshes the data source objects regardless of the current state. If not set and a referenced data source object was in error state, the refresh will fail immediately.")
    references: DataSourceObjectReferences = Field(..., description="References to data source objects to refresh.")
    dataSourceId: str = Field(..., description="Reference to a DataSource. If specified, refreshes all associated data source objects for the data source.")
    isAll: bool = Field(..., description="Refreshes all existing data source objects in the spreadsheet.")



class CancelDataSourceRefreshRequest(BaseModel):
    references: DataSourceObjectReferences = Field(..., description="References to data source objects whose refreshes are to be cancelled.")
    dataSourceId: str = Field(..., description="Reference to a DataSource. If specified, cancels all associated data source object refreshes for this data source.")
    isAll: bool = Field(..., description="Cancels all existing data source object refreshes for all data sources in the spreadsheet.")

class AddTableRequest(BaseModel):
    table: Table = Field(..., description="Required. The table to add.")


class UpdateTableRequest(BaseModel):
    table: Table = Field(..., description="Required. The table to update.")
    fields: str = Field(..., description="Required. The fields that should be updated. At least one field must be specified. The root table is implied and should not be specified. A single '*' can be used as short-hand for listing every field.")

class DeleteTableRequest(BaseModel):
    tableId: str = Field(..., description="The ID of the table to delete.")

class Request(BaseModel):
    updateSpreadsheetProperties: UpdateSpreadsheetPropertiesRequest = Field(..., description="Updates the spreadsheet's properties.")
    updateSheetProperties: UpdateSheetPropertiesRequest = Field(..., description="Updates a sheet's properties.")
    updateDimensionProperties: UpdateDimensionPropertiesRequest = Field(..., description="Updates dimensions' properties.")
    updateNamedRange: UpdateNamedRangeRequest = Field(..., description="Updates a named range.")
    repeatCell: RepeatCellRequest = Field(..., description="Repeats a single cell across a range.")
    addNamedRange: AddNamedRangeRequest = Field(..., description="Adds a named range.")
    deleteNamedRange: DeleteNamedRangeRequest = Field(..., description="Deletes a named range.")
    addSheet: AddSheetRequest = Field(..., description="Adds a sheet.")
    deleteSheet: DeleteSheetRequest = Field(..., description="Deletes a sheet.")
    autoFill: AutoFillRequest = Field(..., description="Automatically fills in more data based on existing data.")
    cutPaste: CutPasteRequest = Field(..., description="Cuts data from one area and pastes it to another.")
    copyPaste: CopyPasteRequest = Field(..., description="Copies data from one area and pastes it to another.")
    mergeCells: MergeCellsRequest = Field(..., description="Merges cells together.")
    unmergeCells: UnmergeCellsRequest = Field(..., description="Unmerges merged cells.")
    updateBorders: UpdateBordersRequest = Field(..., description="Updates the borders in a range of cells.")
    updateCells: UpdateCellsRequest = Field(..., description="Updates many cells at once.")
    addFilterView: AddFilterViewRequest = Field(..., description="Adds a filter view.")
    appendCells: AppendCellsRequest = Field(..., description="Appends cells after the last row with data in a sheet.")
    clearBasicFilter: ClearBasicFilterRequest = Field(..., description="Clears the basic filter on a sheet.")
    deleteDimension: DeleteDimensionRequest = Field(..., description="Deletes rows or columns in a sheet.")
    deleteEmbeddedObject: DeleteEmbeddedObjectRequest = Field(..., description="Deletes an embedded object (e.g, chart, image) in a sheet.")
    deleteFilterView: DeleteFilterViewRequest = Field(..., description="Deletes a filter view from a sheet.")
    duplicateFilterView: DuplicateFilterViewRequest = Field(..., description="Duplicates a filter view.")
    duplicateSheet: DuplicateSheetRequest = Field(..., description="Duplicates a sheet.")
    findReplace: FindReplaceRequest = Field(..., description="Finds and replaces occurrences of some text with other text.")
    insertDimension: InsertDimensionRequest = Field(..., description="Inserts new rows or columns in a sheet.")
    insertRange: InsertRangeRequest = Field(..., description="Inserts new cells in a sheet, shifting the existing cells.")
    moveDimension: MoveDimensionRequest = Field(..., description="Moves rows or columns to another location in a sheet.")
    updateEmbeddedObjectPosition: UpdateEmbeddedObjectPositionRequest = Field(..., description="Updates an embedded object's (e.g. chart, image) position.")
    pasteData: PasteDataRequest = Field(..., description="Pastes data (HTML or delimited) into a sheet.")
    textToColumns: TextToColumnsRequest = Field(..., description="Converts a column of text into many columns of text.")
    updateFilterView: UpdateFilterViewRequest = Field(..., description="Updates the properties of a filter view.")
    deleteRange: DeleteRangeRequest = Field(..., description="Deletes a range of cells from a sheet, shifting the remaining cells.")
    appendDimension: AppendDimensionRequest = Field(..., description="Appends dimensions to the end of a sheet.")
    addConditionalFormatRule: AddConditionalFormatRuleRequest = Field(..., description="Adds a new conditional format rule.")
    updateConditionalFormatRule: UpdateConditionalFormatRuleRequest = Field(..., description="Updates an existing conditional format rule.")
    deleteConditionalFormatRule: DeleteConditionalFormatRuleRequest = Field(..., description="Deletes an existing conditional format rule.")
    sortRange: SortRangeRequest = Field(..., description="Sorts data in a range.")
    setDataValidation: SetDataValidationRequest = Field(..., description="Sets data validation for one or more cells.")
    setBasicFilter: SetBasicFilterRequest = Field(..., description="Sets the basic filter on a sheet.")
    addProtectedRange: AddProtectedRangeRequest = Field(..., description="Adds a protected range.")
    updateProtectedRange: UpdateProtectedRangeRequest = Field(..., description="Updates a protected range.")
    deleteProtectedRange: DeleteProtectedRangeRequest = Field(..., description="Deletes a protected range.")
    autoResizeDimensions: AutoResizeDimensionsRequest = Field(..., description="Automatically resizes one or more dimensions based on the contents of the cells in that dimension.")
    addChart: AddChartRequest = Field(..., description="Adds a chart.")
    updateChartSpec: UpdateChartSpecRequest = Field(..., description="Updates a chart's specifications.")
    updateBanding: UpdateBandingRequest = Field(..., description="Updates a banded range")
    addBanding: AddBandingRequest = Field(..., description="Adds a new banded range")
    deleteBanding: DeleteBandingRequest = Field(..., description="Removes a banded range")
    createDeveloperMetadata: CreateDeveloperMetadataRequest = Field(..., description="Creates new developer metadata")
    updateDeveloperMetadata: UpdateDeveloperMetadataRequest = Field(..., description="Updates an existing developer metadata entry")
    deleteDeveloperMetadata: DeleteDeveloperMetadataRequest = Field(..., description="Deletes developer metadata")
    randomizeRange: RandomizeRangeRequest = Field(..., description="Randomizes the order of the rows in a range.")
    addDimensionGroup: AddDimensionGroupRequest = Field(..., description="Creates a group over the specified range.")
    deleteDimensionGroup: DeleteDimensionGroupRequest = Field(..., description="Deletes a group over the specified range.")
    updateDimensionGroup: UpdateDimensionGroupRequest = Field(..., description="Updates the state of the specified group.")
    trimWhitespace: TrimWhitespaceRequest = Field(..., description="Trims cells of whitespace (such as spaces, tabs, or new lines).")
    deleteDuplicates: DeleteDuplicatesRequest = Field(..., description="Removes rows containing duplicate values in specified columns of a cell range.")
    updateEmbeddedObjectBorder: UpdateEmbeddedObjectBorderRequest = Field(..., description="Updates an embedded object's border.")
    addSlicer: AddSlicerRequest = Field(..., description="Adds a slicer.")
    updateSlicerSpec: UpdateSlicerSpecRequest = Field(..., description="Updates a slicer's specifications.")
    addDataSource: AddDataSourceRequest = Field(..., description="Adds a data source.")
    updateDataSource: UpdateDataSourceRequest = Field(..., description="Updates a data source.")
    deleteDataSource: DeleteDataSourceRequest = Field(..., description="Deletes a data source.")
    refreshDataSource: RefreshDataSourceRequest = Field(..., description="Refreshes one or multiple data sources and associated dbobjects.")
    cancelDataSourceRefresh: CancelDataSourceRefreshRequest = Field(..., description="Cancels refreshes of one or multiple data sources and associated dbobjects.")
    addTable: AddTableRequest = Field(..., description="Adds a table.")
    updateTable: UpdateTableRequest = Field(..., description="Updates a table.")
    deleteTable: DeleteTableRequest = Field(..., description="A request for deleting a table.")
