from enum import Enum
from typing import Any, Dict, List, Optional, TypedDict
from xmlrpc.client import boolean

from pydantic import BaseModel, Field


class ToolError(TypedDict):
    error: str


GoogleSheetsToolResponse = dict[str, Any] | ToolError

ApiObjectResponse = dict[str, Any] | ToolError


class RecalculationInterval(Enum):
    UNSPECIFIED = "RECALCULATION_INTERVAL_UNSPECIFIED"
    ON_CHANGE = "ON_CHANGE"
    MINUTE = "MINUTE"
    HOUR = "HOUR"


class NumberFormatType(Enum):
    NUMBER_FORMAT_TYPE_UNSPECIFIED = "NUMBER_FORMAT_TYPE_UNSPECIFIED"
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    PERCENT = "PERCENT"
    CURRENCY = "CURRENCY"
    DATE = "DATE"
    TIME = "TIME"
    DATE_TIME = "DATE_TIME"
    SCIENTIFIC = "SCIENTIFIC"


class NumberFormat(BaseModel):
    type: NumberFormatType = Field(
        ...,
        description="The type of the number format. When writing, this field must be set.",
    )
    pattern: str = Field(
        ...,
        description="Pattern string used for formatting. If not set, a default pattern based on the spreadsheet's locale will be used if necessary for the given type.",
    )


class Color(BaseModel):
    red: int = Field(
        ...,
        description="The amount of red in the color as a value in the interval [0, 1].",
    )
    green: int = Field(
        ...,
        description="The amount of green in the color as a value in the interval [0, 1].",
    )
    blue: int = Field(
        ...,
        description="The amount of blue in the color as a value in the interval [0, 1].",
    )
    alpha: int = Field(
        ...,
        description="The fraction of this color that should be applied to the pixel. That is, the final pixel color is defined by the equation:",
    )


class ThemeColorType(Enum):
    THEME_COLOR_TYPE_UNSPECIFIED = "THEME_COLOR_TYPE_UNSPECIFIED"
    TEXT = "TEXT"
    ACCENT1 = "ACCENT1"
    ACCENT2 = "ACCENT2"
    ACCENT3 = "ACCENT3"
    ACCENT4 = "ACCENT4"
    ACCENT5 = "ACCENT5"
    ACCENT6 = "ACCENT6"
    LINK = "LINK"


class ColorStyle(BaseModel):
    rgbColor: Color = Field(
        ...,
        description="RGB color. The alpha value in the Color object isn't generally supported",
    )
    themeColor: ThemeColorType = Field(..., description="Theme color.")


class Style(Enum):
    STYLE_UNSPECIFIED = "STYLE_UNSPECIFIED"
    DOTTED = "DOTTED"
    DASHED = "DASHED"
    SOLID = "SOLID"
    SOLID_MEDIUM = "SOLID_MEDIUM"
    SOLID_THICK = "SOLID_THICK"
    NONE = "NONE"
    DOUBLE = "DOUBLE"


class Border(BaseModel):
    style: Style = Field(..., description="The style of the border.")
    colorStyle: ColorStyle = Field(..., description="The color of the border.")


class Borders(BaseModel):
    top: Border = Field(..., description="The top border of the cell")
    bottom: Border = Field(..., description="The bottom border of the cell")
    left: Border = Field(..., description="The left border of the cell")
    right: Border = Field(..., description="The right border of the cell")


class Padding(BaseModel):
    top: int = Field(..., description="The top padding of the cell.")
    right: int = Field(..., description="The right padding of the cell.")
    bottom: int = Field(..., description="The bottom padding of the cell.")
    left: int = Field(..., description="The left padding of the cell.")


class HorizontalAlign(Enum):
    HORIZONTAL_ALIGN_UNSPECIFIED = "HORIZONTAL_ALIGN_UNSPECIFIED"
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class VerticalAlign(Enum):
    VERTICAL_ALIGN_UNSPECIFIED = "VERTICAL_ALIGN_UNSPECIFIED"
    TOP = "TOP"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"


class WrapStrategy(Enum):
    WRAP_STRATEGY_UNSPECIFIED = "WRAP_STRATEGY_UNSPECIFIED"
    OVERFLOW_CELL = "OVERFLOW_CELL"
    LEGACY_WRAP = "LEGACY_WRAP"
    CLIP = "CLIP"
    WRAP = "WRAP"


class TextDirection(Enum):
    TEXT_DIRECTION_UNSPECIFIED = "TEXT_DIRECTION_UNSPECIFIED"
    LEFT_TO_RIGHT = "LEFT_TO_RIGHT"
    RIGHT_TO_LEFT = "RIGHT_TO_LEFT"


class Link(BaseModel):
    uri: str = Field(..., description="The link identifier.")


class TextFormat(BaseModel):
    foregroundColorStyle: ColorStyle = Field(
        ..., description="The foreground color of the text."
    )
    fontFamily: str = Field(..., description="The font family.")
    fontSize: int = Field(..., description="The size of the font.")
    bold: bool = Field(..., description="True if the text is bold.")
    italic: bool = Field(..., description="True if the text is italicized.")
    strikethrough: bool = Field(
        ..., description="True if the text has a strikethrough."
    )
    underline: bool = Field(..., description="True if the text is underlined.")
    link: Link = Field(
        ...,
        description="The link destination of the text, if any. Setting the link field in a TextFormatRun will clear the cell's existing links or a cell-level link set in the same request. When a link is set, the text foreground color will be set to the default link color and the text will be underlined. If these fields are modified in the same request, those values will be used instead of the link defaults.",
    )


class HyperlinkDisplayType(Enum):
    HYPERLINK_DISPLAY_TYPE_UNSPECIFIED = "HYPERLINK_DISPLAY_TYPE_UNSPECIFIED"
    LINKED = "LINKED"
    PLAIN_TEXT = "PLAIN_TEXT"


class TextRotation(BaseModel):
    angle: int = Field(
        ...,
        description="The angle between the standard orientation and the desired orientation. Measured in degrees. Valid values are between -90 and 90. Positive angles are angled upwards, negative are angled downwards.Note: For LTR text direction positive angles are in the counterclockwise direction, whereas for RTL they are in the clockwise direction",
    )
    vertical: bool = Field(
        ...,
        description="If true, text reads top to bottom, but the orientation of individual characters is unchanged",
    )


class CellFormat(BaseModel):
    numberFormat: NumberFormat = Field(
        ...,
        description="A format describing how number values should be represented to the user.",
    )
    backgroundColorStyle: ColorStyle = Field(
        ..., description="The background color of the cell."
    )
    borders: Borders = Field(..., description="The borders of the cell.")
    padding: Padding = Field(..., description="The padding of the cell.")
    horizontalAlignment: HorizontalAlign = Field(
        ..., description="The horizontal alignment of the value in the cell."
    )
    verticalAlignment: VerticalAlign = Field(
        ..., description="The vertical alignment of the value in the cell."
    )
    wrapStrategy: WrapStrategy = Field(
        ..., description="The wrap strategy for the value in the cell."
    )
    textDirection: TextDirection = Field(
        ..., description="The direction of the text in the cell."
    )
    textFormat: TextFormat = Field(
        ...,
        description="The format of the text in the cell (unless overridden by a format run). Setting a cell-level link here clears the cell's existing links. Setting the link field in a TextFormatRun takes precedence over the cell-level link.",
    )
    hyperlinkDisplayType: HyperlinkDisplayType = Field(
        ...,
        description="If one exists, how a hyperlink should be displayed in the cell.",
    )
    textRotation: TextRotation = Field(
        ..., description="The rotation applied to text in the cell."
    )


class IterativeCalculationSettings(BaseModel):
    maxIterations: int = Field(
        ...,
        description="When iterative calculation is enabled, the maximum number of calculation rounds to perform.",
    )
    convergenceThreshold: int = Field(
        ...,
        description="When iterative calculation is enabled and successive results differ by less than this threshold value, the calculation rounds stop.",
    )


class ThemeColorPair(BaseModel):
    colorType: ThemeColorType = Field(
        ..., description="The type of the spreadsheet theme color."
    )
    color: ColorStyle = Field(
        ..., description="The concrete color corresponding to the theme color type."
    )


class SpreadsheetTheme(BaseModel):
    primaryFontFamily: str = Field(..., description="Name of the primary font family.")
    themeColors: ThemeColorPair = Field(
        ...,
        description="The spreadsheet theme color pairs. To update you must provide all theme color pairs.",
    )


