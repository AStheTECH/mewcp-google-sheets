from enum import Enum
from typing import List
from pydantic import Field, BaseModel

from .other import (
    DataSourceColumn,
    DataExecutionStatus,
    DataSourceColumnReference,
    BooleanCondition,
    SortSpec,
    HorizontalAlign,
    EmbeddedObjectPosition,
    FilterCriteria
)

from .cells import (
    CellData,
    CellFormat,
    FilterSpec,
    TextFormat
)

from .spreadsheets import (
    GridRange,
    ColorStyle,
)

from .developer_metadata import (
    DeveloperMetadata
)

from .api_types import (
    DimensionRange
)

from .charts import (
    EmbeddedChart
)



class GridProperties(BaseModel):
    rowCount: int = Field(..., description="The number of rows in the grid.")
    columnCount: int = Field(..., description="The number of columns in the grid.")
    frozenRowCount: int = Field(
        ..., description="The number of rows that are frozen in the grid."
    )
    frozenColumnCount: int = Field(
        ..., description="The number of columns that are frozen in the grid."
    )
    hideGridlines: bool = Field(
        ..., description="True if the grid isn't showing gridlines in the UI."
    )
    rowGroupControlAfter: bool = Field(
        ...,
        description="True if the row grouping control toggle is shown after the group.",
    )
    columnGroupControlAfter: bool = Field(
        ...,
        description="True if the column grouping control toggle is shown after the group.",
    )

class SheetType(Enum):
    SHEET_TYPE_UNSPECIFIED = "SHEET_TYPE_UNSPECIFIED"
    GRID = "GRID"
    OBJECT = "OBJECT"
    DATA_SOURCE = "DATA_SOURCE"


class DataSourceSheetProperties(BaseModel):
    dataSourceId: str = Field(..., description="ID of the DataSource the sheet is connected to.")
    columns: DataSourceColumn = Field(..., description="The columns displayed on the sheet, corresponding to the values in RowData.")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="The data execution status.")

class SheetProperties(BaseModel):
    sheetId: int = Field(
        ...,
        description="The ID of the sheet. Must be non-negative. This field cannot be changed once set.",
    )
    title: str = Field(..., description="The name of the sheet.")
    index: int = Field(
        ...,
        description="The index of the sheet within the spreadsheet. When adding or updating sheet properties, if this field is excluded then the sheet is added or moved to the end of the sheet list. When updating sheet indices or inserting sheets, movement is considered in 'before the move' indexes. A sheet index update request is ignored if the requested index is identical to the sheets current index or if the requested new index is equal to the current sheet index + 1.",
    )
    sheetType: SheetType = Field(
        ...,
        description="The type of sheet. Defaults to GRID. This field cannot be changed once set.",
    )
    gridProperties: GridProperties = Field(
        ...,
        description="Additional properties of the sheet if this sheet is a grid. When writing it is an error to set any grid properties on non-grid sheets. If this sheet is a DATA_SOURCE sheet, this field is output only but contains the properties that reflect how a data source sheet is rendered in the UI, e.g. rowCount.",
    )
    hidden: bool = Field(
        ..., description="True if the sheet is hidden in the UI, false if it's visible."
    )
    tabColorStyle: ColorStyle = Field(
        ..., description="The color of the tab in the UI."
    )
    rightToLeft: bool = Field(
        ..., description="True if the sheet is an RTL sheet instead of an LTR sheet."
    )
    dataSourceSheetProperties: DataSourceSheetProperties = Field(
        ...,
        description="Output only. If present, the field contains DATA_SOURCE sheet specific properties.",
    )

class RowData(BaseModel):
    values: List[CellData] = Field(..., description="The values in the row, one per column.")



class DimensionProperties(BaseModel):
    hiddenByFilter: bool = Field(..., description="True if this dimension is being filtered. This field is read-only.")
    hiddenByUser: bool = Field(..., description="True if this dimension is explicitly hidden.")
    pixelSize: int = Field(..., description="The height (if a row) or width (if a column) of the dimension in pixels.")
    developerMetadata: List[DeveloperMetadata] = Field(..., description="The developer metadata associated with a single row or column.")
    dataSourceColumnReference: DataSourceColumnReference = Field(..., description="Output only. If set, this is a column in a data source sheet.")