class SpreadsheetProperties(BaseModel):
    title: str = Field(..., description="The title of the spreadsheet.")
    locale: str = Field(
        ...,
        description="The locale of the spreadsheet in one of the following formats: an ISO 639-1 language code such as en; an ISO 639-2 language code such as fil, if no 639-1 code exists; a combination of the ISO language code and country code, such as en_US; Note: when updating this field, not all locales/languages are supported.",
    )
    autoRecalc: RecalculationInterval = Field(
        RecalculationInterval.UNSPECIFIED,
        description="The amount of time to wait before volatile functions are recalculated.",
    )
    timeZone: str = Field(
        ...,
        description="The time zone of the spreadsheet, in CLDR format such as America/New_York. If the time zone isn't recognized, this may be a custom time zone such as GMT-07:00.",
    )
    defaultFormat: CellFormat = Field(
        ...,
        description="The default format of all cells in the spreadsheet. CellData.effectiveFormat will not be set if the cell's format is equal to this default format. This field is read-only.",
    )
    iterativeCalculationSettings: IterativeCalculationSettings = Field(
        ...,
        description="Determines whether and how circular references are resolved with iterative calculation. Absence of this field means that circular references result in calculation errors.",
    )
    spreadsheetTheme: SpreadsheetTheme = Field(
        ..., description="Theme applied to the spreadsheet"
    )
    importFunctionsExternalUrlAccessAllowed: bool = Field(
        ...,
        description="Whether to allow external URL access for image and import functions. Read only when true. When false, you can set to true. This value will be bypassed and always return true if the admin has enabled the allowlisting feature.",
    )


class UpdateSpreadsheetPropertiesRequest(BaseModel):
    properties: SpreadsheetProperties = Field(
        ..., description="The properties to update."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root 'properties' is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class SheetType(Enum):
    SHEET_TYPE_UNSPECIFIED = "SHEET_TYPE_UNSPECIFIED"
    GRID = "GRID"
    OBJECT = "OBJECT"
    DATA_SOURCE = "DATA_SOURCE"


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


class DataSourceColumnReference(BaseModel):
    name: str = Field(
        ...,
        description="The display name of the column. It should be unique within a data source.",
    )


class DataSourceColumn(BaseModel):
    reference: DataSourceColumnReference = Field(
        ..., description="The column reference."
    )
    formula: str = Field(..., description="The formula of the calculated column.")


class DataExecutionState(Enum):
    DATA_EXECUTION_STATE_UNSPECIFIED = "DATA_EXECUTION_STATE_UNSPECIFIED"
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    CANCELLING = "CANCELLING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class DataExecutionErrorCode(Enum):
    DATA_EXECUTION_ERROR_CODE_UNSPECIFIED = "DATA_EXECUTION_ERROR_CODE_UNSPECIFIED"
    TIMED_OUT = "TIMED_OUT"
    TOO_MANY_ROWS = "TOO_MANY_ROWS"
    TOO_MANY_COLUMNS = "TOO_MANY_COLUMNS"
    TOO_MANY_CELLS = "TOO_MANY_CELLS"
    ENGINE = "ENGINE"
    PARAMETER_INVALID = "PARAMETER_INVALID"
    UNSUPPORTED_DATA_TYPE = "UNSUPPORTED_DATA_TYPE"
    DUPLICATE_COLUMN_NAMES = "DUPLICATE_COLUMN_NAMES"
    INTERRUPTED = "INTERRUPTED"
    CONCURRENT_QUERY = "CONCURRENT_QUERY"
    OTHER = "OTHER"
    TOO_MANY_CHARS_PER_CELL = "TOO_MANY_CHARS_PER_CELL"
    DATA_NOT_FOUND = "DATA_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    MISSING_COLUMN_ALIAS = "MISSING_COLUMN_ALIAS"
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    OBJECT_IN_ERROR_STATE = "OBJECT_IN_ERROR_STATE"
    OBJECT_SPEC_INVALID = "OBJECT_SPEC_INVALID"
    DATA_EXECUTION_CANCELLED = "DATA_EXECUTION_CANCELLED"


class DataExecutionStatus(BaseModel):
    state: DataExecutionState = Field(
        ..., description="The state of the data execution."
    )
    errorCode: DataExecutionErrorCode = Field(..., description="The error code.")
    errorMessage: str = Field(..., description="The error message, which may be empty.")
    lastRefreshTime: str = Field(
        ..., description="Gets the time the data last successfully refreshed."
    )


class DataSourceSheetProperties(BaseModel):
    dataSourceId: str = Field(..., description="")
    columns: DataSourceColumn = Field(..., description="")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="")


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


class UpdateSheetPropertiesRequest(BaseModel):
    properties: SheetProperties
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root properties is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class DeveloperMetadataLocationType(Enum):
    DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED = (
        "DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED"
    )
    ROW = "ROW"
    COLUMN = "COLUMN"
    SHEET = "SHEET"
    SPREADSHEET = "SPREADSHEET"


class Dimension(Enum):
    DIMENSION_UNSPECIFIED = "DIMENSION_UNSPECIFIED"
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"


class DimensionRange(BaseModel):
    sheetId: int = Field(..., description="The sheet this span is on.")
    dimension: Dimension = Field(..., description="The dimension of the span.")
    startIndex: int = Field(
        ..., description="The start (inclusive) of the span, or not set if unbounded."
    )
    endIndex: int = Field(
        ..., description="The end (exclusive) of the span, or not set if unbounded."
    )


class DeveloperMetadataLocation(BaseModel):
    locationType: DeveloperMetadataLocationType
    spreadsheet: bool
    sheetId: int
    dimensionRange: DimensionRange


class DeveloperMetadataVisibility(Enum):
    DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED = (
        "DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED"
    )
    DOCUMENT = "DOCUMENT"
    PROJECT = "PROJECT"


class DeveloperMetadata(BaseModel):
    metadataId: int
    metadataKey: str
    metadataValue: str
    location: DeveloperMetadataLocation
    visibility: DeveloperMetadataVisibility


class DimensionProperties(BaseModel):
    hiddenByFilter: bool
    hiddenByUser: bool
    pixelSize: int
    developerMetadata: List[DeveloperMetadata]
    dataSourceColumnReference: DataSourceColumnReference


class DataSourceSheetDimensionRange(BaseModel):
    sheetId: int = Field(
        ..., description="The ID of the data source sheet the range is on."
    )
    columnReferences: List[DataSourceColumnReference] = Field(
        ..., description="The columns on the data source sheet."
    )


class UpdateDimensionPropertiesRequest(BaseModel):
    properties: DimensionProperties
    fields: str
    range: DimensionRange
    dataSourceSheetRange: DataSourceSheetDimensionRange


class GridRange(BaseModel):
    sheetId: str = Field(..., description="The sheet this range is on.")
    startRowIndex: int = Field(
        ...,
        description="The start row (inclusive) of the range, or not set if unbounded.",
    )
    endRowIndex: int = Field(
        ...,
        description="The end row (exclusive) of the range, or not set if unbounded.",
    )
    startColumnIndex: int = Field(
        ...,
        description="The start column (inclusive) of the range, or not set if unbounded.",
    )
    endColumnIndex: int = Field(
        ...,
        description="The end column (exclusive) of the range, or not set if unbounded.",
    )


class NamedRange(BaseModel):
    namedRangeId: str = Field(..., description="The ID of the named range.")
    name: str = Field(..., description="The name of the named range.")
    range: GridRange = Field(..., description="The range this represents.")


class UpdateNamedRangeRequest(BaseModel):
    namedRange: NamedRange
    fields: str


class ErrorType(Enum):
    ERROR_TYPE_UNSPECIFIED = "ERROR_TYPE_UNSPECIFIED"
    ERROR = "ERROR"
    NULL_VALUE = "NULL_VALUE"
    DIVIDE_BY_ZERO = "DIVIDE_BY_ZERO"
    VALUE = "VALUE"
    REF = "REF"
    NAME = "NAME"
    NUM = "NUM"
    N_A = "N_A"
    LOADING = "LOADING"


class ErrorValue(BaseModel):
    type: ErrorType = Field(..., description="The type of error.")
    message: str = Field(
        ...,
        description="A message with more information about the error (in the spreadsheet's locale).",
    )