class GridData(BaseModel):
    startRow: int = Field(..., description="The first row this GridData refers to, zero-based.")
    startColumn: int = Field(..., description="The first column this GridData refers to, zero-based.")
    rowData: List[RowData] = Field(..., description="The data in the grid, one entry per row, starting with the row in startRow. The values in RowData will correspond to columns starting at startColumn.")
    rowMetadata: List[DimensionProperties] = Field(..., description="Metadata about the requested rows in the grid, starting with the row in startRow.")
    columnMetadata: List[DimensionProperties] = Field(..., description="Metadata about the requested columns in the grid, starting with the column in startColumn.")

class BooleanRule(BaseModel):
    condition: BooleanCondition = Field(..., description="The condition of the rule. If the condition evaluates to true, the format is applied.")
    format: CellFormat = Field(..., description="The format to apply. Conditional formatting can only apply a subset of formatting: bold, italic, strikethrough, foreground color and, background color.")

class InterpolationPointType(Enum):
    INTERPOLATION_POINT_TYPE_UNSPECIFIED = "INTERPOLATION_POINT_TYPE_UNSPECIFIED"
    MIN = "MIN"
    MAX = "MAX"
    NUMBER = "NUMBER"
    PERCENT = "PERCENT"
    PERCENTILE = "PERCENTILE"

class InterpolationPoint(BaseModel):
    colorStyle: ColorStyle = Field(..., description="The color this interpolation point should use.")
    type: InterpolationPointType = Field(..., description="How the value should be interpreted.")
    value: str = Field(..., description="The value this interpolation point uses. May be a formula. Unused if type is MIN or MAX.")

class GradientRule(BaseModel):
    minpoint: InterpolationPoint = Field(..., description="The starting interpolation point.")
    midpoint: InterpolationPoint = Field(..., description="An optional midway interpolation point.")
    maxpoint: InterpolationPoint = Field(..., description="The final interpolation point.")

class ConditionalFormatRule(BaseModel):
    ranges: List[GridRange] = Field(..., description="The ranges that are formatted if the condition is true. All the ranges must be on the same grid.")
    booleanRule: BooleanRule = Field(..., description="The formatting is either 'on' or 'off' according to the rule.")
    gradientRule: GradientRule = Field(..., description="The formatting will vary based on the gradients in the rule.")


class FilterView(BaseModel):
    filterViewId: int = Field(..., description="The ID of the filter view.")
    title: str = Field(..., description="The name of the filter view.")
    range: GridRange = Field(..., description="The range this filter view covers. When writing, only one of range, namedRangeId, or tableId may be set.")
    namedRangeId: str = Field(..., description="The named range this filter view is backed by, if any.When writing, only one of range, namedRangeId, or tableId may be set.")
    tableId: str = Field(..., description="The table this filter view is backed by, if any. When writing, only one of range, namedRangeId, or tableId may be set.")
    sortSpecs: List[SortSpec] = Field(..., description="The sort order per column. Later specifications are used when values are equal in the earlier specifications.")
    filterSpecs: List[FilterSpec] = Field(..., description="The filter criteria for showing or hiding values per column.")


class Editors(BaseModel):
    users: List[str] = Field(..., description="The email addresses of users with edit access to the protected range.")
    groups: List[str] = Field(..., description="The email addresses of groups with edit access to the protected range.")
    domainUsersCanEdit: bool = Field(..., description="True if anyone in the document's domain has edit access to the protected range. Domain protection is only supported on documents within a domain.")


class ProtectedRange(BaseModel):
    protectedRangeId: int = Field(..., description="The ID of the protected range. This field is read-only.")
    range: GridRange = Field(..., description="The range that is being protected. The range may be fully unbounded, in which case this is considered a protected sheet. When writing, only one of range or namedRangeId or tableId may be set.")
    namedRangeId: str = Field(..., description="The named range this protected range is backed by, if any. When writing, only one of range or namedRangeId or tableId may be set.")
    tableId: str = Field(..., description="The table this protected range is backed by, if any. When writing, only one of range or namedRangeId or tableId may be set.")
    description: str = Field(..., description="The description of this protected range.")
    warningOnly: bool = Field(..., description="True if this protected range will show a warning when editing. Warning-based protection means that every user can edit data in the protected range, except editing will prompt a warning asking the user to confirm the edit.")
    requestingUserCanEdit: bool = Field(..., description="True if the user who requested this protected range can edit the protected area. This field is read-only.")
    unprotectedRanges: List[GridRange] = Field(..., description="The list of unprotected ranges within a protected sheet. Unprotected ranges are only supported on protected sheets.")
    editors: Editors = Field(..., description="The users and groups with edit access to the protected range. This field is only visible to users with edit access to the protected range and the document. Editors are not supported with warningOnly protection.")