class ExtendedValue(BaseModel):
    numberValue: int = Field(
        ...,
        description="Represents a double value. Note: Dates, Times and DateTimes are represented as doubles in SERIAL_NUMBER format.",
    )
    stringValue: str = Field(
        ...,
        description="Represents a string value. Leading single quotes are not included. For example, if the user typed '123 into the UI, this would be represented as a stringValue of '123'.",
    )
    boolValue: bool = Field(..., description="Represents a boolean value.")
    formulaValue: str = Field(..., description="Represents a formula.")
    errorValue: ErrorValue = Field(
        ..., description="Represents an error. This field is read-only."
    )


class TextFormatRun(BaseModel):
    startIndex: int = Field(
        ...,
        description="The zero-based character index where this run starts, in UTF-16 code units.",
    )
    format: TextFormat = Field(
        ...,
        description="The format of this run. Absent values inherit the cell's format.",
    )


class ConditionType(Enum):
    CONDITION_TYPE_UNSPECIFIED = "CONDITION_TYPE_UNSPECIFIED"
    NUMBER_GREATER = "NUMBER_GREATER"
    NUMBER_GREATER_THAN_EQ = "NUMBER_GREATER_THAN_EQ"
    NUMBER_LESS = "NUMBER_LESS"
    NUMBER_LESS_THAN_EQ = "NUMBER_LESS_THAN_EQ"
    NUMBER_EQ = "NUMBER_EQ"
    NUMBER_NOT_EQ = "NUMBER_NOT_EQ"
    NUMBER_BETWEEN = "NUMBER_BETWEEN"
    NUMBER_NOT_BETWEEN = "NUMBER_NOT_BETWEEN"
    TEXT_CONTAINS = "TEXT_CONTAINS"
    TEXT_NOT_CONTAINS = "TEXT_NOT_CONTAINS"
    TEXT_STARTS_WITH = "TEXT_STARTS_WITH"
    TEXT_ENDS_WITH = "TEXT_ENDS_WITH"
    TEXT_EQ = "TEXT_EQ"
    TEXT_IS_EMAIL = "TEXT_IS_EMAIL"
    TEXT_IS_URL = "TEXT_IS_URL"
    DATE_EQ = "DATE_EQ"
    DATE_BEFORE = "DATE_BEFORE"
    DATE_AFTER = "DATE_AFTER"
    DATE_ON_OR_BEFORE = "DATE_ON_OR_BEFORE"
    DATE_ON_OR_AFTER = "DATE_ON_OR_AFTER"
    DATE_BETWEEN = "DATE_BETWEEN"
    DATE_NOT_BETWEEN = "DATE_NOT_BETWEEN"
    DATE_IS_VALID = "DATE_IS_VALID"
    ONE_OF_RANGE = "ONE_OF_RANGE"
    ONE_OF_LIST = "ONE_OF_LIST"
    BLANK = "BLANK"
    NOT_BLANK = "NOT_BLANK"
    CUSTOM_FORMULA = "CUSTOM_FORMULA"
    BOOLEAN = "BOOLEAN"
    TEXT_NOT_EQ = "TEXT_NOT_EQ"
    DATE_NOT_EQ = "DATE_NOT_EQ"
    FILTER_EXPRESSION = "FILTER_EXPRESSION"


class RelativeDate(Enum):
    RELATIVE_DATE_UNSPECIFIED = "RELATIVE_DATE_UNSPECIFIED"
    PAST_YEAR = "PAST_YEAR"
    PAST_MONTH = "PAST_MONTH"
    PAST_WEEK = "PAST_WEEK"
    YESTERDAY = "YESTERDAY"
    TODAY = "TODAY"
    TOMORROW = "TOMORROW"


class ConditionValue(BaseModel):
    relativeDate: RelativeDate
    userEnteredValue: str


class BooleanCondition(BaseModel):
    type: ConditionType
    values: ConditionValue


class DataValidationRule(BaseModel):
    condition: BooleanCondition
    inputMessage: str
    strict: bool
    showCustomUi: bool


class PivotGroupValueMetadata(BaseModel):
    value: ExtendedValue = Field(
        ...,
        description="The calculated value the metadata corresponds to. (Note that formulaValue is not valid, because the values will be calculated.)",
    )
    collapsed: bool = Field(
        ..., description="True if the data corresponding to the value is collapsed."
    )


class SortOrder(BaseModel):
    pass


class PivotGroupSortValueBucket(BaseModel):
    valuesIndex: int = Field(
        ...,
        description="The offset in the PivotTable.values list which the values in this grouping should be sorted by.",
    )
    buckets: List[ExtendedValue] = Field(
        ...,
        description="Determines the bucket from which values are chosen to sort. For example, in a pivot table with one row group & two column groups, the row group can list up to two values. The first value corresponds to a value within the first column group, and the second value corresponds to a value in the second column group. If no values are listed, this would indicate that the row should be sorted according to the 'Grand Total' over the column groups. If a single value is listed, this would correspond to using the 'Total' of that bucket.",
    )


class ManualRuleGroup(BaseModel):
    groupName: ExtendedValue = Field(
        ...,
        description="The group name, which must be a string. Each group in a given ManualRule must have a unique group name.",
    )
    items: List[ExtendedValue] = Field(
        ...,
        description="The items in the source data that should be placed into this group. Each item may be a string, number, or boolean. Items may appear in at most one group within a given ManualRule. Items that do not appear in any group will appear on their own",
    )


class ManualRule(BaseModel):
    groups: List[ManualRuleGroup]


class HistogramRule(BaseModel):
    interval: str = Field(
        ..., description="The size of the buckets that are created. Must be positive."
    )
    start: Optional[int] = Field(
        ...,
        description="The minimum value at which items are placed into buckets of constant size. Values below start are lumped into a single bucket. This field is optional.",
    )
    end: Optional[int] = Field(
        ...,
        description="The maximum value at which items are placed into buckets of constant size. Values above end are lumped into a single bucket. This field is optional.",
    )

class DateTimeRuleType(Enum):
    DATE_TIME_RULE_TYPE_UNSPECIFIED = "DATE_TIME_RULE_TYPE_UNSPECIFIED"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    HOUR_MINUTE = "HOUR_MINUTE"
    HOUR_MINUTE_AMPM = "HOUR_MINUTE_AMPM"
    DAY_OF_WEEK = "DAY_OF_WEEK"
    DAY_OF_YEAR = "DAY_OF_YEAR"
    DAY_OF_MONTH = "DAY_OF_MONTH"
    DAY_MONTH = "DAY_MONTH"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"
    YEAR_MONTH = "YEAR_MONTH"
    YEAR_QUARTER = "YEAR_QUARTER"
    YEAR_MONTH_DAY = "YEAR_MONTH_DAY"

class DateTimeRule(BaseModel):
    type: DateTimeRuleType


class PivotGroupRule(BaseModel):
    manualRule: ManualRule
    histogramRule: HistogramRule
    dateTimeRule: DateTimeRule


class PivotGroupLimit(BaseModel):
    countLimit: int
    applyOrder: int


class PivotGroup(BaseModel):
    showTotals: bool
    valueMetadata: PivotGroupValueMetadata
    sortOrder: SortOrder
    valueBucket: PivotGroupSortValueBucket
    repeatHeadings: boolean
    label: str
    groupRule: PivotGroupRule
    groupLimit: PivotGroupLimit
    sourceColumnOffset: int
    dataSourceColumnReference: DataSourceColumnReference


class PivotFilterCriteria(BaseModel):
    visibleValues: List[str]
    condition: BooleanCondition
    visibileByDefault: bool


class PivotFilterSpec(BaseModel):
    filterCriteria: PivotFilterCriteria
    columnOffsetIndex: int
    dataSourceColumnReference: DataSourceColumnReference

class PivotValueSummarizeFunction(Enum):
    PIVOT_STANDARD_VALUE_FUNCTION_UNSPECIFIED = "PIVOT_STANDARD_VALUE_FUNCTION_UNSPECIFIED"
    SUM = "SUM"
    COUNTA = "COUNTA"
    COUNT = "COUNT"
    COUNTUNIQUE = "COUNTUNIQUE"
    AVERAGE = "AVERAGE"
    MAX = "MAX"
    MIN = "MIN"
    MEDIAN = "MEDIAN"
    PRODUCT = "PRODUCT"
    STDEV = "STDEV"
    STDEVP = "STDEVP"
    VAR = "VAR"
    VARP = "VARP"
    CUSTOM = "CUSTOM"
    NONE = "NONE"