class BasicFilter(BaseModel):
    range: GridRange = Field(..., description="The range the filter covers.")
    tableid: str = Field(..., description="The table this filter is backed by, if any. When writing, only one of range or tableId may be set.")
    sortSpecs: List[SortSpec] = Field(..., description="The sort order per column. Later specifications are used when values are equal in the earlier specifications.")
    filterSpecs: List[FilterSpec] = Field(..., description="The filter criteria per column.")


class BandingProperties(BaseModel):
    headerColorStyle: ColorStyle = Field(..., description="The color of the first row or column. If this field is set, the first row or column is filled with this color and the colors alternate between firstBandColor and secondBandColor starting from the second row or column. Otherwise, the first row or column is filled with firstBandColor and the colors proceed to alternate as they normally would. If headerColor is also set, this field takes precedence.")
    firstBandColorStyle: ColorStyle = Field(..., description="The first color that is alternating. (Required) If firstBandColor is also set, this field takes precedence.")
    secondBandColorStyle: ColorStyle = Field(..., description="The second color that is alternating. (Required) If secondBandColor is also set, this field takes precedence.")
    footerColorStyle: ColorStyle = Field(..., description="The color of the last row or column. If this field is not set, the last row or column is filled with either firstBandColor or secondBandColor, depending on the color of the previous row or column. If footerColor is also set, this field takes precedence.")

class BandedRange(BaseModel):
    bandedRangeId: int = Field(..., description="The ID of the banded range. If unset, refer to bandedRangeReference.")
    bandedRangeReference: str = Field(..., description="Output only. The reference of the banded range, used to identify the ID that is not supported by the bandedRangeId.")
    range: GridRange = Field(..., description="The range over which these properties are applied.")
    rowProperties: BandingProperties = Field(..., description="Properties for row bands. These properties are applied on a row-by-row basis throughout all the rows in the range. At least one of rowProperties or columnProperties must be specified.")
    columnProperties: BandingProperties = Field(..., description="Properties for column bands. These properties are applied on a column- by-column basis throughout all the columns in the range. At least one of rowProperties or columnProperties must be specified.")

class DimensionGroup(BaseModel):
    range: DimensionRange = Field(..., description="The range over which this group exists.")
    depth: int = Field(..., description="The depth of the group, representing how many groups have a range that wholly contains the range of this group.")
    collapsed: bool = Field(..., description="This field is true if this group is collapsed. A collapsed group remains collapsed if an overlapping group at a shallower depth is expanded. A true value does not imply that all dimensions within the group are hidden, since a dimension's visibility can change independently from this group property. However, when this property is updated, all dimensions within it are set to hidden if this field is true, or set to visible if this field is false.")

class SlicerSpec(BaseModel):
    dataRange: GridRange = Field(..., description="The data range of the slicer.")
    filterCriteria: FilterCriteria = Field(..., description="The filtering criteria of the slicer.")
    columnIndex: int = Field(..., description="The zero-based column index in the data table on which the filter is applied to.")
    applyToPivotTables: bool = Field(..., description="True if the filter should apply to pivot tables. If not set, default to True.")
    title: str = Field(..., description="The title of the slicer.")
    textFormat: TextFormat = Field(..., description="The text format of title in the slicer. The link field is not supported.")
    backgroundColorStyle: ColorStyle = Field(..., description="The background color of the slicer. If backgroundColor is also set, this field takes precedence.")
    horizontalAlignment: HorizontalAlign = Field(..., description="The horizontal alignment of title in the slicer. If unspecified, defaults to LEFT")