class PivotValueCalculatedDisplayType(Enum):
    PIVOT_VALUE_CALCULATED_DISPLAY_TYPE_UNSPECIFIED = "PIVOT_VALUE_CALCULATED_DISPLAY_TYPE_UNSPECIFIED"
    PERCENT_OF_ROW_TOTAL = "PERCENT_OF_ROW_TOTAL"
    PERCENT_OF_COLUMN_TOTAL = "PERCENT_OF_COLUMN_TOTAL"
    PERCENT_OF_GRAND_TOTAL = "PERCENT_OF_GRAND_TOTAL"

class PivotValue(BaseModel):
    summarizeFunction: PivotValueSummarizeFunction
    name: str
    calculatedDisplayType: PivotValueCalculatedDisplayType
    sourceColumnOffset: int
    formula: str
    dataSourceColumnReference: DataSourceColumnReference


class PivotValueLayout(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"


class PivotTable(BaseModel):
    rows: List[PivotGroup]
    columns: List[PivotGroup]
    criteria: Dict[int, PivotFilterCriteria]
    filterSpecs: List[PivotFilterSpec]
    values: List[PivotValue]
    valueLayout: PivotValueLayout
    dataExecutionStatus: DataExecutionStatus
    source: GridRange
    dataSourceId: str

class DataSourceTableColumnSelectionType(Enum):
    DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED = "DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED"
    SELECTED = "SELECTED"
    SYNC_ALL = "SYNC_ALL"

class FilterCriteria(BaseModel):
    hiddenValues: List[str]
    condition: BooleanCondition
    visibleBackgroundColor: Color
    visibleBackgroundcolorStyle: ColorStyle
    visibleForegroundColor: Color
    visibleForegroundColorStyle: ColorStyle

class FilterSpec(BaseModel):
    filterCriteria = FilterCriteria
    columnIndex: int
    dataSourceColumnReference: DataSourceColumnReference

class SortSpec(BaseModel):
    sortOrder: SortOrder
    foregroundColor: Color
    foregroundColorStyle: ColorStyle
    backgroundColor: Color
    backgroundColorStyle: ColorStyle
    dimensionIndex: int
    dataSourceColumnReference: DataSourceColumnReference


class DataSourceTable(BaseModel):
    dataSourceId: str
    columnSelectionType: DataSourceTableColumnSelectionType
    columns: List[DataSourceColumnReference]
    filterSpecs: List[FilterSpec]
    sortSpec: List[SortSpec]
    rowLimit: int
    dataExecutionStatus: DataExecutionStatus


class DataSourceFormula(BaseModel):
    dataSourceId: str
    dataExecutionStatus: DataExecutionStatus

class DisplayFormat(Enum):
    DISPLAY_FORMAT_UNSPECIFIED = "DISPLAY_FORMAT_UNSPECIFIED"
    DEFAULT = "DEFAULT"
    LAST_NAME_COMMA_FIRST_NAME = "LAST_NAME_COMMA_FIRST_NAME"
    EMAIL = "EMAIL"

class PersonProperties(BaseModel):
    email: str
    displayFormat: DisplayFormat

class RichLinkProperties(BaseModel):
    uri: str
    mimeType: str

class Chip(BaseModel):
    personProperties: PersonProperties
    richLinkProperties: RichLinkProperties

class ChipRun(BaseModel):
    startIndex: int
    chip: Chip


class CellData:
    userEnteredValued: ExtendedValue
    effectiveValue: ExtendedValue
    formattedValue: str
    userEnteredFormat: CellFormat
    effectiveFormat: CellFormat
    hyperlink: str
    note: str
    textFormatRuns: TextFormatRun
    dataValidation: DataValidationRule
    pivotTable: PivotTable
    dataSourceTable: DataSourceTable
    dataSourceFormula: DataSourceFormula
    chipRuns: List[ChipRun]


class RepeatCellRequest(BaseModel):
    range: GridRange
    cell: CellData
    fields: str


class AddNamedRangeRequest(BaseModel):
    namedRange: NamedRange


class DeleteNamedRangeRequest(BaseModel):
    namedRangeId: str


class AddSheetRequest(BaseModel):
    properties: SheetProperties


class DeleteSheetRequest(BaseModel):
    sheetId: int

class SourceAndDestination(BaseModel):
    source: GridRange
    dimension: Dimension
    fillLength: int

class AutoFillRequest(BaseModel):
    useAlternateSeries: bool
    range: GridRange
    sourceAndDestination: SourceAndDestination

class GridCoordinate(BaseModel):
    sheetId: int
    rowIndex: int
    columnIndex: int

class PasteType(Enum):
    PASTE_NORMAL = "PASTE_NORMAL"
    PASTE_VALUES = "PASTE_VALUES"
    PASTE_FORMAT = "PASTE_FORMAT"
    PASTE_NO_BORDERS = "PASTE_NO_BORDERS"
    PASTE_FORMULA = "PASTE_FORMULA"
    PASTE_DATA_VALIDATION = "PASTE_DATA_VALIDATION"
    PASTE_CONDITIONAL_FORMATTING = "PASTE_CONDITIONAL_FORMATTING"

class CutPasteRequest(BaseModel):
    source: GridRange
    destination: GridCoordinate
    pasteType: PasteType

class PasteOrientation(Enum):
    NORMAL = "NORMAL"
    TRANSPOSE = "TRANSPOSE"

class CopyPasteRequest(BaseModel):
    source: GridRange
    destination: GridRange
    pasteType: PasteType
    pasteOrientation: PasteOrientation

class MergeType(Enum):
    MERGE_ALL = "MERGE_ALL"
    MERGE_COLUMNS = "MERGE_COLUMNS"
    MERGE_ROWS = "MERGE_ROWS"

class MergeCellsRequest(BaseModel):
    range: GridRange
    mergeType: MergeType


class UnmergeCellsRequest(BaseModel):
    range: GridRange


class UpdateBordersRequest(BaseModel):
    range: GridRange
    top: Border
    bottom: Border
    left: Border
    right: Border
    innerHorizontal: Border
    innerVertical: Border

class RowData(BaseModel):
    values: List[CellData]

class UpdateCellsRequest(BaseModel):
    rows: List[RowData]
    fields: str
    start: GridCoordinate
    range: GridRange

class FilterView(BaseModel):
    filterViewId: int
    title: str
    range: GridRange
    namedRangeId: str
    tableId: str
    sortSpecs: List[SortSpec]
    criteria: Dict[int, FilterCriteria]
    filterSpecs: List[FilterSpec]

class AddFilterViewRequest(BaseModel):
    filter: FilterView


class AppendCellsRequest(BaseModel):
    sheetId: int
    rows: List[RowData]
    fields: str
    tableId: str

class ClearBasicFilterRequest(BaseModel):
    sheetId: int

class DeleteDimensionRequest(BaseModel):
    range: DimensionRange


class DeleteEmbeddedObjectRequest(BaseModel):
    objectId: int

class DeleteFilterViewRequest(BaseModel):
    filterId: int


class DuplicateFilterViewRequest(BaseModel):
    filterId: int


class DuplicateSheetRequest(BaseModel):
    sourceSheetId: int
    insertSheetId: int
    newSheetId: int
    newSheetName: str


class FindReplaceRequest(BaseModel):
    find: str
    replacement: str
    matchCase: bool
    matchEntireCell: bool
    searchByRegex: bool
    includeFormulas: bool
    range: GridRange
    sheetId: int
    allSheets: bool


class InsertDimensionRequest(BaseModel):
    range: DimensionRange
    inheritFromBefore: bool


class InsertRangeRequest(BaseModel):
    range: GridRange
    shiftDimension: Dimension


class MoveDimensionRequest(BaseModel):
    source: DimensionRange
    destinationIndex: int

class OverlayPosition(BaseModel):
    anchorCell: GridCoordinate
    offsetXPixels: int
    offsetYPixels: int
    widthPixels: int
    heightPixels: int

class EmbeddedObjectPosition(BaseModel):
    sheetId: int
    overlayPosition: OverlayPosition
    newSheet: bool

class UpdateEmbeddedObjectPositionRequest(BaseModel):
    objectId: int
    newPosition: EmbeddedObjectPosition
    fields: str


class PasteDataRequest(BaseModel):
    coordinate: GridCoordinate
    data: str
    type: PasteType
    delimiter: str
    html: bool

class DelimiterType(Enum):
    DELIMITER_TYPE_UNSPECIFIED = "DELIMITER_TYPE_UNSPECIFIED"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    PERIOD = "PERIOD"
    SPACE = "SPACE"
    CUSTOM = "CUSTOM"
    AUTODETECT = "AUTODETECT"

class TextToColumnsRequest(BaseModel):
    source: GridRange
    delimiter: str
    delimiterType: DelimiterType


class UpdateFilterViewRequest(BaseModel):
    filter: FilterView
    fields: str


class DeleteRangeRequest(BaseModel):
    range: GridRange
    shiftDimension: Dimension


class AppendDimensionRequest(BaseModel):
    sheetId: int
    dimension: Dimension
    length: int

class BooleanRule(BaseModel):
    condition: BooleanCondition
    format: CellFormat

class InterpolationPointType(Enum):
    INTERPOLATION_POINT_TYPE_UNSPECIFIED = "INTERPOLATION_POINT_TYPE_UNSPECIFIED"
    MIN = "MIN"
    MAX = "MAX"
    NUMBER = "NUMBER"
    PERCENT = "PERCENT"
    PERCENTILE = "PERCENTILE"

class InterpolationPoint(BaseModel):
    color: Color
    colorStyle: ColorStyle
    type: InterpolationPointType
    value: str

class GradientRule(BaseModel):
    minpoint: InterpolationPoint
    midpoint: InterpolationPoint
    maxpoint: InterpolationPoint

class ConditionalFormatRule(BaseModel):
    ranges: List[GridRange]
    booleanRule: BooleanRule
    gradientRule: GradientRule


class AddConditionalFormatRuleRequest(BaseModel):
    rule: ConditionalFormatRule
    index: int


class UpdateConditionalFormatRuleRequest(BaseModel):
    index: int
    sheetId: int
    rule: ConditionalFormatRule
    newIndex: int

class DeleteConditionalFormatRuleRequest(BaseModel):
    index: int
    sheetId: int


class SortRangeRequest(BaseModel):
    range: GridRange
    sortSpecs: List[SortSpec]


class SetDataValidationRequest(BaseModel):
    range: GridRange
    rule: DataValidationRule
    filteredRowsIncluded: bool

class BasicFilter(BaseModel):
    range: GridRange
    tableid: str
    sortSpecs: List[SortSpec]
    criteria: Dict[int, FilterCriteria]
    filterSpecs: List[FilterSpec]

class SetBasicFilterRequest(BaseModel):
    filter: BasicFilter

class Editors(BaseModel):
    users: List[str]
    groups: List[str]
    domainUsersCanEdit: bool

class ProtectedRange(BaseModel):
    protectedRangeId: int
    range: GridRange
    namedRangeId: str
    tableId: str
    description: str
    warningOnly: bool
    requestingUserCanEdit: bool
    unprotectedRanges: List[GridRange]
    editors: Editors

class AddProtectedRangeRequest(BaseModel):
    protectedRange: ProtectedRange


class UpdateProtectedRangeRequest(BaseModel):
    protectedRange: ProtectedRange
    fields: str


class DeleteProtectedRangeRequest(BaseModel):
    protectedRangeId: int


class AutoResizeDimensionsRequest(BaseModel):
    dimensions: DimensionRange
    dataSourceSheetDimensions: DataSourceSheetDimensionRange

class TextPosition(BaseModel):
    horizontalAlignment: HorizontalAlign

class DataSourceChartProperties(BaseModel):
    dataSourceId: str
    dataExecutionStatus: DataExecutionStatus

class ChartHiddenDimensionStrategy(Enum):
    CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED = "CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED"
    SKIP_HIDDEN_ROWS_AND_COLUMNS = "SKIP_HIDDEN_ROWS_AND_COLUMNS"
    SKIP_HIDDEN_ROWS = "SKIP_HIDDEN_ROWS"
    SKIP_HIDDEN_COLUMNS = "SKIP_HIDDEN_COLUMNS"
    SHOW_ALL = "SHOW_ALL"

class BasicChartType(Enum):
    BASIC_CHART_TYPE_UNSPECIFIED = "BASIC_CHART_TYPE_UNSPECIFIED"
    BAR = "BAR"
    LINE = "LINE"
    AREA = "AREA"
    COLUMN = "COLUMN"
    SCATTER = "SCATTER"
    COMBO = "COMBO"
    STEPPED_AREA = "STEPPED_AREA"

class BasicChartLegendPosition(Enum):
    BASIC_CHART_LEGEND_POSITION_UNSPECIFIED = "BASIC_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"

class BasicChartAxisPosition(Enum):
    BASIC_CHART_AXIS_POSITION_UNSPECIFIED = "BASIC_CHART_AXIS_POSITION_UNSPECIFIED"
    BOTTOM_AXIS = "BOTTOM_AXIS"
    LEFT_AXIS = "LEFT_AXIS"
    RIGHT_AXIS = "RIGHT_AXIS"

class ViewWindowMode(Enum):
    DEFAULT_VIEW_WINDOW_MODE = "DEFAULT_VIEW_WINDOW_MODE"
    VIEW_WINDOW_MODE_UNSUPPORTED = "VIEW_WINDOW_MODE_UNSUPPORTED"
    EXPLICIT = "EXPLICIT"
    PRETTY = "PRETTY"


class ChartAxisViewWindowOptions(BaseModel):
    viewWindowMin: int
    viewWindowMax: int
    viewWindowMode: ViewWindowMode

class BasicChartAxis(BaseModel):
    position: BasicChartAxisPosition
    title: str
    format: TextFormat
    titleTextPosition: TextPosition
    viewWindowOptions: ChartAxisViewWindowOptions

class ChartDateTimeRuleType(Enum):
    CHART_DATE_TIME_RULE_TYPE_UNSPECIFIED = "CHART_DATE_TIME_RULE_TYPE_UNSPECIFIED"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    HOUR_MINUTE = "HOUR_MINUTE"
    HOUR_MINUTE_AMPM = "HOUR_MINUTE_AMPM"
    DAY_OF_WEEK = "DAY_OF_WEEK"
    DAY_OF_YEAR = "DAY_OF_YEAR"
    DAY_OF_MONTH = "DAY_OF_MONTH"
    DAY_MONTH = "DAY_MONTH"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"
    YEAR_MONTH = "YEAR_MONTH"
    YEAR_QUARTER = "YEAR_QUARTER"
    YEAR_MONTH_DAY = "YEAR_MONTH_DAY"

class ChartDateTimeRule(BaseModel):
    type: ChartDateTimeRuleType

class ChartHistogramRule(BaseModel):
    minValue: int
    maxValue: int
    intervalSize: int

class ChartGroupRule(BaseModel):
    dateTimeRule: ChartDateTimeRule
    histogramRule: ChartHistogramRule

class ChartAggregateType(Enum):
    CHART_AGGREGATE_TYPE_UNSPECIFIED = "CHART_AGGREGATE_TYPE_UNSPECIFIED"
    AVERAGE = "AVERAGE"
    COUNT = "COUNT"
    MAX = "MAX"
    MEDIAN = "MEDIAN"
    MIN = "MIN"
    SUM = "SUM"

class ChartSourceRange(BaseModel):
    sources: List[GridRange]

class ChartData(BaseModel):
    groupRule: ChartGroupRule
    aggregateType: ChartAggregateType
    sourceRange: ChartSourceRange
    columnReference: DataSourceColumnReference

class BasicChartDomain(BaseModel):
    domain: ChartData
    reversed: bool

class LineDashType(Enum):
    LINE_DASH_TYPE_UNSPECIFIED = "LINE_DASH_TYPE_UNSPECIFIED"
    INVISIBLE = "INVISIBLE"
    CUSTOM = "CUSTOM"
    SOLID = "SOLID"
    DOTTED = "DOTTED"
    MEDIUM_BASED = "MEDIUM_BASED"
    MEDIUM_DASHED_DOTTED = "MEDIUM_DASHED_DOTTED"
    LONG_DASHED = "LONG_DASHED"
    LONG_DASHED_DOTTED = "LONG_DASH_DOTTED"

class LineStyle(BaseModel):
    width: int
    type: LineDashType

class DataLabelType(BaseModel):
    DATA_LABEL_TYPE_UNSPECIFIED = "DATA_LABEL_TYPE_UNSPECIFIED"
    NONE = "NONE"
    DATA = "DATA"
    CUSTOM = "CUSTOM"

class DataLabelPlacement(BaseModel):
    DATA_LABEL_PLACEMENT_UNSPECIFIED = "DATA_LABEL_PLACEMENT_UNSPECIFIED"
    CENTER = "CENTER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ABOVE = "ABOVE"
    BELOW = "BELOW"
    INSIDE_END = "INSIDE_END"
    INSIDE_BASE = "INSIDE_BASE"
    OUTSIDE_END = "OUTSIDE_END"

class DataLabel(BaseModel):
    type: DataLabelType
    textFormat: TextFormat
    placement: DataLabelPlacement
    customLabelData: ChartData

class PointShape(Enum):
    POINT_SHAPE_UNSPECIFIED = "POINT_SHAPE_UNSPECIFIED"
    CIRCLE = "CIRCLE"
    DIAMOND = "DIAMOND"
    HEXAGON = "HEXAGON"
    PENTAGON = "PENTAGON"
    SQUARE = "SQUARE"
    STAR = "STAR"
    TRIANGLE = "TRIANGLE"
    X_MARK = "X_MARK"

class PointStyle(BaseModel):
    size: int
    shape: PointShape

class BasicSeriesDataPointStyleOverride(BaseModel):
    index: int
    colorStyle: ColorStyle
    pointStyle: PointStyle

class BasicChartSeries(BaseModel):
    series: ChartData
    targetAxis: BasicChartAxisPosition
    type: BasicChartType
    lineStyle: LineStyle
    dataLabel: DataLabel
    color: Color
    colorStyle: ColorStyle
    pointStyle: PointStyle
    styleOverrides: List[BasicSeriesDataPointStyleOverride]

class BasicChartStackedType(Enum):
    BASIC_CHART_STACKED_TYPE_UNSPECIFIED = "BASIC_CHART_STACKED_TYPE_UNSPECIFIED"
    NOT_STACKED = "NOT_STACKED"
    STACKED = "STACKED"
    PERCENT_STACKED = "PERCENT_STACKED"

class BasicChartCompareMode(Enum):
    BASIC_CHART_COMPARE_MODE_UNSPECIFIED = "BASIC_CHART_COMPARE_MODE_UNSPECIFIED"
    DATUM = "DATUM"
    CATEGORY = "CATEGORY"

class BasicChartSpec(BaseModel):
    chartType: BasicChartType
    legendPosition: BasicChartLegendPosition
    axis: List[BasicChartAxis]
    domains: List[BasicChartDomain]
    series: List[BasicChartSeries]
    headerCount: int
    threeDimensional: bool
    interpolateNulls: bool
    stackedType: BasicChartStackedType
    lineSmoothing: bool
    compareMode: BasicChartCompareMode
    totalDataLabel: DataLabel

class PieChartLegendPosition(Enum):
    PIE_CHART_LEGEND_POSITION_UNSPECIFIED = "PIE_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    LABELED_LEGEND = "LABELED_LEGEND"

class PieChartSpec(BaseModel):
    legendPosition: PieChartLegendPosition
    domain: ChartData
    series: ChartData
    threeDimensional: bool
    pieHole: int

class BubbleChartLegendPosition(Enum):
    BUBBLE_CHART_LEGEND_POSITION_UNSPECIFIED = "BUBBLE_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    INSIDE_LEGEND = "INSIDE_LEGEND"

class BubbleChartSpec(BaseModel):
    legendPosition: BubbleChartLegendPosition
    bubbleLabels: ChartData
    domain: ChartData
    series: ChartData
    groupIds: ChartData
    bubbleSizes: ChartData
    bubbleOpacity: int
    bubbleBorderColorStyle: ColorStyle
    bubbleMaxRadiusSize: int
    bubbleMinRadiusSize: int
    bubbleTextStyle: TextFormat

class CandleStickDomain(BaseModel):
    data: ChartData
    reversed: bool

class CandlestickSeries:
    data: ChartData

class CandleStickData(BaseModel):
    lowSeries: CandlestickSeries
    openSeries: CandlestickSeries
    closeSeries: CandlestickSeries
    highSeries: CandlestickSeries

class CandleStickChartSpec(BaseModel):
    domain: CandleStickDomain
    data: CandleStickData

class OrgChartNodeSize(Enum):
    ORG_CHART_LABEL_SIZE_UNSPECIFIED = "ORG_CHART_LABEL_SIZE_UNSPECIFIED"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class OrgChartSpec(BaseModel):
    nodeSize: OrgChartNodeSize
    nodeColorStyle: ColorStyle
    selectedNodeColorStyle: ColorStyle
    labels: ChartData
    parentLabels: ChartData
    tooltips: ChartData

class HistogramSeries(BaseModel):
    barColorStyle: ColorStyle
    data: ChartData

class HistogramChartLegendPosition(Enum):
    HISTOGRAM_CHART_LEGEND_POSITION_UNSPECIFIED = "HISTOGRAM_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    INSIDE_LEGEND = "INSIDE_LEGEND"

class HistogramChartSpec(BaseModel):
    series: List[HistogramSeries]
    legendPosition: HistogramChartLegendPosition
    showItemDividers: bool
    bucketSize: int
    outlierPercentile: int

class WaterfallChartDomain(BaseModel):
    data: ChartData
    reversed: bool

class WaterfallChartColumnStyle(BaseModel):
    label: str
    colorStyle: ColorStyle

class WaterfallChartCustomSubtotal(BaseModel):
    subtotalIndex: int
    label: str
    dataIsSubtotal: bool

class WaterfallChartSeries(BaseModel):
    data: ChartData
    positiveColumnsStyle: WaterfallChartColumnStyle
    negativeColumnsStyle: WaterfallChartColumnStyle
    subtotalColumnsStyle: WaterfallChartColumnStyle
    hideTrailingSubtotal: bool
    customSubtotals: List[WaterfallChartCustomSubtotal]
    dataLabel: DataLabel

class WaterfallChartStackedType(Enum):
    WATERFALL_STACKED_TYPE_UNSPECIFIED = "WATERFALL_STACKED_TYPE_UNSPECIFIED"
    STACKED = "STACKED"
    SEQUENTIAL = "SEQUENTIAL"

class WaterfallChartSpec(BaseModel):
    domain: WaterfallChartDomain
    series: WaterfallChartSeries
    stackedType: WaterfallChartStackedType
    firstValueIsTotal: bool
    hideConnectorLines: bool
    connectorLineStyle: LineStyle
    totalDataLabel: DataLabel

class TreemapChartColorScale(BaseModel):
    minValueColorStyle: ColorStyle
    midValueColorStyle: ColorStyle
    maxValueColorStyle: ColorStyle
    noDataColorStyle: ColorStyle

class TreemapChartSpec(BaseModel):
    labels: ChartData
    parentLabels: ChartData
    sizeData: ChartData
    colorData: ChartData
    textFormat: TextFormat
    levels: int
    hintedLevels: int
    minValue: int
    maxValue: int
    headerColor: Color
    headerColorStyle: ColorStyle
    colorScale: TreemapChartColorScale
    hideToolTips: bool

class KeyValueFormat(BaseModel):
    textFormat: TextFormat
    position: TextPosition

class ComparisonType(Enum):
    COMPARISON_TYPE_UNDEFINED = "COMPARISON_TYPE_UNDEFINED"
    ABSOLUTE_DIFFERENCE = "ABSOLUTE_DIFFERENCE"
    PERCENTAGE_DIFFERENCE = "PERCENTAGE_DIFFERENCE"

class BaselineValueFormat(BaseModel):
    comparisonType: ComparisonType
    textFormat: TextFormat
    position: TextPosition
    description: str
    positiveColorStyle: ColorStyle
    negativeColorStyle: ColorStyle

class ChartNumberFormatSource(Enum):
    CHART_NUMBER_FORMAT_SOURCE_UNDEFINED = "CHART_NUMBER_FORMAT_SOURCE_UNDEFINED"
    FROM_DATA = "FROM_DATA"
    CUSTOM = "CUSTOM"

class ChartCustomNumberFormatOptions(Enum):
    prefix: str
    suffix: str

class ScorecardChartSpec(BaseModel):
    keyValueData: ChartData
    baselineValueData: ChartData
    aggregateType: ChartAggregateType
    keyValueFormat: KeyValueFormat
    baselineValueFormat: BaselineValueFormat
    scaleFactor: int
    numberFormatSource: ChartNumberFormatSource
    customFormatOptions: ChartCustomNumberFormatOptions

class ChartSpec(BaseModel):
    title: str
    altText: str
    titleTextFormat: TextFormat
    titleTextPosition: TextPosition
    subtitle: str
    subtitleTextFormat: TextFormat
    subtitleTextPosition: TextPosition
    fontName: str
    maximized: bool
    backgroundColor: Color
    backgroundColorStyle: ColorStyle
    dataSourceChartProperties: DataSourceChartProperties
    filterSpecs: List[FilterSpec]
    sortSpecs: List[SortSpec]
    hiddenDimensionStrategy: ChartHiddenDimensionStrategy
    basicChart: BasicChartSpec
    pieChart: PieChartSpec
    bubbleChart: BubbleChartSpec
    candlestickChart: CandleStickChartSpec
    orgChart: OrgChartSpec
    histogramChart: HistogramChartSpec
    waterfallChart: WaterfallChartSpec
    treemapChart: TreemapChartSpec
    scorecardChart: ScorecardChartSpec


class EmbeddedObjectBorder(BaseModel):
    colorStyle: ColorStyle

class EmbeddedChart(BaseModel):
    chartId: int
    spec: ChartSpec
    position: EmbeddedObjectPosition
    border: EmbeddedObjectBorder


class AddChartRequest(BaseModel):
    chart: EmbeddedChart


class UpdateChartSpecRequest(BaseModel):
    chartId: int
    spec: ChartSpec

class BandingProperties(BaseModel):
    headerColorStyle: ColorStyle
    firstBandColorStyle: ColorStyle
    secondBandColorStyle: ColorStyle
    footerColorStyle: ColorStyle

class BandedRange(BaseModel):
    bandedRangeId: int
    bandedRangeReference: str
    range: GridRange
    rowProperties: BandingProperties
    columnProperties: BandingProperties

class UpdateBandingRequest(BaseModel):
    bandedRange: BandedRange
    fields: str

class AddBandingRequest(BaseModel):
    bandedRange: BandedRange


class DeleteBandingRequest(BaseModel):
    bandedRangeId: int


class CreateDeveloperMetadataRequest(BaseModel):
    developerMetadata: DeveloperMetadata

class DeveloperMetadataLocationMatchingStrategy(Enum):
    DEVELOPER_METADATA_LOCATION_MATCHING_STRATEGY_UNSPECIFIED = "DEVELOPER_METADATA_LOCATION_MATCHING_STRATEGY_UNSPECIFIED"
    EXACT_LOCATION = "EXACT_LOCATION"
    INTERSECTING_LOCATION = "INTERSECTING_LOCATION"

class DeveloperMetadataLookup(BaseModel):
    locationType: DeveloperMetadataLocationType
    metadataLocation: DeveloperMetadataLocation
    locationMatchingStrategy: DeveloperMetadataLocationMatchingStrategy
    metadataId: int
    metadataKey: str
    metadataValue: str
    visibility: DeveloperMetadataVisibility

class DataFilter(BaseModel):
    developerMetadataLookup: DeveloperMetadataLookup
    a1Range: str
    gridRange: GridRange

class UpdateDeveloperMetadataRequest(BaseModel):
    dataFilters: List[DataFilter]
    developerMetadata: DeveloperMetadata
    fields: str


class DeleteDeveloperMetadataRequest(BaseModel):
    dataFilter: DataFilter


class RandomizeRangeRequest(BaseModel):
    range: GridRange


class AddDimensionGroupRequest(BaseModel):
    range: DimensionRange


class DeleteDimensionGroupRequest(BaseModel):
    range: DimensionRange

class DimensionGroup(BaseModel):
    range: DimensionRange
    depth: int
    collapsed: bool

class UpdateDimensionGroupRequest(BaseModel):
    dimensionGroup: DimensionGroup
    fields: str

class TrimWhitespaceRequest(BaseModel):
    range: GridRange


class DeleteDuplicatesRequest(BaseModel):
    range: GridRange
    comparisonColumns: List[DimensionRange]


class UpdateEmbeddedObjectBorderRequest(BaseModel):
    objectId: int
    border: EmbeddedObjectBorder
    fields: str

class SlicerSpec(BaseModel):
    dataRange: GridRange
    filterCriteria: FilterCriteria
    columnIndex: int
    applyToPivotTables: bool
    title: str
    textFormat: TextFormat
    backgroundColorStyle: ColorStyle
    horizontalAlignment: HorizontalAlign

class Slicer(BaseModel):
    slicerId: int
    spec: SlicerSpec
    position: EmbeddedObjectPosition

class AddSlicerRequest(BaseModel):
    slicer: Slicer


class UpdateSlicerSpecRequest(BaseModel):
    slicerId: int
    spec: SlicerSpec
    fields: str

class DataSourceParameter(BaseModel):
    name: str
    namedRangeId: str
    range: GridRange

class BigQueryQuerySpec(BaseModel):
    rawQuery: str

class BigQueryTableSpec(BaseModel):
    tableProjectId: str
    tableId: str
    datasetId: str

class BigQueryDataSourceSpec(BaseModel):
    projectId: str
    querySpec: BigQueryQuerySpec
    tableSpec: BigQueryTableSpec

class LookerDataSourceSpec(BaseModel):
    instanceUri: str
    model: str
    explore: str

class DataSourceSpec(BaseModel):
    parameters: DataSourceParameter
    bigQuery: BigQueryDataSourceSpec
    looker: LookerDataSourceSpec

class DataSource(BaseModel):
    dataSourceId: str
    spec: DataSourceSpec
    calculatedColumns: DataSourceColumn
    sheetId: int

class AddDataSourceRequest(BaseModel):
    dataSource: DataSource


class UpdateDataSourceRequest(BaseModel):
    dataSource: DataSource
    fields: str


class DeleteDataSourceRequest(BaseModel):
    dataSourceId: str

class DataSourceObjectReference(BaseModel):
    sheetId: str
    chartId: int
    dataSourceTableAnchorCell: GridCoordinate
    dataSourcePivotTableAnchorCell: GridCoordinate
    dataSourceFormulaCell: GridCoordinate

class DataSourceObjectReferences(BaseModel):
    references: List[DataSourceObjectReference]

class RefreshDataSourceRequest(BaseModel):
    force: bool
    references: DataSourceObjectReferences


class CancelDataSourceRefreshRequest(BaseModel):
    references: DataSourceObjectReferences
    dataSourceId: str
    isAll: bool

class TableRowsProperties(BaseModel):
    headerColorStyle: ColorStyle
    firstBandColorStyle: ColorStyle
    secondBandColorStyle: ColorStyle
    footerColorStyle: ColorStyle

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
    condition: BooleanCondition

class TableColumnProperties(BaseModel):
    columnIndex: int
    columnName: str
    columnType: ColumnType
    dataValidationRule: TableColumnDataValidationRule

class Table(BaseModel):
    tableId: str
    name: str
    range: GridRange
    rowsProperties: TableRowsProperties
    columnProperties: List[TableColumnProperties]

class AddTableRequest(BaseModel):
    table: Table


class UpdateTableRequest(BaseModel):
    table: Table
    fields: str


class DeleteTableRequest(BaseModel):
    tableId: str

class Request(BaseModel):
    updateSpreadsheetProperties: UpdateSpreadsheetPropertiesRequest
    updateSheetProperties: UpdateSheetPropertiesRequest
    updateDimensionProperties: UpdateDimensionPropertiesRequest
    updateNamedRange: UpdateNamedRangeRequest
    repeatCell: RepeatCellRequest
    addNamedRange: AddNamedRangeRequest
    deleteNamedRange: DeleteNamedRangeRequest
    addSheet: AddSheetRequest
    deleteSheet: DeleteSheetRequest
    autoFill: AutoFillRequest
    cutPaste: CutPasteRequest
    copyPaste: CopyPasteRequest
    mergeCells: MergeCellsRequest
    unmergeCells: UnmergeCellsRequest
    updateBorders: UpdateBordersRequest
    updateCells: UpdateCellsRequest
    addFilterView: AddFilterViewRequest
    appendCells: AppendCellsRequest
    clearBasicFilter: ClearBasicFilterRequest
    deleteDimension: DeleteDimensionRequest
    deleteEmbeddedObject: DeleteEmbeddedObjectRequest
    deleteFilterView: DeleteFilterViewRequest
    duplicateFilterView: DuplicateFilterViewRequest
    duplicateSheet: DuplicateSheetRequest
    findReplace: FindReplaceRequest
    insertDimension: InsertDimensionRequest
    insertRange: InsertRangeRequest
    moveDimension: MoveDimensionRequest
    updateEmbeddedObjectPosition: UpdateEmbeddedObjectPositionRequest
    pasteData: PasteDataRequest
    textToColumns: TextToColumnsRequest
    updateFilterView: UpdateFilterViewRequest
    deleteRange: DeleteRangeRequest
    appendDimension: AppendDimensionRequest
    addConditionalFormatRule: AddConditionalFormatRuleRequest
    updateConditionalFormatRule: UpdateConditionalFormatRuleRequest
    deleteConditionalFormatRule: DeleteConditionalFormatRuleRequest
    sortRange: SortRangeRequest
    setDataValidation: SetDataValidationRequest
    setBasicFilter: SetBasicFilterRequest
    addProtectedRange: AddProtectedRangeRequest
    updateProtectedRange: UpdateProtectedRangeRequest
    deleteProtectedRange: DeleteProtectedRangeRequest
    autoResizeDimensions: AutoResizeDimensionsRequest
    addChart: AddChartRequest
    updateChartSpec: UpdateChartSpecRequest
    updateBanding: UpdateBandingRequest
    addBanding: AddBandingRequest
    deleteBanding: DeleteBandingRequest
    createDeveloperMetadata: CreateDeveloperMetadataRequest
    updateDeveloperMetadata: UpdateDeveloperMetadataRequest
    deleteDeveloperMetadata: DeleteDeveloperMetadataRequest
    randomizeRange: RandomizeRangeRequest
    addDimensionGroup: AddDimensionGroupRequest
    deleteDimensionGroup: DeleteDimensionGroupRequest
    updateDimensionGroup: UpdateDimensionGroupRequest
    trimWhitespace: TrimWhitespaceRequest
    deleteDuplicates: DeleteDuplicatesRequest
    updateEmbeddedObjectBorder: UpdateEmbeddedObjectBorderRequest
    addSlicer: AddSlicerRequest
    updateSlicerSpec: UpdateSlicerSpecRequest
    addDataSource: AddDataSourceRequest
    updateDataSource: UpdateDataSourceRequest
    deleteDataSource: DeleteDataSourceRequest
    refreshDataSource: RefreshDataSourceRequest
    cancelDataSourceRefresh: CancelDataSourceRefreshRequest
    addTable: AddTableRequest
    updateTable: UpdateTableRequest
    deleteTable: DeleteTableRequest

class AddNamedRangeResponse(BaseModel):
    namedRange: NamedRange

class AddSheetResponse(BaseModel):
    properties: SheetProperties

class AddFilterViewResponse(BaseModel):
    filter: FilterView

class DuplicateFilterViewResponse(BaseModel):
    filter: FilterView

class DuplicateSheetResponse(BaseModel):
    properties: SheetProperties

class FindReplaceResponse(BaseModel):
    valuesChanged: int
    formulasChanged: int
    rowsChanged: int
    sheetsChanged: int
    occurrencesChanged: int

class UpdateEmbeddedObjectPositionResponse(BaseModel):
    position: EmbeddedObjectPosition

class UpdateConditionalFormatRuleResponse(BaseModel):
    newrule: ConditionalFormatRule
    newIndex: int
    oldRule: ConditionalFormatRule
    oldIndex: int

class DeleteConditionalFormatRuleResponse(BaseModel):
    rule: ConditionalFormatRule

class AddProtectedRangeResponse(BaseModel):
    protectedRange: ProtectedRange

class AddChartResponse(BaseModel):
    chart: EmbeddedChart

class AddBandingResponse(BaseModel):
    bandedRange: BandedRange

class CreateDeveloperMetadataResponse(BaseModel):
    developerMetadata: DeveloperMetadata

class UpdateDeveloperMetadataResponse(BaseModel):
    developerMetadata: DeveloperMetadata

class DeleteDeveloperMetadataResponse(BaseModel):
    deletedDeveloperMetadata: List[DeveloperMetadata]

class AddDimensionGroupResponse(BaseModel):
    dimensionGroups: List[DimensionGroup]

class DeleteDimensionGroupResponse(BaseModel):
    dimensionGroups: List[DimensionGroup]

class TrimWhitespaceResponse(BaseModel):
    cellsChangedCount: int

class DeleteDuplicatesResponse(BaseModel):
    duplicatesRemovedCount: int

class AddSlicerResponse(BaseModel):
    slicer: Slicer

class AddDataSourceResponse(BaseModel):
    dataSource: DataSource
    dataExecutionStatus: DataExecutionStatus

class UpdateDataSourceResponse(BaseModel):
    dataSource: DataSource
    dataExecutionStatus: DataExecutionStatus

class RefreshDataSourceObjectExecutionStatus(BaseModel):
    reference: DataSourceObjectReference
    dataExecutionStatus: DataExecutionStatus

class RefreshDataSourceResponse(BaseModel):
    statuses: List[RefreshDataSourceObjectExecutionStatus]

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
    state: RefreshCancellationState
    errorCode: RefreshCancellationErrorCode

class CancelDataSourceRefreshStatus(BaseModel):
    reference: DataSourceObjectReference
    refreshCancellationStatus: RefreshCancellationStatus

class CancelDataSourceRefreshResponse(BaseModel):
    statuses: List[CancelDataSourceRefreshStatus]

class AddTableResponse(BaseModel):
    table: Table


class Response(BaseModel):
    addNamedRange: AddNamedRangeResponse
    addSheet: AddSheetResponse
    addFilterView: AddFilterViewResponse
    duplicateFilterView: DuplicateFilterViewResponse
    duplicateSheet: DuplicateSheetResponse
    findReplace: FindReplaceResponse
    updateEmbeddedObjectPosition: UpdateEmbeddedObjectPositionResponse
    updateConditionalFormatRule: UpdateConditionalFormatRuleResponse
    deleteConditionalFormatRule: DeleteConditionalFormatRuleResponse
    addProtectedRange: AddProtectedRangeResponse
    addChart: AddChartResponse
    addBanding: AddBandingResponse
    createDeveloperMetadata: CreateDeveloperMetadataResponse
    updateDeveloperMetadata: UpdateDeveloperMetadataResponse
    deleteDeveloperMetadata: DeleteDeveloperMetadataResponse
    addDimensionGroup: AddDimensionGroupResponse
    deleteDimensionGroup: DeleteDimensionGroupResponse
    trimWhitespace: TrimWhitespaceResponse
    deleteDuplicates: DeleteDuplicatesResponse
    addSlicer: AddSlicerResponse
    addDataSource: AddDataSourceResponse
    updateDataSource: UpdateDataSourceResponse
    refreshDataSource: RefreshDataSourceResponse
    cancelDataSourceRefresh: CancelDataSourceRefreshResponse
    addTable: AddTableResponse

class GridData(BaseModel):
    pass

class Sheet(BaseModel):
    properties: SheetProperties
    data: List[GridData]
    merges: List[GridRange]
    conditionalFormats: List[ConditionalFormatRule]
    filterViews: List[FilterView]
    protectedRanges: List[ProtectedRange]
    basicFilter: BasicFilter
    charts: List[EmbeddedChart]
    bandedRanges: List[BandedRange]
    developerMetadata: List[DeveloperMetadata]
    rowGroups: List[DimensionGroup]
    columnGroups: List[DimensionGroup]
    slicers: List[Slicer]
    tables: List[Table]

class DataSourceRefreshScope(Enum):
    DATA_SOURCE_REFRESH_SCOPE_UNSPECIFIED = "DATA_SOURCE_REFRESH_SCOPE_UNSPECIFIED"
    ALL_DATA_SOURCES = "ALL_DATA_SOURCES"

class TimeOfDay(BaseModel):
    hours: int
    minutes: int
    seconds: int
    nanos: int

class DataSourceRefreshDailySchedule(BaseModel):
    startTime: TimeOfDay

class Interval(BaseModel):
    startTime: str
    endTime: str

class DayOfWeek(Enum):
    DAY_OF_WEEK_UNSPECIFIED = "DAY_OF_WEEK_UNSPECIFIED"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class DataSourceRefreshMonthlySchedule(BaseModel):
    startTime: TimeOfDay
    daysOfMonth: List[int]

class DataSourceRefreshWeeklySchedule(BaseModel):
    startTime: TimeOfDay
    daysOfWeek: DayOfWeek


class DataSourceRefreshSchedule(BaseModel):
    enabled: bool
    refreshScope: DataSourceRefreshScope
    nextRun: Interval
    dailySchedule: DataSourceRefreshDailySchedule
    weeklySchedule: DataSourceRefreshWeeklySchedule
    monthlySchedule: DataSourceRefreshMonthlySchedule

class Spreadsheet(BaseModel):
    spreadsheetId: str
    properties: SpreadsheetProperties
    sheets: List[Sheet]
    namedRanges: List[NamedRange]
    spreadsheetUrl: str
    developerMetadata: List[DeveloperMetadata]
    dataSources: List[DataSource]
    dataSourceSchedules: List[DataSourceRefreshSchedule]


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