class Slicer(BaseModel):
    slicerId: int = Field(..., description="The ID of the slicer.")
    spec: SlicerSpec = Field(..., description="The specification of the slicer.")
    position: EmbeddedObjectPosition = Field(..., description="The position of the slicer. Note that slicer can be positioned only on existing sheet. Also, width and height of slicer can be automatically adjusted to keep it within permitted limits.")

class TableRowsProperties(BaseModel):
    headerColorStyle: ColorStyle = Field(..., description="The color of the header row. If this field is set, the header row is filled with the specified color. Otherwise, the header row is filled with a default color.")
    firstBandColorStyle: ColorStyle = Field(..., description="The first color that is alternating. If this field is set, the first banded row is filled with the specified color. Otherwise, the first banded row is filled with a default color.")
    secondBandColorStyle: ColorStyle = Field(..., description="The second color that is alternating. If this field is set, the second banded row is filled with the specified color. Otherwise, the second banded row is filled with a default color.")
    footerColorStyle: ColorStyle = Field(..., description="The color of the last row. If this field is not set a footer is not added, the last row is filled with either firstBandColorStyle or secondBandColorStyle, depending on the color of the previous row.")

class ColumnType(Enum):
    COLUMN_TYPE_UNSPECIFIED = "COLUMN_TYPE_UNSPECIFIED"
    DOUBLE = "DOUBLE"
    CURRENCY = "CURRENCY"
    PERCENT = "PERCENT"
    DATE = "DATE"
    TIME = "TIME"
    DATE_TIME = "DATE_TIME"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DROPDOWN = "DROPDOWN"
    FILES_CHIP = "FILES_CHIP"
    PEOPLE_CHIP = "PEOPLE_CHIP"
    FINANCE_CHIP = "FINANCE_CHIP"
    PLACE_CHIP = "PLACE_CHIP"
    RATINGS_CHIP = "RATINGS_CHIP"

class TableColumnDataValidationRule(BaseModel):
    condition: BooleanCondition = Field(..., description="The condition that data in the cell must match. Valid only if the [BooleanCondition.type] is ONE_OF_LIST.")

class TableColumnProperties(BaseModel):
    columnIndex: int = Field(..., description="The 0-based column index. This index is relative to its position in the table and is not necessarily the same as the column index in the sheet.")
    columnName: str = Field(..., description="The column name.")
    columnType: ColumnType = Field(..., description="The column type.")
    dataValidationRule: TableColumnDataValidationRule = Field(..., description="The column data validation rule. Only set for dropdown column type.")

class Table(BaseModel):
    tableId: str = Field(..., description="The id of the table.")
    name: str = Field(..., description="The table name. This is unique to all tables in the same spreadsheet.")
    range: GridRange = Field(..., description="The table range.")
    rowsProperties: TableRowsProperties = Field(..., description="The table rows properties.")
    columnProperties: List[TableColumnProperties] = Field(..., description="The table column properties.")

class Sheet(BaseModel):
    properties: SheetProperties = Field(..., description="The properties of the sheet.")
    data: List[GridData] = Field(..., description="Data in the grid, if this is a grid sheet. The number of GridData objects returned is dependent on the number of ranges requested on this sheet.")
    merges: List[GridRange] = Field(..., description="The ranges that are merged together.")
    conditionalFormats: List[ConditionalFormatRule] = Field(..., description="The conditional format rules in this sheet.")
    filterViews: List[FilterView] = Field(..., description="The filter views in this sheet.")
    protectedRanges: List[ProtectedRange] = Field(..., description="The protected ranges in this sheet.")
    basicFilter: BasicFilter = Field(..., description="The filter on this sheet, if any.")
    charts: List[EmbeddedChart] = Field(..., description="The specifications of every chart on this sheet.")
    bandedRanges: List[BandedRange] = Field(..., description="The banded (alternating colors) ranges on this sheet.")
    developerMetadata: List[DeveloperMetadata] = Field(..., description="The developer metadata associated with a sheet.")
    rowGroups: List[DimensionGroup] = Field(..., description="All row groups on this sheet, ordered by increasing range start index, then by group depth.")
    columnGroups: List[DimensionGroup] = Field(..., description="All column groups on this sheet, ordered by increasing range start index, then by group depth.")
    slicers: List[Slicer] = Field(..., description="The slicers on this sheet.")
    tables: List[Table] = Field(..., description="The tables on this sheet.")


