from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Dimension(Enum):
    DIMENSION_UNSPECIFIED = "DIMENSION_UNSPECIFIED"
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"


class ValueRange(BaseModel):
    range: str = Field(
        ...,
        description="The range the values cover, in A1 notation. For output, this range indicates the entire requested range, even though the values will exclude trailing rows and columns. When appending values, this field represents the range to search for a table, after which values will be appended.",
    )
    majorDimension: Dimension = Field(
        ..., description="The major dimension of the values."
    )
    values: List = Field(
        ...,
        description="The data that was read or to be written. This is an array of arrays, the outer array representing all the data and each inner array representing a major dimension. Each item in the inner array corresponds with one cell. For output, empty trailing rows and columns will not be included.For input, supported value types are: bool, string, and double. Null values will be skipped. To set a cell to an empty value, set the string value to an empty string.",
    )


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


class TimeOfDay(BaseModel):
    hours: int = Field(
        ...,
        description="Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value '24:00:00' for scenarios like business closing time",
    )
    minutes: int = Field(
        ...,
        description="Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.",
    )
    seconds: int = Field(
        ...,
        description="Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.",
    )
    nanos: int = Field(
        ...,
        description="Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999.",
    )


class DataSourceRefreshMonthlySchedule(BaseModel):
    startTime: TimeOfDay
    daysOfMonth: List[int]


class DataSourceRefreshWeeklySchedule(BaseModel):
    startTime: TimeOfDay
    daysOfWeek: DayOfWeek


class DataSourceRefreshDailySchedule(BaseModel):
    startTime: TimeOfDay


class DataSourceRefreshScope(Enum):
    DATA_SOURCE_REFRESH_SCOPE_UNSPECIFIED = "DATA_SOURCE_REFRESH_SCOPE_UNSPECIFIED"
    ALL_DATA_SOURCES = "ALL_DATA_SOURCES"


class DataSourceRefreshSchedule(BaseModel):
    enabled: bool
    refreshScope: DataSourceRefreshScope
    nextRun: Interval
    dailySchedule: DataSourceRefreshDailySchedule
    weeklySchedule: DataSourceRefreshWeeklySchedule
    monthlySchedule: DataSourceRefreshMonthlySchedule


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


class DataSourceParameter(BaseModel):
    name: str
    namedRangeId: str
    range: GridRange


class LookerDataSourceSpec(BaseModel):
    instanceUri: str
    model: str
    explore: str


class BigQueryTableSpec(BaseModel):
    tableProjectId: str
    tableId: str
    datasetId: str


class BigQueryQuerySpec(BaseModel):
    rawQuery: str


class BigQueryDataSourceSpec(BaseModel):
    projectId: str
    querySpec: BigQueryQuerySpec
    tableSpec: BigQueryTableSpec


class DataSourceSpec(BaseModel):
    parameters: DataSourceParameter
    bigQuery: BigQueryDataSourceSpec
    looker: LookerDataSourceSpec


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


class DataSource(BaseModel):
    dataSourceId: str
    spec: DataSourceSpec
    calculatedColumns: DataSourceColumn
    sheetId: int


class NamedRange(BaseModel):
    namedRangeId: str = Field(..., description="The ID of the named range.")
    name: str = Field(..., description="The name of the named range.")
    range: GridRange = Field(..., description="The range this represents.")


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


class ColorStyle(BaseModel):
    rgbColor: Color = Field(
        ...,
        description="RGB color. The alpha value in the Color object isn't generally supported",
    )
    themeColor: ThemeColorType = Field(..., description="Theme color.")


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


class IterativeCalculationSettings(BaseModel):
    maxIterations: int = Field(
        ...,
        description="When iterative calculation is enabled, the maximum number of calculation rounds to perform.",
    )
    convergenceThreshold: int = Field(
        ...,
        description="When iterative calculation is enabled and successive results differ by less than this threshold value, the calculation rounds stop.",
    )


class RecalculationInterval(Enum):
    UNSPECIFIED = "RECALCULATION_INTERVAL_UNSPECIFIED"
    ON_CHANGE = "ON_CHANGE"
    MINUTE = "MINUTE"
    HOUR = "HOUR"


class HorizontalAlign(Enum):
    HORIZONTAL_ALIGN_UNSPECIFIED = "HORIZONTAL_ALIGN_UNSPECIFIED"
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


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


class SpreadsheetProperties(BaseModel):
    title: str = Field(..., description="The title of the spreadsheet.")
    locale: Optional[str] = Field(
        ...,
        description="The locale of the spreadsheet in one of the following formats: an ISO 639-1 language code such as en; an ISO 639-2 language code such as fil, if no 639-1 code exists; a combination of the ISO language code and country code, such as en_US; Note: when updating this field, not all locales/languages are supported.",
    )
    autoRecalc: Optional[RecalculationInterval] = Field(
        RecalculationInterval.UNSPECIFIED,
        description="The amount of time to wait before volatile functions are recalculated.",
    )
    timeZone: Optional[str] = Field(
        ...,
        description="The time zone of the spreadsheet, in CLDR format such as America/New_York. If the time zone isn't recognized, this may be a custom time zone such as GMT-07:00.",
    )
    defaultFormat: Optional[CellFormat] = Field(
        ...,
        description="The default format of all cells in the spreadsheet. CellData.effectiveFormat will not be set if the cell's format is equal to this default format. This field is read-only.",
    )
    iterativeCalculationSettings: Optional[IterativeCalculationSettings] = Field(
        ...,
        description="Determines whether and how circular references are resolved with iterative calculation. Absence of this field means that circular references result in calculation errors.",
    )
    spreadsheetTheme: Optional[SpreadsheetTheme] = Field(
        ..., description="Theme applied to the spreadsheet"
    )
    importFunctionsExternalUrlAccessAllowed: Optional[bool] = Field(
        ...,
        description="Whether to allow external URL access for image and import functions. Read only when true. When false, you can set to true. This value will be bypassed and always return true if the admin has enabled the allowlisting feature.",
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
    dataSourceId: str = Field(
        ..., description="ID of the DataSource the sheet is connected to."
    )
    columns: DataSourceColumn = Field(
        ...,
        description="The columns displayed on the sheet, corresponding to the values in RowData.",
    )
    dataExecutionStatus: DataExecutionStatus = Field(
        ..., description="The data execution status."
    )


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
    relativeDate: RelativeDate = Field(
        ...,
        description="A relative date (based on the current date). Valid only if the type is DATE_BEFORE, DATE_AFTER, DATE_ON_OR_BEFORE or DATE_ON_OR_AFTER.Relative dates are not supported in data validation. They are supported only in conditional formatting and conditional filters.",
    )
    userEnteredValue: str = Field(
        ...,
        description="A value the condition is based on. The value is parsed as if the user typed into a cell. Formulas are supported (and must begin with an = or a '+').",
    )


class BooleanCondition(BaseModel):
    type: ConditionType
    values: ConditionValue


class PivotFilterCriteria(BaseModel):
    visibleValues: List[str] = Field(
        ...,
        description="Values that should be included. Values not listed here are excluded.",
    )
    condition: BooleanCondition = Field(
        ...,
        description="A condition that must be true for values to be shown. ( visibleValues does not override this -- even if a value is listed there, it is still hidden if it does not meet the condition.)",
    )
    visibileByDefault: bool = Field(
        ...,
        description="Whether values are visible by default. If true, the visibleValues are ignored, all values that meet condition (if specified) are shown. If false, values that are both in visibleValues and meet condition are shown.",
    )


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


class PivotGroupSortValueBucket(BaseModel):
    valuesIndex: int = Field(
        ...,
        description="The offset in the PivotTable.values list which the values in this grouping should be sorted by.",
    )
    buckets: List[ExtendedValue] = Field(
        ...,
        description="Determines the bucket from which values are chosen to sort. For example, in a pivot table with one row group & two column groups, the row group can list up to two values. The first value corresponds to a value within the first column group, and the second value corresponds to a value in the second column group. If no values are listed, this would indicate that the row should be sorted according to the 'Grand Total' over the column groups. If a single value is listed, this would correspond to using the 'Total' of that bucket.",
    )


class PivotGroupValueMetadata(BaseModel):
    value: ExtendedValue = Field(
        ...,
        description="The calculated value the metadata corresponds to. (Note that formulaValue is not valid, because the values will be calculated.)",
    )
    collapsed: bool = Field(
        ..., description="True if the data corresponding to the value is collapsed."
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
    groups: List[ManualRuleGroup] = Field(
        ...,
        description="The list of group names and the corresponding items from the source data that map to each group name.",
    )


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
    type: DateTimeRuleType = Field(
        ..., description="The type of date-time grouping to apply."
    )


class PivotGroupRule(BaseModel):
    manualRule: ManualRule = Field(..., description="A ManualRule.")
    histogramRule: HistogramRule = Field(..., description="A HistogramRule.")
    dateTimeRule: DateTimeRule = Field(..., description="A DateTimeRule.")


class PivotGroupLimit(BaseModel):
    countLimit: int = Field(..., description="The count limit.")
    applyOrder: int = Field(
        ...,
        description="The order in which the group limit is applied to the pivot table. Pivot group limits are applied from lower to higher order number. Order numbers are normalized to consecutive integers from 0.",
    )


class SortOrder(Enum):
    SORT_ORDER_UNSPECIFIED = "SORT_ORDER_UNSPECIFIED"
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class PivotGroup(BaseModel):
    showTotals: bool = Field(
        ...,
        description="True if the pivot table should include the totals for this grouping.",
    )
    valueMetadata: PivotGroupValueMetadata = Field(
        ..., description="Metadata about values in the grouping."
    )
    sortOrder: SortOrder = Field(
        ..., description="The order the values in this group should be sorted."
    )
    valueBucket: PivotGroupSortValueBucket = Field(
        ...,
        description="The bucket of the opposite pivot group to sort by. If not specified, sorting is alphabetical by this group's values.",
    )
    repeatHeadings: bool = Field(
        ...,
        description="True if the headings in this pivot group should be repeated. This is only valid for row groupings and is ignored by columns. By default, we minimize repetition of headings by not showing higher level headings where they are the same",
    )
    label: str = Field(
        ...,
        description="The labels to use for the row/column groups which can be customized. For example, in the following pivot table, the row label is Region (which could be renamed to State) and the column label is Product (which could be renamed Item).",
    )
    groupRule: PivotGroupRule = Field(
        ..., description="The group rule to apply to this row/column group."
    )
    groupLimit: PivotGroupLimit = Field(
        ...,
        description="The count limit on rows or columns to apply to this pivot group.",
    )
    sourceColumnOffset: int = Field(
        ...,
        description="The column offset of the source range that this grouping is based on.",
    )
    dataSourceColumnReference: DataSourceColumnReference = Field(
        ...,
        description="The reference to the data source column this grouping is based on.",
    )


class PivotFilterSpec(BaseModel):
    filterCriteria: PivotFilterCriteria = Field(
        ..., description="The criteria for the column."
    )
    columnOffsetIndex: int = Field(
        ..., description="The zero-based column offset of the source range."
    )
    dataSourceColumnReference: DataSourceColumnReference = Field(
        ..., description="The reference to the data source column."
    )


class PivotValueSummarizeFunction(Enum):
    PIVOT_STANDARD_VALUE_FUNCTION_UNSPECIFIED = (
        "PIVOT_STANDARD_VALUE_FUNCTION_UNSPECIFIED"
    )
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
    PIVOT_VALUE_CALCULATED_DISPLAY_TYPE_UNSPECIFIED = (
        "PIVOT_VALUE_CALCULATED_DISPLAY_TYPE_UNSPECIFIED"
    )
    PERCENT_OF_ROW_TOTAL = "PERCENT_OF_ROW_TOTAL"
    PERCENT_OF_COLUMN_TOTAL = "PERCENT_OF_COLUMN_TOTAL"
    PERCENT_OF_GRAND_TOTAL = "PERCENT_OF_GRAND_TOTAL"


class PivotValue(BaseModel):
    summarizeFunction: PivotValueSummarizeFunction = Field(
        ...,
        description="A function to summarize the value. If formula is set, the only supported values are SUM and CUSTOM. If sourceColumnOffset is set, then CUSTOM is not supported.",
    )
    name: str = Field(..., description="A name to use for the value.")
    calculatedDisplayType: PivotValueCalculatedDisplayType = Field(
        ...,
        description="If specified, indicates that pivot values should be displayed as the result of a calculation with another pivot value.",
    )
    sourceColumnOffset: int = Field(
        ...,
        description="The column offset of the source range that this value reads from.",
    )
    formula: str = Field(
        ...,
        description="A custom formula to calculate the value. The formula must start with an = character.",
    )
    dataSourceColumnReference: DataSourceColumnReference = Field(
        ...,
        description="The reference to the data source column that this value reads from.",
    )


class PivotValueLayout(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"


class PivotTable(BaseModel):
    rows: List[PivotGroup] = Field(
        ..., description="Each row grouping in the pivot table."
    )
    columns: List[PivotGroup] = Field(
        ..., description="Each column grouping in the pivot table."
    )
    criteria: Dict[int, PivotFilterCriteria] = Field(
        ...,
        description="An optional mapping of filters per source column offset.The filters are applied before aggregating data into the pivot table. The map's key is the column offset of the source range that you want to filter, and the value is the criteria for that column",
    )
    filterSpecs: List[PivotFilterSpec] = Field(
        ...,
        description="The filters applied to the source columns before aggregating data for the pivot table. Both criteria and filterSpecs are populated in responses. If both fields are specified in an update request, this field takes precedence.",
    )
    values: List[PivotValue] = Field(
        ..., description="A list of values to include in the pivot table."
    )
    valueLayout: PivotValueLayout = Field(
        ...,
        description="Whether values should be listed horizontally (as columns) or vertically (as rows).",
    )
    dataExecutionStatus: DataExecutionStatus = Field(
        ...,
        description="Output only. The data execution status for data source pivot tables.",
    )
    source: GridRange = Field(
        ..., description="The range the pivot table is reading data from."
    )
    dataSourceId: str = Field(
        ...,
        description="The ID of the data source the pivot table is reading data from.",
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


class DataValidationRule(BaseModel):
    condition: BooleanCondition = Field(
        ..., description="The condition that data in the cell must match."
    )
    inputMessage: str = Field(
        ..., description="A message to show the user when adding data to the cell."
    )
    strict: bool = Field(..., description="True if invalid data should be rejected.")
    showCustomUi: bool = Field(
        ...,
        description="True if the UI should be customized based on the kind of condition. If true, 'List' conditions will show a dropdown.",
    )


class DataSourceFormula(BaseModel):
    dataSourceId: str = Field(
        ..., description="The ID of the data source the formula is associated with."
    )
    dataExecutionStatus: DataExecutionStatus = Field(
        ..., description="Output only. The data execution status."
    )


class FilterCriteria(BaseModel):
    hiddenValues: List[str] = Field(..., description="Values that should be hidden.")
    condition: BooleanCondition = Field(
        ...,
        description="A condition that must be true for values to be shown. (This does not override hiddenValues -- if a value is listed there, it will still be hidden.)",
    )
    visibleBackgroundcolorStyle: ColorStyle = Field(
        ...,
        description="The background fill color to filter by; only cells with this fill color are shown. This field is mutually exclusive with visibleForegroundColor, and must be set to an RGB-type color",
    )
    visibleForegroundColorStyle: ColorStyle = Field(
        ...,
        description="The foreground color to filter by; only cells with this foreground color are shown. This field is mutually exclusive with visibleBackgroundColor, and must be set to an RGB-type color.",
    )


class FilterSpec(BaseModel):
    filterCriteria: FilterCriteria = Field(
        ..., description="The criteria for the column"
    )
    columnIndex: int = Field(..., description="The zero-based column index.")
    dataSourceColumnReference: DataSourceColumnReference = Field(
        ..., description="Reference to a data source column."
    )


class SortSpec(BaseModel):
    sortOrder: SortOrder = Field(..., description="The order data should be sorted.")
    foregroundColorStyle: ColorStyle = Field(
        ...,
        description="The foreground color to sort by; cells with this foreground color are sorted to the top. Mutually exclusive with backgroundColor, and must be an RGB-type color.",
    )
    backgroundColorStyle: ColorStyle = Field(
        ...,
        description="The background fill color to sort by; cells with this fill color are sorted to the top. Mutually exclusive with foregroundColor, and must be an RGB-type color.",
    )
    dimensionIndex: int = Field(
        ..., description="The dimension the sort should be applied to."
    )
    dataSourceColumnReference: DataSourceColumnReference = Field(
        ..., description="Reference to a data source column"
    )


class DataSourceTableColumnSelectionType(Enum):
    DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED = (
        "DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED"
    )
    SELECTED = "SELECTED"
    SYNC_ALL = "SYNC_ALL"


class DataSourceTable(BaseModel):
    dataSourceId: str = Field(
        ...,
        description="The ID of the data source the data source table is associated with.",
    )
    columnSelectionType: DataSourceTableColumnSelectionType = Field(
        ...,
        description="he type to select columns for the data source table. Defaults to SELECTED.",
    )
    columns: List[DataSourceColumnReference] = Field(
        ...,
        description="Columns selected for the data source table. The columnSelectionType must be SELECTED.",
    )
    filterSpecs: List[FilterSpec] = Field(
        ..., description="Filter specifications in the data source table."
    )
    sortSpec: List[SortSpec] = Field(
        ...,
        description="Sort specifications in the data source table. The result of the data source table is sorted based on the sort specifications in order.",
    )
    rowLimit: int = Field(
        ...,
        description="The limit of rows to return. If not set, a default limit is applied. Please refer to the Sheets editor for the default and max limit.",
    )
    dataExecutionStatus: DataExecutionStatus = Field(
        ..., description="Output only. The data execution status."
    )


class DisplayFormat(Enum):
    DISPLAY_FORMAT_UNSPECIFIED = "DISPLAY_FORMAT_UNSPECIFIED"
    DEFAULT = "DEFAULT"
    LAST_NAME_COMMA_FIRST_NAME = "LAST_NAME_COMMA_FIRST_NAME"
    EMAIL = "EMAIL"


class PersonProperties(BaseModel):
    email: str = Field(
        ...,
        description="Required. The email address linked to this person. This field is always present.",
    )
    displayFormat: DisplayFormat = Field(
        ...,
        description="Optional. The display format of the person chip. If not set, the default display format is used.",
    )


class RichLinkProperties(BaseModel):
    uri: str = Field(
        ..., description="Required. The URI to the link. This is always present."
    )
    mimeType: str = Field(
        ...,
        description="Output only. The MIME type of the link, if there's one (for example, when it's a file in Drive).",
    )


class Chip(BaseModel):
    personProperties: PersonProperties = Field(
        ..., description="Properties of a linked person."
    )
    richLinkProperties: RichLinkProperties = Field(
        ..., description="Properties of a rich link."
    )


class ChipRun(BaseModel):
    startIndex: int = Field(
        ...,
        description="Required. The zero-based character index where this run starts, in UTF-16 code units.",
    )
    chip: Chip = Field(..., description="Optional. The chip of this run.")


class CellData(BaseModel):
    userEnteredValued: ExtendedValue = Field(
        ..., description="The value the user entered in the cell."
    )
    effectiveValue: ExtendedValue = Field(
        ...,
        description="The effective value of the cell. For cells with formulas, this is the calculated value. For cells with literals, this is the same as the userEnteredValue. This field is read-only.",
    )
    formattedValue: str = Field(
        ...,
        description="The formatted value of the cell. This is the value as it's shown to the user. This field is read-only.",
    )
    userEnteredFormat: CellFormat = Field(
        ...,
        description="The format the user entered for the cell. When writing, the new format will be merged with the existing format.",
    )
    effectiveFormat: CellFormat = Field(
        ...,
        description="The effective format being used by the cell. This includes the results of applying any conditional formatting and, if the cell contains a formula, the computed number format. If the effective format is the default format, effective format will not be written. This field is read-only.",
    )
    hyperlink: str = Field(
        ...,
        description="A hyperlink this cell points to, if any. If the cell contains multiple hyperlinks, this field will be empty. This field is read-only. To set it, use a =HYPERLINK formula in the userEnteredValue.formulaValue field. A cell-level link can also be set from the userEnteredFormat.textFormat field. Alternatively, set a hyperlink in the textFormatRun.format.link field that spans the entire cell.",
    )
    note: str = Field(..., description="Any note on the cell.")
    textFormatRuns: TextFormatRun = Field(
        ...,
        description="Runs of rich text applied to subsections of the cell. Runs are only valid on user entered strings, not formulas, bools, or numbers. Properties of a run start at a specific index in the text and continue until the next run. Runs will inherit the properties of the cell unless explicitly changed. When writing, the new runs will overwrite any prior runs. When writing a new userEnteredValue, previous runs are erased.",
    )
    dataValidation: DataValidationRule = Field(
        ...,
        description="A data validation rule on the cell, if any. When writing, the new data validation rule will overwrite any prior rule.",
    )
    pivotTable: PivotTable = Field(
        ...,
        description="A pivot table anchored at this cell. The size of pivot table itself is computed dynamically based on its data, grouping, filters, values, etc. Only the top-left cell of the pivot table contains the pivot table definition. The other cells will contain the calculated values of the results of the pivot in their effectiveValue fields.",
    )
    dataSourceTable: DataSourceTable = Field(
        ...,
        description="A data source table anchored at this cell. The size of data source table itself is computed dynamically based on its configuration. Only the first cell of the data source table contains the data source table definition. The other cells will contain the display values of the data source table result in their effectiveValue fields.",
    )
    dataSourceFormula: DataSourceFormula = Field(
        ...,
        description="Output only. Information about a data source formula on the cell. The field is set if userEnteredValue is a formula referencing some DATA_SOURCE sheet, e.g. =SUM(DataSheet!Column).",
    )
    chipRuns: List[ChipRun] = Field(
        ...,
        description="Optional. Runs of chips applied to subsections of the cell. Properties of a run start at a specific index in the text and continue until the next run. When reading, all chipped and non-chipped runs are included. Non-chipped runs will have an empty Chip. When writing, only runs with chips are included. Runs containing chips are of length 1 and are represented in the user-entered text by an “@” placeholder symbol. New runs will overwrite any prior runs. Writing a new userEnteredValue will erase previous runs.",
    )


class RowData(BaseModel):
    values: List[CellData] = Field(
        ..., description="The values in the row, one per column."
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


class DeveloperMetadataLocationType(Enum):
    DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED = (
        "DEVELOPER_METADATA_LOCATION_TYPE_UNSPECIFIED"
    )
    ROW = "ROW"
    COLUMN = "COLUMN"
    SHEET = "SHEET"
    SPREADSHEET = "SPREADSHEET"


class DeveloperMetadataLocation(BaseModel):
    locationType: DeveloperMetadataLocationType = Field(
        ...,
        description="The type of location this object represents. This field is read-only.",
    )
    spreadsheet: bool = Field(
        ..., description="True when metadata is associated with an entire spreadsheet."
    )
    sheetId: int = Field(
        ...,
        description="The ID of the sheet when metadata is associated with an entire sheet.",
    )
    dimensionRange: DimensionRange = Field(
        ...,
        description="Represents the row or column when metadata is associated with a dimension. The specified DimensionRange must represent a single row or column. It cannot be unbounded or span multiple rows or columns.",
    )


class DeveloperMetadataVisibility(Enum):
    DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED = (
        "DEVELOPER_METADATA_VISIBILITY_UNSPECIFIED"
    )
    DOCUMENT = "DOCUMENT"
    PROJECT = "PROJECT"


class DeveloperMetadata(BaseModel):
    metadataId: int = Field(
        ...,
        description="The spreadsheet-scoped unique ID that identifies the metadata. IDs may be specified when metadata is created, otherwise one will be randomly generated and assigned. Must be positive.",
    )
    metadataKey: str = Field(
        ...,
        description="The metadata key. There may be multiple metadata in a spreadsheet with the same key. Developer metadata must always have a key specified.",
    )
    metadataValue: str = Field(
        ..., description="Data associated with the metadata's key."
    )
    location: DeveloperMetadataLocation = Field(
        ..., description="The location where the metadata is associated."
    )
    visibility: DeveloperMetadataVisibility = Field(
        ...,
        description="The metadata visibility. Developer metadata must always have visibility specified.",
    )


class DimensionProperties(BaseModel):
    hiddenByFilter: bool = Field(
        ...,
        description="True if this dimension is being filtered. This field is read-only.",
    )
    hiddenByUser: bool = Field(
        ..., description="True if this dimension is explicitly hidden."
    )
    pixelSize: int = Field(
        ...,
        description="The height (if a row) or width (if a column) of the dimension in pixels.",
    )
    developerMetadata: List[DeveloperMetadata] = Field(
        ...,
        description="The developer metadata associated with a single row or column.",
    )
    dataSourceColumnReference: DataSourceColumnReference = Field(
        ..., description="Output only. If set, this is a column in a data source sheet."
    )


class GridData(BaseModel):
    startRow: int = Field(
        ..., description="The first row this GridData refers to, zero-based."
    )
    startColumn: int = Field(
        ..., description="The first column this GridData refers to, zero-based."
    )
    rowData: List[RowData] = Field(
        ...,
        description="The data in the grid, one entry per row, starting with the row in startRow. The values in RowData will correspond to columns starting at startColumn.",
    )
    rowMetadata: List[DimensionProperties] = Field(
        ...,
        description="Metadata about the requested rows in the grid, starting with the row in startRow.",
    )
    columnMetadata: List[DimensionProperties] = Field(
        ...,
        description="Metadata about the requested columns in the grid, starting with the column in startColumn.",
    )


class BooleanRule(BaseModel):
    condition: BooleanCondition = Field(
        ...,
        description="The condition of the rule. If the condition evaluates to true, the format is applied.",
    )
    format: CellFormat = Field(
        ...,
        description="The format to apply. Conditional formatting can only apply a subset of formatting: bold, italic, strikethrough, foreground color and, background color.",
    )


class InterpolationPointType(Enum):
    INTERPOLATION_POINT_TYPE_UNSPECIFIED = "INTERPOLATION_POINT_TYPE_UNSPECIFIED"
    MIN = "MIN"
    MAX = "MAX"
    NUMBER = "NUMBER"
    PERCENT = "PERCENT"
    PERCENTILE = "PERCENTILE"


class InterpolationPoint(BaseModel):
    colorStyle: ColorStyle = Field(
        ..., description="The color this interpolation point should use."
    )
    type: InterpolationPointType = Field(
        ..., description="How the value should be interpreted."
    )
    value: str = Field(
        ...,
        description="The value this interpolation point uses. May be a formula. Unused if type is MIN or MAX.",
    )


class GradientRule(BaseModel):
    minpoint: InterpolationPoint = Field(
        ..., description="The starting interpolation point."
    )
    midpoint: InterpolationPoint = Field(
        ..., description="An optional midway interpolation point."
    )
    maxpoint: InterpolationPoint = Field(
        ..., description="The final interpolation point."
    )


class ConditionalFormatRule(BaseModel):
    ranges: List[GridRange] = Field(
        ...,
        description="The ranges that are formatted if the condition is true. All the ranges must be on the same grid.",
    )
    booleanRule: BooleanRule = Field(
        ..., description="The formatting is either 'on' or 'off' according to the rule."
    )
    gradientRule: GradientRule = Field(
        ..., description="The formatting will vary based on the gradients in the rule."
    )


class FilterView(BaseModel):
    filterViewId: int = Field(..., description="The ID of the filter view.")
    title: str = Field(..., description="The name of the filter view.")
    range: GridRange = Field(
        ...,
        description="The range this filter view covers. When writing, only one of range, namedRangeId, or tableId may be set.",
    )
    namedRangeId: str = Field(
        ...,
        description="The named range this filter view is backed by, if any.When writing, only one of range, namedRangeId, or tableId may be set.",
    )
    tableId: str = Field(
        ...,
        description="The table this filter view is backed by, if any. When writing, only one of range, namedRangeId, or tableId may be set.",
    )
    sortSpecs: List[SortSpec] = Field(
        ...,
        description="The sort order per column. Later specifications are used when values are equal in the earlier specifications.",
    )
    filterSpecs: List[FilterSpec] = Field(
        ..., description="The filter criteria for showing or hiding values per column."
    )


class Editors(BaseModel):
    users: List[str] = Field(
        ...,
        description="The email addresses of users with edit access to the protected range.",
    )
    groups: List[str] = Field(
        ...,
        description="The email addresses of groups with edit access to the protected range.",
    )
    domainUsersCanEdit: bool = Field(
        ...,
        description="True if anyone in the document's domain has edit access to the protected range. Domain protection is only supported on documents within a domain.",
    )


class ProtectedRange(BaseModel):
    protectedRangeId: int = Field(
        ..., description="The ID of the protected range. This field is read-only."
    )
    range: GridRange = Field(
        ...,
        description="The range that is being protected. The range may be fully unbounded, in which case this is considered a protected sheet. When writing, only one of range or namedRangeId or tableId may be set.",
    )
    namedRangeId: str = Field(
        ...,
        description="The named range this protected range is backed by, if any. When writing, only one of range or namedRangeId or tableId may be set.",
    )
    tableId: str = Field(
        ...,
        description="The table this protected range is backed by, if any. When writing, only one of range or namedRangeId or tableId may be set.",
    )
    description: str = Field(
        ..., description="The description of this protected range."
    )
    warningOnly: bool = Field(
        ...,
        description="True if this protected range will show a warning when editing. Warning-based protection means that every user can edit data in the protected range, except editing will prompt a warning asking the user to confirm the edit.",
    )
    requestingUserCanEdit: bool = Field(
        ...,
        description="True if the user who requested this protected range can edit the protected area. This field is read-only.",
    )
    unprotectedRanges: List[GridRange] = Field(
        ...,
        description="The list of unprotected ranges within a protected sheet. Unprotected ranges are only supported on protected sheets.",
    )
    editors: Editors = Field(
        ...,
        description="The users and groups with edit access to the protected range. This field is only visible to users with edit access to the protected range and the document. Editors are not supported with warningOnly protection.",
    )


class BasicFilter(BaseModel):
    range: GridRange = Field(..., description="The range the filter covers.")
    tableid: str = Field(
        ...,
        description="The table this filter is backed by, if any. When writing, only one of range or tableId may be set.",
    )
    sortSpecs: List[SortSpec] = Field(
        ...,
        description="The sort order per column. Later specifications are used when values are equal in the earlier specifications.",
    )
    filterSpecs: List[FilterSpec] = Field(
        ..., description="The filter criteria per column."
    )


class BandingProperties(BaseModel):
    headerColorStyle: ColorStyle = Field(
        ...,
        description="The color of the first row or column. If this field is set, the first row or column is filled with this color and the colors alternate between firstBandColor and secondBandColor starting from the second row or column. Otherwise, the first row or column is filled with firstBandColor and the colors proceed to alternate as they normally would. If headerColor is also set, this field takes precedence.",
    )
    firstBandColorStyle: ColorStyle = Field(
        ...,
        description="The first color that is alternating. (Required) If firstBandColor is also set, this field takes precedence.",
    )
    secondBandColorStyle: ColorStyle = Field(
        ...,
        description="The second color that is alternating. (Required) If secondBandColor is also set, this field takes precedence.",
    )
    footerColorStyle: ColorStyle = Field(
        ...,
        description="The color of the last row or column. If this field is not set, the last row or column is filled with either firstBandColor or secondBandColor, depending on the color of the previous row or column. If footerColor is also set, this field takes precedence.",
    )


class BandedRange(BaseModel):
    bandedRangeId: int = Field(
        ...,
        description="The ID of the banded range. If unset, refer to bandedRangeReference.",
    )
    bandedRangeReference: str = Field(
        ...,
        description="Output only. The reference of the banded range, used to identify the ID that is not supported by the bandedRangeId.",
    )
    range: GridRange = Field(
        ..., description="The range over which these properties are applied."
    )
    rowProperties: BandingProperties = Field(
        ...,
        description="Properties for row bands. These properties are applied on a row-by-row basis throughout all the rows in the range. At least one of rowProperties or columnProperties must be specified.",
    )
    columnProperties: BandingProperties = Field(
        ...,
        description="Properties for column bands. These properties are applied on a column- by-column basis throughout all the columns in the range. At least one of rowProperties or columnProperties must be specified.",
    )


class DimensionGroup(BaseModel):
    range: DimensionRange = Field(
        ..., description="The range over which this group exists."
    )
    depth: int = Field(
        ...,
        description="The depth of the group, representing how many groups have a range that wholly contains the range of this group.",
    )
    collapsed: bool = Field(
        ...,
        description="This field is true if this group is collapsed. A collapsed group remains collapsed if an overlapping group at a shallower depth is expanded. A true value does not imply that all dimensions within the group are hidden, since a dimension's visibility can change independently from this group property. However, when this property is updated, all dimensions within it are set to hidden if this field is true, or set to visible if this field is false.",
    )


class SlicerSpec(BaseModel):
    dataRange: GridRange = Field(..., description="The data range of the slicer.")
    filterCriteria: FilterCriteria = Field(
        ..., description="The filtering criteria of the slicer."
    )
    columnIndex: int = Field(
        ...,
        description="The zero-based column index in the data table on which the filter is applied to.",
    )
    applyToPivotTables: bool = Field(
        ...,
        description="True if the filter should apply to pivot tables. If not set, default to True.",
    )
    title: str = Field(..., description="The title of the slicer.")
    textFormat: TextFormat = Field(
        ...,
        description="The text format of title in the slicer. The link field is not supported.",
    )
    backgroundColorStyle: ColorStyle = Field(
        ...,
        description="The background color of the slicer. If backgroundColor is also set, this field takes precedence.",
    )
    horizontalAlignment: HorizontalAlign = Field(
        ...,
        description="The horizontal alignment of title in the slicer. If unspecified, defaults to LEFT",
    )


class GridCoordinate(BaseModel):
    sheetId: int = Field(..., description="The sheet this coordinate is on.")
    rowIndex: int = Field(..., description="The row index of the coordinate.")
    columnIndex: int = Field(..., description="The column index of the coordinate.")


class OverlayPosition(BaseModel):
    anchorCell: GridCoordinate = Field(
        ..., description="The cell the object is anchored to."
    )
    offsetXPixels: int = Field(
        ...,
        description="The horizontal offset, in pixels, that the object is offset from the anchor cell.",
    )
    offsetYPixels: int = Field(
        ...,
        description="The vertical offset, in pixels, that the object is offset from the anchor cell.",
    )
    widthPixels: int = Field(
        ..., description="The width of the object, in pixels. Defaults to 600."
    )
    heightPixels: int = Field(
        ..., description="The height of the object, in pixels. Defaults to 371."
    )


class EmbeddedObjectPosition(BaseModel):
    sheetId: int = Field(
        ...,
        description="The sheet this is on. Set only if the embedded object is on its own sheet. Must be non-negative",
    )
    overlayPosition: OverlayPosition = Field(
        ...,
        description="The position at which the object is overlaid on top of a grid.",
    )
    newSheet: bool = Field(
        ...,
        description="If true, the embedded object is put on a new sheet whose ID is chosen for you. Used only when writing.",
    )


class Slicer(BaseModel):
    slicerId: int = Field(..., description="The ID of the slicer.")
    spec: SlicerSpec = Field(..., description="The specification of the slicer.")
    position: EmbeddedObjectPosition = Field(
        ...,
        description="The position of the slicer. Note that slicer can be positioned only on existing sheet. Also, width and height of slicer can be automatically adjusted to keep it within permitted limits.",
    )


class TableRowsProperties(BaseModel):
    headerColorStyle: ColorStyle = Field(
        ...,
        description="The color of the header row. If this field is set, the header row is filled with the specified color. Otherwise, the header row is filled with a default color.",
    )
    firstBandColorStyle: ColorStyle = Field(
        ...,
        description="The first color that is alternating. If this field is set, the first banded row is filled with the specified color. Otherwise, the first banded row is filled with a default color.",
    )
    secondBandColorStyle: ColorStyle = Field(
        ...,
        description="The second color that is alternating. If this field is set, the second banded row is filled with the specified color. Otherwise, the second banded row is filled with a default color.",
    )
    footerColorStyle: ColorStyle = Field(
        ...,
        description="The color of the last row. If this field is not set a footer is not added, the last row is filled with either firstBandColorStyle or secondBandColorStyle, depending on the color of the previous row.",
    )


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
    condition: BooleanCondition = Field(
        ...,
        description="The condition that data in the cell must match. Valid only if the [BooleanCondition.type] is ONE_OF_LIST.",
    )


class TableColumnProperties(BaseModel):
    columnIndex: int = Field(
        ...,
        description="The 0-based column index. This index is relative to its position in the table and is not necessarily the same as the column index in the sheet.",
    )
    columnName: str = Field(..., description="The column name.")
    columnType: ColumnType = Field(..., description="The column type.")
    dataValidationRule: TableColumnDataValidationRule = Field(
        ...,
        description="The column data validation rule. Only set for dropdown column type.",
    )


class Table(BaseModel):
    tableId: str = Field(..., description="The id of the table.")
    name: str = Field(
        ...,
        description="The table name. This is unique to all tables in the same spreadsheet.",
    )
    range: GridRange = Field(..., description="The table range.")
    rowsProperties: TableRowsProperties = Field(
        ..., description="The table rows properties."
    )
    columnProperties: List[TableColumnProperties] = Field(
        ..., description="The table column properties."
    )


class TextPosition(BaseModel):
    horizontalAlignment: HorizontalAlign = Field(
        ..., description="Horizontal alignment setting for the piece of text."
    )


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


class BasicChartStackedType(Enum):
    BASIC_CHART_STACKED_TYPE_UNSPECIFIED = "BASIC_CHART_STACKED_TYPE_UNSPECIFIED"
    NOT_STACKED = "NOT_STACKED"
    STACKED = "STACKED"
    PERCENT_STACKED = "PERCENT_STACKED"


class BasicChartCompareMode(Enum):
    BASIC_CHART_COMPARE_MODE_UNSPECIFIED = "BASIC_CHART_COMPARE_MODE_UNSPECIFIED"
    DATUM = "DATUM"
    CATEGORY = "CATEGORY"


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
    viewWindowMin: int = Field(
        ...,
        description="The minimum numeric value to be shown in this view window. If unset, will automatically determine a minimum value that looks good for the data.",
    )
    viewWindowMax: int = Field(
        ...,
        description="The maximum numeric value to be shown in this view window. If unset, will automatically determine a maximum value that looks good for the data.",
    )
    viewWindowMode: ViewWindowMode = Field(..., description="The view window's mode.")


class BasicChartAxis(BaseModel):
    position: BasicChartAxisPosition = Field(
        ..., description="The position of this axis."
    )
    title: str = Field(
        ...,
        description="The title of this axis. If set, this overrides any title inferred from headers of the data.",
    )
    format: TextFormat = Field(
        ...,
        description="The format of the title. Only valid if the axis is not associated with the domain. The link field is not supported.",
    )
    titleTextPosition: TextPosition = Field(
        ..., description="The axis title text position."
    )
    viewWindowOptions: ChartAxisViewWindowOptions = Field(
        ..., description="The view window options for this axis."
    )


class ChartAggregateType(Enum):
    CHART_AGGREGATE_TYPE_UNSPECIFIED = "CHART_AGGREGATE_TYPE_UNSPECIFIED"
    AVERAGE = "AVERAGE"
    COUNT = "COUNT"
    MAX = "MAX"
    MEDIAN = "MEDIAN"
    MIN = "MIN"
    SUM = "SUM"


class ChartSourceRange(BaseModel):
    sources: List[GridRange] = Field(
        ...,
        description="The ranges of data for a series or domain. Exactly one dimension must have a length of 1, and all sources in the list must have the same dimension with length 1. The domain (if it exists) & all series must have the same number of source ranges. If using more than one source range, then the source range at a given offset must be in order and contiguous across the domain and series.",
    )


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
    type: ChartDateTimeRuleType = Field(
        ..., description="The type of date-time grouping to apply."
    )


class ChartHistogramRule(BaseModel):
    minValue: int = Field(
        ...,
        description="The minimum value at which items are placed into buckets. Values that are less than the minimum are grouped into a single bucket. If omitted, it is determined by the minimum item value.",
    )
    maxValue: int = Field(
        ...,
        description="The maximum value at which items are placed into buckets. Values greater than the maximum are grouped into a single bucket. If omitted, it is determined by the maximum item value.",
    )
    intervalSize: int = Field(
        ..., description="The size of the buckets that are created. Must be positive."
    )


class ChartGroupRule(BaseModel):
    dateTimeRule: ChartDateTimeRule = Field(..., description="A ChartDateTimeRule.")
    histogramRule: ChartHistogramRule = Field(..., description="A ChartHistogramRule")


class ChartData(BaseModel):
    groupRule: ChartGroupRule = Field(
        ...,
        description="The rule to group the data by if the ChartData backs the domain of a data source chart. Only supported for data source charts.",
    )
    aggregateType: ChartAggregateType = Field(
        ...,
        description="The aggregation type for the series of a data source chart. Only supported for data source charts.",
    )
    sourceRange: ChartSourceRange = Field(
        ..., description="The source ranges of the data."
    )
    columnReference: DataSourceColumnReference = Field(
        ...,
        description="The reference to the data source column that the data reads from.",
    )


class BasicChartDomain(BaseModel):
    domain: ChartData = Field(
        ...,
        description="The data of the domain. For example, if charting stock prices over time, this is the data representing the dates.",
    )
    reversed: bool = Field(
        ...,
        description="True to reverse the order of the domain values (horizontal axis).",
    )


class DataLabelType(Enum):
    DATA_LABEL_TYPE_UNSPECIFIED = "DATA_LABEL_TYPE_UNSPECIFIED"
    NONE = "NONE"
    DATA = "DATA"
    CUSTOM = "CUSTOM"


class DataLabelPlacement(Enum):
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
    type: DataLabelType = Field(..., description="The type of the data label.")
    textFormat: TextFormat = Field(
        ...,
        description="The text format used for the data label. The link field is not supported.",
    )
    placement: DataLabelPlacement = Field(
        ..., description="The placement of the data label relative to the labeled data."
    )
    customLabelData: ChartData = Field(
        ...,
        description="Data to use for custom labels. Only used if type is set to CUSTOM. This data must be the same length as the series or other element this data label is applied to. In addition, if the series is split into multiple source ranges, this source data must come from the next column in the source data.",
    )


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
    width: int = Field(..., description="The thickness of the line, in px.")
    type: LineDashType = Field(..., description="The dash type of the line.")


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
    size: int = Field(
        ..., description="The point size. If empty, a default size is used."
    )
    shape: PointShape = Field(
        ...,
        description="The point shape. If empty or unspecified, a default shape is used.",
    )


class BasicSeriesDataPointStyleOverride(BaseModel):
    index: int = Field(
        ..., description="The zero-based index of the series data point."
    )
    colorStyle: ColorStyle = Field(
        ...,
        description="Color of the series data point. If empty, the series default is used. If color is also set, this field takes precedence.",
    )
    pointStyle: PointStyle = Field(
        ...,
        description="Point style of the series data point. Valid only if the chartType is AREA, LINE, or SCATTER. COMBO charts are also supported if the series chart type is AREA, LINE, or SCATTER. If empty, the series default is used.",
    )


class BasicChartSeries(BaseModel):
    series: ChartData = Field(
        ..., description="The data being visualized in this chart series."
    )
    targetAxis: BasicChartAxisPosition = Field(
        ...,
        description="The minor axis that will specify the range of values for this series. For example, if charting stocks over time, the 'Volume' series may want to be pinned to the right with the prices pinned to the left, because the scale of trading volume is different than the scale of prices. It is an error to specify an axis that isn't a valid minor axis for the chart's type.",
    )
    type: BasicChartType = Field(
        ...,
        description="The type of this series. Valid only if the chartType is COMBO. Different types will change the way the series is visualized. Only LINE, AREA, and COLUMN are supported.",
    )
    lineStyle: LineStyle = Field(
        ...,
        description="The line style of this series. Valid only if the chartType is AREA, LINE, or SCATTER. COMBO charts are also supported if the series chart type is AREA or LINE.",
    )
    dataLabel: DataLabel = Field(
        ..., description="Information about the data labels for this series."
    )
    colorStyle: ColorStyle = Field(
        ...,
        description="The color for elements (such as bars, lines, and points) associated with this series. If empty, a default color is used. If color is also set, this field takes precedence.",
    )
    pointStyle: PointStyle = Field(
        ...,
        description="The style for points associated with this series. Valid only if the chartType is AREA, LINE, or SCATTER. COMBO charts are also supported if the series chart type is AREA, LINE, or SCATTER. If empty, a default point style is used.",
    )
    styleOverrides: List[BasicSeriesDataPointStyleOverride] = Field(
        ..., description="Style override settings for series data points."
    )


class BasicChartSpec(BaseModel):
    chartType: BasicChartType = Field(..., description="The type of the chart.")
    legendPosition: BasicChartLegendPosition = Field(
        ..., description="The position of the chart legend."
    )
    axis: List[BasicChartAxis] = Field(..., description="The axis on the chart.")
    domains: List[BasicChartDomain] = Field(
        ...,
        description="The domain of data this is charting. Only a single domain is supported.",
    )
    series: List[BasicChartSeries] = Field(
        ..., description="The data this chart is visualizing."
    )
    headerCount: int = Field(
        ...,
        description="The number of rows or columns in the data that are 'headers'. If not set, Google Sheets will guess how many rows are headers based on the data. (Note that BasicChartAxis.title may override the axis title inferred from the header values.)",
    )
    threeDimensional: bool = Field(
        ..., description="True to make the chart 3D. Applies to Bar and Column charts."
    )
    interpolateNulls: bool = Field(
        ...,
        description="If some values in a series are missing, gaps may appear in the chart (e.g, segments of lines in a line chart will be missing). To eliminate these gaps set this to true. Applies to Line, Area, and Combo charts.",
    )
    stackedType: BasicChartStackedType = Field(
        ...,
        description="The stacked type for charts that support vertical stacking. Applies to Area, Bar, Column, Combo, and Stepped Area charts.",
    )
    lineSmoothing: bool = Field(
        ...,
        description="Gets whether all lines should be rendered smooth or straight by default. Applies to Line charts.",
    )
    compareMode: BasicChartCompareMode = Field(
        ...,
        description="The behavior of tooltips and data highlighting when hovering on data and chart area.",
    )
    totalDataLabel: DataLabel = Field(
        ...,
        description="Controls whether to display additional data labels on stacked charts which sum the total value of all stacked values at each value along the domain axis.",
    )


class DataSourceChartProperties(BaseModel):
    dataSourceId: str = Field(
        ..., description="ID of the data source that the chart is associated with."
    )
    dataExecutionStatus: DataExecutionStatus = Field(
        ..., description="Output only. The data execution status."
    )


class PieChartLegendPosition(Enum):
    PIE_CHART_LEGEND_POSITION_UNSPECIFIED = "PIE_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    LABELED_LEGEND = "LABELED_LEGEND"


class PieChartSpec(BaseModel):
    legendPosition: PieChartLegendPosition = Field(
        ..., description="Where the legend of the pie chart should be drawn."
    )
    domain: ChartData = Field(
        ..., description="The data that covers the domain of the pie chart."
    )
    series: ChartData = Field(
        ...,
        description="The data that covers the one and only series of the pie chart.",
    )
    threeDimensional: bool = Field(
        ..., description="True if the pie is three dimensional."
    )
    pieHole: int = Field(..., description="The size of the hole in the pie chart.")


class BubbleChartLegendPosition(Enum):
    BUBBLE_CHART_LEGEND_POSITION_UNSPECIFIED = (
        "BUBBLE_CHART_LEGEND_POSITION_UNSPECIFIED"
    )
    BOTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    INSIDE_LEGEND = "INSIDE_LEGEND"


class BubbleChartSpec(BaseModel):
    legendPosition: BubbleChartLegendPosition = Field(
        ..., description="Where the legend of the chart should be drawn."
    )
    bubbleLabels: ChartData = Field(
        ...,
        description="The data containing the bubble labels. These do not need to be unique.",
    )
    domain: ChartData = Field(
        ...,
        description="The data containing the bubble x-values. These values locate the bubbles in the chart horizontally.",
    )
    series: ChartData = Field(
        ...,
        description="The data containing the bubble y-values. These values locate the bubbles in the chart vertically.",
    )
    groupIds: ChartData = Field(
        ...,
        description="The data containing the bubble group IDs. All bubbles with the same group ID are drawn in the same color. If bubbleSizes is specified then this field must also be specified but may contain blank values. This field is optional.",
    )
    bubbleSizes: ChartData = Field(
        ...,
        description="The data containing the bubble sizes. Bubble sizes are used to draw the bubbles at different sizes relative to each other. If specified, groupIds must also be specified. This field is optional.",
    )
    bubbleOpacity: int = Field(
        ...,
        description="The opacity of the bubbles between 0 and 1.0. 0 is fully transparent and 1 is fully opaque.",
    )
    bubbleBorderColorStyle: ColorStyle = Field(
        ...,
        description="The bubble border color. If bubbleBorderColor is also set, this field takes precedence.",
    )
    bubbleMaxRadiusSize: int = Field(
        ...,
        description="The max radius size of the bubbles, in pixels. If specified, the field must be a positive value.",
    )
    bubbleMinRadiusSize: int = Field(
        ...,
        description="The minimum radius size of the bubbles, in pixels. If specific, the field must be a positive value.",
    )
    bubbleTextStyle: TextFormat = Field(
        ...,
        description="The format of the text inside the bubbles. Strikethrough, underline, and link are not supported.",
    )


class CandlestickDomain(BaseModel):
    data: ChartData = Field(..., description="The data of the CandlestickDomain.")
    reversed: bool = Field(
        ...,
        description="True to reverse the order of the domain values (horizontal axis).",
    )


class CandlestickSeries(BaseModel):
    data: ChartData = Field(..., description="The data of the CandlestickSeries.")


class CandlestickData(BaseModel):
    lowSeries: CandlestickSeries = Field(
        ...,
        description="The range data (vertical axis) for the low/minimum value for each candle. This is the bottom of the candle's center line.",
    )
    openSeries: CandlestickSeries = Field(
        ...,
        description="The range data (vertical axis) for the open/initial value for each candle. This is the bottom of the candle body. If less than the close value the candle will be filled. Otherwise the candle will be hollow.",
    )
    closeSeries: CandlestickSeries = Field(
        ...,
        description="The range data (vertical axis) for the close/final value for each candle. This is the top of the candle body. If greater than the open value the candle will be filled. Otherwise the candle will be hollow.",
    )
    highSeries: CandlestickSeries = Field(
        ...,
        description="The range data (vertical axis) for the high/maximum value for each candle. This is the top of the candle's center line.",
    )


class CandlestickChartSpec(BaseModel):
    domain: CandlestickDomain = Field(
        ...,
        description="The domain data (horizontal axis) for the candlestick chart. String data will be treated as discrete labels, other data will be treated as continuous values.",
    )
    data: CandlestickData = Field(
        ...,
        description="The Candlestick chart data. Only one CandlestickData is supported.",
    )


class HistogramChartLegendPosition(Enum):
    HISTOGRAM_CHART_LEGEND_POSITION_UNSPECIFIED = (
        "HISTOGRAM_CHART_LEGEND_POSITION_UNSPECIFIED"
    )
    BOTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    INSIDE_LEGEND = "INSIDE_LEGEND"


class HistogramSeries(BaseModel):
    barColorStyle: ColorStyle = Field(
        ...,
        description="The color of the column representing this series in each bucket. This field is optional. If barColor is also set, this field takes precedence.",
    )
    data: ChartData = Field(..., description="The data for this histogram series.")


class HistogramChartSpec(BaseModel):
    series: List[HistogramSeries] = Field(
        ...,
        description="The series for a histogram may be either a single series of values to be bucketed or multiple series, each of the same length, containing the name of the series followed by the values to be bucketed for that series.",
    )
    legendPosition: HistogramChartLegendPosition = Field(
        ..., description="The position of the chart legend."
    )
    showItemDividers: bool = Field(
        ...,
        description="Whether horizontal divider lines should be displayed between items in each column.",
    )
    bucketSize: int = Field(
        ...,
        description="By default the bucket size (the range of values stacked in a single column) is chosen automatically, but it may be overridden here.",
    )
    outlierPercentile: int = Field(
        ...,
        description="The outlier percentile is used to ensure that outliers do not adversely affect the calculation of bucket sizes. For example, setting an outlier percentile of 0.05 indicates that the top and bottom 5% of values when calculating buckets. The values are still included in the chart, they will be added to the first or last buckets instead of their own buckets. Must be between 0.0 and 0.5.",
    )


class OrgChartNodeSize(Enum):
    ORG_CHART_LABEL_SIZE_UNSPECIFIED = "ORG_CHART_LABEL_SIZE_UNSPECIFIED"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class OrgChartSpec(BaseModel):
    nodeSize: OrgChartNodeSize = Field(
        ..., description="The size of the org chart nodes."
    )
    nodeColorStyle: ColorStyle = Field(
        ...,
        description="The color of the org chart nodes. If nodeColor is also set, this field takes precedence.",
    )
    selectedNodeColorStyle: ColorStyle = Field(
        ...,
        description="The color of the selected org chart nodes. If selectedNodeColor is also set, this field takes precedence.",
    )
    labels: ChartData = Field(
        ...,
        description="The data containing the labels for all the nodes in the chart. Labels must be unique.",
    )
    parentLabels: Optional[ChartData] = Field(
        ...,
        description="The data containing the label of the parent for the corresponding node. A blank value indicates that the node has no parent and is a top-level node. This field is optional.",
    )
    tooltips: Optional[ChartData] = Field(
        ...,
        description="The data containing the tooltip for the corresponding node. A blank value results in no tooltip being displayed for the node. This field is optional.",
    )


class WaterfallChartStackedType(Enum):
    WATERFALL_STACKED_TYPE_UNSPECIFIED = "WATERFALL_STACKED_TYPE_UNSPECIFIED"
    STACKED = "STACKED"
    SEQUENTIAL = "SEQUENTIAL"


class WaterfallChartDomain(BaseModel):
    data: ChartData = Field(..., description="The data of the WaterfallChartDomain.")
    reversed: bool = Field(
        ...,
        description="True to reverse the order of the domain values (horizontal axis).",
    )


class WaterfallChartColumnStyle(BaseModel):
    label: str = Field(..., description="The label of the column's legend.")
    colorStyle: ColorStyle = Field(
        ...,
        description="The color of the column. If color is also set, this field takes precedence.",
    )


class WaterfallChartCustomSubtotal(BaseModel):
    subtotalIndex: int = Field(
        ...,
        description="The zero-based index of a data point within the series. If dataIsSubtotal is true, the data point at this index is the subtotal. Otherwise, the subtotal appears after the data point with this index. A series can have multiple subtotals at arbitrary indices, but subtotals do not affect the indices of the data points.",
    )
    label: str = Field(..., description="A label for the subtotal column.")
    dataIsSubtotal: bool = Field(
        ...,
        description="True if the data point at subtotalIndex is the subtotal. If false, the subtotal will be computed and appear after the data point.",
    )


class WaterfallChartSeries(BaseModel):
    data: ChartData = Field(
        ..., description="The data being visualized in this series."
    )
    positiveColumnsStyle: WaterfallChartColumnStyle = Field(
        ..., description="Styles for all columns in this series with positive values."
    )
    negativeColumnsStyle: WaterfallChartColumnStyle = Field(
        ..., description="Styles for all columns in this series with negative values."
    )
    subtotalColumnsStyle: WaterfallChartColumnStyle = Field(
        ..., description="Styles for all subtotal columns in this series."
    )
    hideTrailingSubtotal: bool = Field(
        ...,
        description="True to hide the subtotal column from the end of the series. By default, a subtotal column will appear at the end of each series. Setting this field to true will hide that subtotal column for this series.",
    )
    customSubtotals: List[WaterfallChartCustomSubtotal] = Field(
        ...,
        description="Custom subtotal columns appearing in this series. The order in which subtotals are defined is not significant. Only one subtotal may be defined for each data point.",
    )
    dataLabel: DataLabel = Field(
        ..., description="Information about the data labels for this series."
    )


class WaterfallChartSpec(BaseModel):
    domain: WaterfallChartDomain = Field(
        ..., description="The domain data (horizontal axis) for the waterfall chart."
    )
    series: WaterfallChartSeries = Field(
        ..., description="The data this waterfall chart is visualizing."
    )
    stackedType: WaterfallChartStackedType = Field(..., description="The stacked type.")
    firstValueIsTotal: bool = Field(
        ..., description="True to interpret the first value as a total."
    )
    hideConnectorLines: bool = Field(
        ..., description="True to hide connector lines between columns."
    )
    connectorLineStyle: LineStyle = Field(
        ..., description="The line style for the connector lines."
    )
    totalDataLabel: DataLabel = Field(
        ...,
        description="Controls whether to display additional data labels on stacked charts which sum the total value of all stacked values at each value along the domain axis. stackedType must be STACKED and neither CUSTOM nor placement can be set on the totalDataLabel.",
    )


class TreemapChartColorScale(BaseModel):
    minValueColorStyle: ColorStyle = Field(
        ...,
        description="The background color for cells with a color value less than or equal to minValue. Defaults to #dc3912 if not specified. If minValueColor is also set, this field takes precedence.",
    )
    midValueColorStyle: ColorStyle = Field(
        ...,
        description="The background color for cells with a color value at the midpoint between minValue and maxValue. Defaults to #efe6dc if not specified. If midValueColor is also set, this field takes precedence.",
    )
    maxValueColorStyle: ColorStyle = Field(
        ...,
        description="The background color for cells with a color value greater than or equal to maxValue. Defaults to #109618 if not specified. If maxValueColor is also set, this field takes precedence.",
    )
    noDataColorStyle: ColorStyle = Field(
        ...,
        description="The background color for cells that have no color data associated with them. Defaults to #000000 if not specified. If noDataColor is also set, this field takes precedence.",
    )


class TreemapChartSpec(BaseModel):
    labels: ChartData = Field(
        ..., description="The data that contains the treemap cell labels."
    )
    parentLabels: ChartData = Field(
        ..., description="The data the contains the treemap cells' parent labels."
    )
    sizeData: ChartData = Field(
        ...,
        description="The data that determines the size of each treemap data cell. This data is expected to be numeric. The cells corresponding to non-numeric or missing data will not be rendered. If colorData is not specified, this data is used to determine data cell background colors as well.",
    )
    colorData: ChartData = Field(
        ...,
        description="The data that determines the background color of each treemap data cell. This field is optional. If not specified, sizeData is used to determine background colors. If specified, the data is expected to be numeric. colorScale will determine how the values in this data map to data cell background colors.",
    )
    textFormat: TextFormat = Field(
        ...,
        description="The text format for all labels on the chart. The link field is not supported.",
    )
    levels: int = Field(
        ...,
        description="The number of data levels to show on the treemap chart. These levels are interactive and are shown with their labels. Defaults to 2 if not specified.",
    )
    hintedLevels: int = Field(
        ...,
        description="The number of additional data levels beyond the labeled levels to be shown on the treemap chart. These levels are not interactive and are shown without their labels. Defaults to 0 if not specified.",
    )
    minValue: int = Field(
        ...,
        description="The minimum possible data value. Cells with values less than this will have the same color as cells with this value. If not specified, defaults to the actual minimum value from colorData, or the minimum value from sizeData if colorData is not specified.",
    )
    maxValue: int = Field(
        ...,
        description="The maximum possible data value. Cells with values greater than this will have the same color as cells with this value. If not specified, defaults to the actual maximum value from colorData, or the maximum value from sizeData if colorData is not specified.",
    )
    headerColorStyle: ColorStyle = Field(
        ...,
        description="The background color for header cells. If headerColor is also set, this field takes precedence.",
    )
    colorScale: TreemapChartColorScale = Field(
        ...,
        description="The color scale for data cells in the treemap chart. Data cells are assigned colors based on their color values. These color values come from colorData, or from sizeData if colorData is not specified. Cells with color values less than or equal to minValue will have minValueColor as their background color. Cells with color values greater than or equal to maxValue will have maxValueColor as their background color. Cells with color values between minValue and maxValue will have background colors on a gradient between minValueColor and maxValueColor, the midpoint of the gradient being midValueColor. Cells with missing or non-numeric color values will have noDataColor as their background color.",
    )
    hideToolTips: bool = Field(..., description="True to hide tooltips.")


class ChartHiddenDimensionStrategy(Enum):
    CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED = (
        "CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED"
    )
    SKIP_HIDDEN_ROWS_AND_COLUMNS = "SKIP_HIDDEN_ROWS_AND_COLUMNS"
    SKIP_HIDDEN_ROWS = "SKIP_HIDDEN_ROWS"
    SKIP_HIDDEN_COLUMNS = "SKIP_HIDDEN_COLUMNS"
    SHOW_ALL = "SHOW_ALL"


class KeyValueFormat(BaseModel):
    textFormat: TextFormat = Field(
        ...,
        description="Text formatting options for key value. The link field is not supported.",
    )
    position: TextPosition = Field(
        ...,
        description="Specifies the horizontal text positioning of key value. This field is optional. If not specified, default positioning is used.",
    )


class ComparisonType(Enum):
    COMPARISON_TYPE_UNDEFINED = "COMPARISON_TYPE_UNDEFINED"
    ABSOLUTE_DIFFERENCE = "ABSOLUTE_DIFFERENCE"
    PERCENTAGE_DIFFERENCE = "PERCENTAGE_DIFFERENCE"


class BaselineValueFormat(BaseModel):
    comparisonType: ComparisonType = Field(
        ..., description="The comparison type of key value with baseline value."
    )
    textFormat: TextFormat = Field(
        ...,
        description="Text formatting options for baseline value. The link field is not supported.",
    )
    position: TextPosition = Field(
        ...,
        description="Specifies the horizontal text positioning of baseline value. This field is optional. If not specified, default positioning is used.",
    )
    description: Optional[str] = Field(
        ...,
        description="Description which is appended after the baseline value. This field is optional.",
    )
    positiveColorStyle: ColorStyle = Field(
        ...,
        description="Color to be used, in case baseline value represents a positive change for key value. This field is optional. If positiveColor is also set, this field takes precedence.",
    )
    negativeColorStyle: ColorStyle = Field(
        ...,
        description="Color to be used, in case baseline value represents a negative change for key value. This field is optional. If negativeColor is also set, this field takes precedence.",
    )


class ChartNumberFormatSource(Enum):
    CHART_NUMBER_FORMAT_SOURCE_UNDEFINED = "CHART_NUMBER_FORMAT_SOURCE_UNDEFINED"
    FROM_DATA = "FROM_DATA"
    CUSTOM = "CUSTOM"


class ChartCustomNumberFormatOptions(BaseModel):
    prefix: Optional[str] = Field(
        ...,
        description="Custom prefix to be prepended to the chart attribute. This field is optional.",
    )
    suffix: Optional[str] = Field(
        ...,
        description="Custom suffix to be appended to the chart attribute. This field is optional.",
    )


class ScorecardChartSpec(BaseModel):
    keyValueData: ChartData = Field(
        ..., description="The data for scorecard key value."
    )
    baselineValueData: Optional[ChartData] = Field(
        ...,
        description="The data for scorecard baseline value. This field is optional.",
    )
    aggregateType: Optional[ChartAggregateType] = Field(
        ...,
        description="The aggregation type for key and baseline chart data in scorecard chart. This field is not supported for data source charts. Use the ChartData.aggregateType field of the keyValueData or baselineValueData instead for data source charts. This field is optional.",
    )
    keyValueFormat: KeyValueFormat = Field(
        ..., description="Formatting options for key value."
    )
    baselineValueFormat: BaselineValueFormat = Field(
        ...,
        description="Formatting options for baseline value. This field is needed only if baselineValueData is specified.",
    )
    scaleFactor: Optional[int] = Field(
        ...,
        description="Value to scale scorecard key and baseline value. For example, a factor of 10 can be used to divide all values in the chart by 10. This field is optional.",
    )
    numberFormatSource: Optional[ChartNumberFormatSource] = Field(
        ...,
        description="The number format source used in the scorecard chart. This field is optional.",
    )
    customFormatOptions: Optional[ChartCustomNumberFormatOptions] = Field(
        ...,
        description="Custom formatting options for numeric key/baseline values in scorecard chart. This field is used only when numberFormatSource is set to CUSTOM. This field is optional.",
    )


class ChartSpec(BaseModel):
    title: str = Field(..., description="The title of the chart.")
    altText: str = Field(
        ...,
        description="The alternative text that describes the chart. This is often used for accessibility.",
    )
    titleTextFormat: TextFormat = Field(
        ...,
        description="The title text format. Strikethrough, underline, and link are not supported.",
    )
    titleTextPosition: TextPosition = Field(
        ..., description="The title text position. This field is optional."
    )
    subtitle: str = Field(..., description="The subtitle of the chart.")
    subtitleTextFormat: TextFormat = Field(
        ...,
        description="The subtitle text format. Strikethrough, underline, and link are not supported.",
    )
    subtitleTextPosition: TextPosition = Field(
        ..., description="The subtitle text position. This field is optional."
    )
    fontName: str = Field(
        ...,
        description="The name of the font to use by default for all chart text (e.g. title, axis labels, legend). If a font is specified for a specific part of the chart it will override this font name.",
    )
    maximized: bool = Field(
        ...,
        description="True to make a chart fill the entire space in which it's rendered with minimum padding. False to use the default padding. (Not applicable to Geo and Org charts.)",
    )
    backgroundColorStyle: ColorStyle = Field(
        ...,
        description="The background color of the entire chart. Not applicable to Org charts.",
    )
    dataSourceChartProperties: DataSourceChartProperties = Field(
        ...,
        description="If present, the field contains data source chart specific properties.",
    )
    filterSpecs: List[FilterSpec] = Field(
        ...,
        description="The filters applied to the source data of the chart. Only supported for data source charts.",
    )
    sortSpecs: List[SortSpec] = Field(
        ...,
        description="The order to sort the chart data by. Only a single sort spec is supported. Only supported for data source charts.",
    )
    hiddenDimensionStrategy: ChartHiddenDimensionStrategy = Field(
        ..., description="Determines how the charts will use hidden rows or columns."
    )
    basicChart: BasicChartSpec = Field(
        ...,
        description="A basic chart specification, can be one of many kinds of charts. See BasicChartType for the list of all charts this supports.",
    )
    pieChart: PieChartSpec = Field(..., description="A pie chart specification.")
    bubbleChart: BubbleChartSpec = Field(
        ..., description="A bubble chart specification."
    )
    candlestickChart: CandlestickChartSpec = Field(
        ..., description="A candlestick chart specification."
    )
    orgChart: OrgChartSpec = Field(..., description="An org chart specification.")
    histogramChart: HistogramChartSpec = Field(
        ..., description="A histogram chart specification."
    )
    waterfallChart: WaterfallChartSpec = Field(
        ..., description="A waterfall chart specification."
    )
    treemapChart: TreemapChartSpec = Field(
        ..., description="A treemap chart specification."
    )
    scorecardChart: ScorecardChartSpec = Field(
        ..., description="A scorecard chart specification."
    )


class EmbeddedObjectBorder(BaseModel):
    colorStyle: ColorStyle = Field(
        ...,
        description="The color of the border. If color is also set, this field takes precedence.",
    )


class EmbeddedChart(BaseModel):
    chartId: int = Field(..., description="The ID of the chart.")
    spec: ChartSpec = Field(..., description="The specification of the chart.")
    position: EmbeddedObjectPosition = Field(
        ..., description="The position of the chart."
    )
    border: EmbeddedObjectBorder = Field(..., description="The border of the chart.")


class Sheet(BaseModel):
    properties: SheetProperties = Field(..., description="The properties of the sheet.")
    data: List[GridData] = Field(
        ...,
        description="Data in the grid, if this is a grid sheet. The number of GridData objects returned is dependent on the number of ranges requested on this sheet.",
    )
    merges: List[GridRange] = Field(
        ..., description="The ranges that are merged together."
    )
    conditionalFormats: List[ConditionalFormatRule] = Field(
        ..., description="The conditional format rules in this sheet."
    )
    filterViews: List[FilterView] = Field(
        ..., description="The filter views in this sheet."
    )
    protectedRanges: List[ProtectedRange] = Field(
        ..., description="The protected ranges in this sheet."
    )
    basicFilter: BasicFilter = Field(
        ..., description="The filter on this sheet, if any."
    )
    charts: List[EmbeddedChart] = Field(
        ..., description="The specifications of every chart on this sheet."
    )
    bandedRanges: List[BandedRange] = Field(
        ..., description="The banded (alternating colors) ranges on this sheet."
    )
    developerMetadata: List[DeveloperMetadata] = Field(
        ..., description="The developer metadata associated with a sheet."
    )
    rowGroups: List[DimensionGroup] = Field(
        ...,
        description="All row groups on this sheet, ordered by increasing range start index, then by group depth.",
    )
    columnGroups: List[DimensionGroup] = Field(
        ...,
        description="All column groups on this sheet, ordered by increasing range start index, then by group depth.",
    )
    slicers: List[Slicer] = Field(..., description="The slicers on this sheet.")
    tables: List[Table] = Field(..., description="The tables on this sheet.")


class Spreadsheet(BaseModel):
    spreadsheetId: Optional[str] = Field(..., description="The ID of the spreadsheet. This field is read-only.")
    properties: SpreadsheetProperties = Field(..., description="Overall properties of a spreadsheet.")
    sheets: Optional[List[Sheet]] = Field(..., description="The sheets that are part of a spreadsheet.")
    namedRanges: Optional[List[NamedRange]] = Field(..., description="The named ranges defined in a spreadsheet.")
    spreadsheetUrl: Optional[str] = Field(..., description="The url of the spreadsheet. This field is read-only.")
    developerMetadata: Optional[List[DeveloperMetadata]] = Field(..., description="The developer metadata associated with a spreadsheet.")
    dataSources: Optional[List[DataSource]] = Field(..., description="A list of external data sources connected with the spreadsheet.")
    dataSourceSchedules: Optional[List[DataSourceRefreshSchedule]] = Field(..., description="Output only. A list of data source refresh schedules.")


class DateTimeRenderOption(Enum):
    SERIAL_NUMBER = "SERIAL_NUMBER"
    FORMATTED_STRING = "FORMATTED_STRING"


class DeveloperMetadataLocationMatchingStrategy(Enum):
    DEVELOPER_METADATA_LOCATION_MATCHING_STRATEGY_UNSPECIFIED = (
        "DEVELOPER_METADATA_LOCATION_MATCHING_STRATEGY_UNSPECIFIED"
    )
    EXACT_LOCATION = "EXACT_LOCATION"
    INTERSECTING_LOCATION = "INTERSECTING_LOCATION"


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
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root properties is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )
    range: DimensionRange = Field(..., description="The rows or columns to update.")
    dataSourceSheetRange: DataSourceSheetDimensionRange = Field(
        ..., description="The columns on a data source sheet to update."
    )


class UpdateNamedRangeRequest(BaseModel):
    namedRange: NamedRange = Field(
        ..., description="The named range to update with the new properties."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root namedRange is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class RepeatCellRequest(BaseModel):
    range: GridRange = Field(..., description="The range to repeat the cell in.")
    cell: CellData = Field(..., description="The data to write.")
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root cell is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class AddNamedRangeRequest(BaseModel):
    namedRange: NamedRange = Field(
        ...,
        description="The named range to add. The namedRangeId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a range that already exists.)",
    )


class DeleteNamedRangeRequest(BaseModel):
    namedRangeId: str = Field(..., description="The ID of the named range to delete.")


class AddSheetRequest(BaseModel):
    properties: SheetProperties = Field(
        ...,
        description="The properties the new sheet should have. All properties are optional. The sheetId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a sheet that already exists.)",
    )


class DeleteSheetRequest(BaseModel):
    sheetId: int = Field(..., description="The ID of the sheet to delete.")


class SourceAndDestination(BaseModel):
    source: GridRange = Field(
        ...,
        description="The location of the data to use as the source of the autofill.",
    )
    dimension: Dimension = Field(
        ..., description="The dimension that data should be filled into."
    )
    fillLength: int = Field(
        ...,
        description="The number of rows or columns that data should be filled into. Positive numbers expand beyond the last row or last column of the source. Negative numbers expand before the first row or first column of the source.",
    )


class AutoFillRequest(BaseModel):
    useAlternateSeries: bool = Field(
        ...,
        description="True if we should generate data with the 'alternate' series. This differs based on the type and amount of source data.",
    )
    range: GridRange = Field(
        ...,
        description="The range to autofill. This will examine the range and detect the location that has data and automatically fill that data in to the rest of the range.",
    )
    sourceAndDestination: SourceAndDestination = Field(
        ...,
        description="The source and destination areas to autofill. This explicitly lists the source of the autofill and where to extend that data.",
    )


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
    destination: GridCoordinate = Field(
        ..., description="The top-left coordinate where the data should be pasted."
    )
    pasteType: PasteType = Field(
        ...,
        description="What kind of data to paste. All the source data will be cut, regardless of what is pasted.",
    )


class PasteOrientation(Enum):
    NORMAL = "NORMAL"
    TRANSPOSE = "TRANSPOSE"


class CopyPasteRequest(BaseModel):
    source: GridRange = Field(..., description="The source range to copy.")
    destination: GridRange = Field(
        ...,
        description="The location to paste to. If the range covers a span that's a multiple of the source's height or width, then the data will be repeated to fill in the destination range. If the range is smaller than the source range, the entire source data will still be copied (beyond the end of the destination range).",
    )
    pasteType: PasteType = Field(..., description="What kind of data to paste.")
    pasteOrientation: PasteOrientation = Field(
        ..., description="How that data should be oriented when pasting."
    )


class MergeType(Enum):
    MERGE_ALL = "MERGE_ALL"
    MERGE_COLUMNS = "MERGE_COLUMNS"
    MERGE_ROWS = "MERGE_ROWS"


class MergeCellsRequest(BaseModel):
    range: GridRange = Field(..., description="The range of cells to merge.")
    mergeType: MergeType = Field(..., description="How the cells should be merged.")


class UnmergeCellsRequest(BaseModel):
    range: GridRange = Field(
        ...,
        description="The range within which all cells should be unmerged. If the range spans multiple merges, all will be unmerged. The range must not partially span any merge.",
    )


class UpdateBordersRequest(BaseModel):
    range: GridRange = Field(
        ..., description="The range whose borders should be updated."
    )
    top: Border = Field(..., description="The border to put at the top of the range.")
    bottom: Border = Field(
        ..., description="The border to put at the bottom of the range."
    )
    left: Border = Field(..., description="The border to put at the left of the range.")
    right: Border = Field(
        ..., description="The border to put at the right of the range."
    )
    innerHorizontal: Border = Field(
        ..., description="The horizontal border to put within the range."
    )
    innerVertical: Border = Field(
        ..., description="The vertical border to put within the range."
    )


class UpdateCellsRequest(BaseModel):
    rows: List[RowData] = Field(..., description="The data to write.")
    fields: str = Field(
        ...,
        description="The fields of CellData that should be updated. At least one field must be specified. The root is the CellData; 'row.values.' should not be specified. A single '*' can be used as short-hand for listing every field.",
    )
    start: GridCoordinate = Field(
        ...,
        description="The coordinate to start writing data at. Any number of rows and columns (including a different number of columns per row) may be written.",
    )
    range: GridRange = Field(
        ...,
        description="The range to write data to. If the data in rows does not cover the entire requested range, the fields matching those set in fields will be cleared.",
    )


class AddFilterViewRequest(BaseModel):
    filter: FilterView = Field(
        ...,
        description="The filter to add. The filterViewId field is optional. If one is not set, an ID will be randomly generated. (It is an error to specify the ID of a filter that already exists.)",
    )


class AppendCellsRequest(BaseModel):
    sheetId: int = Field(..., description="The sheet ID to append the data to.")
    rows: List[RowData] = Field(..., description="The data to append.")
    fields: str = Field(
        ...,
        description="The fields of CellData that should be updated. At least one field must be specified. The root is the CellData; 'row.values.' should not be specified. A single '*' can be used as short-hand for listing every field.",
    )
    tableId: str = Field(
        ...,
        description="The ID of the table to append data to. The data will be only appended to the table body.",
    )


class ClearBasicFilterRequest(BaseModel):
    sheetId: int = Field(
        ..., description="The sheet ID on which the basic filter should be cleared."
    )


class DeleteDimensionRequest(BaseModel):
    range: DimensionRange = Field(
        ..., description="The dimensions to delete from the sheet."
    )


class DeleteEmbeddedObjectRequest(BaseModel):
    objectId: int = Field(..., description="The ID of the embedded object to delete.")


class DeleteFilterViewRequest(BaseModel):
    filterId: int = Field(..., description="The ID of the filter to delete.")


class DuplicateFilterViewRequest(BaseModel):
    filterId: int = Field(..., description="The ID of the filter being duplicated.")


class DuplicateSheetRequest(BaseModel):
    sourceSheetId: int = Field(..., description="The sheet to duplicate.")
    insertSheetIndex: int = Field(
        ...,
        description="The zero-based index where the new sheet should be inserted. The index of all sheets after this are incremented.",
    )
    newSheetId: int = Field(
        ...,
        description="If set, the ID of the new sheet. If not set, an ID is chosen. If set, the ID must not conflict with any existing sheet ID. If set, it must be non-negative.",
    )
    newSheetName: str = Field(
        ...,
        description="The name of the new sheet. If empty, a new name is chosen for you.",
    )


class FindReplaceRequest(BaseModel):
    find: str = Field(..., description="The value to search.")
    replacement: str = Field(..., description="The value to use as the replacement.")
    matchCase: bool = Field(..., description="True if the search is case sensitive.")
    matchEntireCell: bool = Field(
        ..., description="True if the find value should match the entire cell."
    )
    searchByRegex: bool = Field(..., description="True if the find value is a regex.")
    includeFormulas: bool = Field(
        ...,
        description="True if the search should include cells with formulas. False to skip cells with formulas.",
    )
    range: GridRange = Field(..., description="The range to find/replace over.")
    sheetId: int = Field(..., description="The sheet to find/replace over.")
    allSheets: bool = Field(..., description="True to find/replace over all sheets.")


class InsertDimensionRequest(BaseModel):
    range: DimensionRange = Field(
        ...,
        description="The dimensions to insert. Both the start and end indexes must be bounded.",
    )
    inheritFromBefore: bool = Field(
        ...,
        description="Whether dimension properties should be extended from the dimensions before or after the newly inserted dimensions. True to inherit from the dimensions before (in which case the start index must be greater than 0), and false to inherit from the dimensions after.",
    )


class InsertRangeRequest(BaseModel):
    range: GridRange = Field(
        ...,
        description="The range to insert new cells into. The range is constrained to the current sheet boundaries.",
    )
    shiftDimension: Dimension = Field(
        ...,
        description="The dimension which will be shifted when inserting cells. If ROWS, existing cells will be shifted down. If COLUMNS, existing cells will be shifted right.",
    )


class MoveDimensionRequest(BaseModel):
    source: DimensionRange = Field(..., description="The source dimensions to move.")
    destinationIndex: int = Field(
        ...,
        description="The zero-based start index of where to move the source data to, based on the coordinates before the source data is removed from the grid. Existing data will be shifted down or right (depending on the dimension) to make room for the moved dimensions. The source dimensions are removed from the grid, so the the data may end up in a different index than specified.",
    )


class UpdateEmbeddedObjectPositionRequest(BaseModel):
    objectId: int = Field(..., description="The ID of the object to moved.")
    newPosition: EmbeddedObjectPosition = Field(
        ...,
        description="An explicit position to move the embedded object to. If newPosition.sheetId is set, a new sheet with that ID will be created. If newPosition.newSheet is set to true, a new sheet will be created with an ID that will be chosen for you.",
    )
    fields: str = Field(
        ...,
        description="The fields of OverlayPosition that should be updated when setting a new position. Used only if newPosition.overlayPosition is set, in which case at least one field must be specified. The root newPosition.overlayPosition is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class PasteDataRequest(BaseModel):
    coordinate: GridCoordinate = Field(
        ..., description="The coordinate at which the data should start being inserted."
    )
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
    source: GridRange = Field(
        ..., description="The source data range. This must span exactly one column."
    )
    delimiter: str = Field(
        ..., description="The delimiter to use. Used only if delimiterType is CUSTOM."
    )
    delimiterType: DelimiterType = Field(..., description="The delimiter type to use.")


class UpdateFilterViewRequest(BaseModel):
    filter: FilterView = Field(
        ..., description="The new properties of the filter view."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root filter is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class DeleteRangeRequest(BaseModel):
    range: GridRange = Field(..., description="The range of cells to delete.")
    shiftDimension: Dimension = Field(
        ...,
        description="The dimension from which deleted cells will be replaced with. If ROWS, existing cells will be shifted upward to replace the deleted cells. If COLUMNS, existing cells will be shifted left to replace the deleted cells.",
    )


class AppendDimensionRequest(BaseModel):
    sheetId: int = Field(..., description="The sheet to append rows or columns to.")
    dimension: Dimension = Field(
        ..., description="Whether rows or columns should be appended."
    )
    length: int = Field(..., description="The number of rows or columns to append.")


class AddConditionalFormatRuleRequest(BaseModel):
    rule: ConditionalFormatRule = Field(..., description="The rule to add.")
    index: int = Field(
        ..., description="The zero-based index where the rule should be inserted."
    )


class UpdateConditionalFormatRuleRequest(BaseModel):
    index: int = Field(
        ...,
        description="The zero-based index of the rule that should be replaced or moved.",
    )
    sheetId: int = Field(
        ...,
        description="The zero-based index of the rule that should be replaced or moved.",
    )
    rule: ConditionalFormatRule = Field(
        ..., description="The rule that should replace the rule at the given index."
    )
    newIndex: int = Field(
        ..., description="The zero-based new index the rule should end up at."
    )


class DeleteConditionalFormatRuleRequest(BaseModel):
    index: int = Field(
        ..., description="The zero-based index of the rule to be deleted."
    )
    sheetId: int = Field(..., description="The sheet the rule is being deleted from.")


class SortRangeRequest(BaseModel):
    range: GridRange = Field(..., description="The range to sort.")
    sortSpecs: List[SortSpec] = Field(
        ...,
        description="The sort order per column. Later specifications are used when values are equal in the earlier specifications.",
    )


class SetDataValidationRequest(BaseModel):
    range: GridRange = Field(
        ..., description="The range the data validation rule should apply to."
    )
    rule: DataValidationRule = Field(
        ...,
        description="The data validation rule to set on each cell in the range, or empty to clear the data validation in the range.",
    )
    filteredRowsIncluded: Optional[bool] = Field(
        ...,
        description="If true, the data validation rule will be applied to the filtered rows as well.",
    )


class SetBasicFilterRequest(BaseModel):
    filter: BasicFilter = Field(..., description="The filter to set.")


class AddProtectedRangeRequest(BaseModel):
    protectedRange: ProtectedRange = Field(
        ...,
        description="The protected range to be added. The protectedRangeId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a range that already exists.)",
    )


class UpdateProtectedRangeRequest(BaseModel):
    protectedRange: ProtectedRange = Field(
        ..., description="The protected range to update with the new properties."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root protectedRange is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class DeleteProtectedRangeRequest(BaseModel):
    protectedRangeId: int = Field(
        ..., description="The ID of the protected range to delete."
    )


class AutoResizeDimensionsRequest(BaseModel):
    dimensions: DimensionRange = Field(
        ..., description="The dimensions to automatically resize."
    )
    dataSourceSheetDimensions: DataSourceSheetDimensionRange = Field(
        ...,
        description="The dimensions on a data source sheet to automatically resize.",
    )


class AddChartRequest(BaseModel):
    chart: EmbeddedChart = Field(
        ...,
        description="The chart that should be added to the spreadsheet, including the position where it should be placed. The chartId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of an embedded object that already exists.)",
    )


class UpdateChartSpecRequest(BaseModel):
    chartId: int = Field(..., description="The ID of the chart to update.")
    spec: ChartSpec = Field(..., description="The specification to apply to the chart.")


class UpdateBandingRequest(BaseModel):
    bandedRange: BandedRange = Field(
        ..., description="The banded range to update with the new properties."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root bandedRange is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class AddBandingRequest(BaseModel):
    bandedRange: BandedRange = Field(
        ...,
        description="The banded range to add. The bandedRangeId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a range that already exists.)",
    )


class DeleteBandingRequest(BaseModel):
    bandedRangeId: int = Field(..., description="The ID of the banded range to delete.")


class CreateDeveloperMetadataRequest(BaseModel):
    developerMetadata: DeveloperMetadata = Field(
        ..., description="The developer metadata to create."
    )


class UpdateDeveloperMetadataRequest(BaseModel):
    dataFilters: List[DataFilter] = Field(
        ...,
        description="The filters matching the developer metadata entries to update.",
    )
    developerMetadata: DeveloperMetadata = Field(
        ...,
        description="The value that all metadata matched by the data filters will be updated to.",
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root developerMetadata is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class DeleteDeveloperMetadataRequest(BaseModel):
    dataFilter: DataFilter = Field(
        ...,
        description="The data filter describing the criteria used to select which developer metadata entry to delete.",
    )


class RandomizeRangeRequest(BaseModel):
    range: GridRange = Field(..., description="The range to randomize.")


class AddDimensionGroupRequest(BaseModel):
    range: DimensionRange = Field(
        ..., description="The range over which to create a group."
    )


class DeleteDimensionGroupRequest(BaseModel):
    range: DimensionRange = Field(
        ..., description="The range of the group to be deleted."
    )


class UpdateDimensionGroupRequest(BaseModel):
    dimensionGroup: DimensionGroup = Field(
        ...,
        description="The group whose state should be updated. The range and depth of the group should specify a valid group on the sheet, and all other fields updated.",
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root dimensionGroup is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class TrimWhitespaceRequest(BaseModel):
    range: GridRange = Field(..., description="The range whose cells to trim.")


class DeleteDuplicatesRequest(BaseModel):
    range: GridRange = Field(
        ..., description="The range to remove duplicates rows from."
    )
    comparisonColumns: List[DimensionRange] = Field(
        ...,
        description="The columns in the range to analyze for duplicate values. If no columns are selected then all columns are analyzed for duplicates.",
    )


class UpdateEmbeddedObjectBorderRequest(BaseModel):
    objectId: int = Field(..., description="The ID of the embedded object to update.")
    border: EmbeddedObjectBorder = Field(
        ..., description="The border that applies to the embedded object."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root border is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class AddSlicerRequest(BaseModel):
    slicer: Slicer = Field(
        ...,
        description="The slicer that should be added to the spreadsheet, including the position where it should be placed. The slicerId field is optional; if one is not set, an id will be randomly generated. (It is an error to specify the ID of a slicer that already exists.)",
    )


class UpdateSlicerSpecRequest(BaseModel):
    slicerId: int = Field(..., description="The id of the slicer to update.")
    spec: SlicerSpec = Field(
        ..., description="The specification to apply to the slicer."
    )
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root SlicerSpec is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class AddDataSourceRequest(BaseModel):
    dataSource: DataSource = Field(..., description="The data source to add.")


class UpdateDataSourceRequest(BaseModel):
    dataSource: DataSource = Field(..., description="The data source to update.")
    fields: str = Field(
        ...,
        description="The fields that should be updated. At least one field must be specified. The root dataSource is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class DeleteDataSourceRequest(BaseModel):
    dataSourceId: str = Field(..., description="The ID of the data source to delete.")


class DataSourceObjectReference(BaseModel):
    sheetId: str = Field(..., description="References to a DATA_SOURCE sheet.")
    chartId: int = Field(..., description="References to a data source chart.")
    dataSourceTableAnchorCell: GridCoordinate = Field(
        ..., description="References to a DataSourceTable anchored at the cell."
    )
    dataSourcePivotTableAnchorCell: GridCoordinate = Field(
        ..., description="References to a data source PivotTable anchored at the cell."
    )
    dataSourceFormulaCell: GridCoordinate = Field(
        ..., description="References to a cell containing DataSourceFormula."
    )


class DataSourceObjectReferences(BaseModel):
    references: List[DataSourceObjectReference] = Field(
        ..., description="The references."
    )


class RefreshDataSourceRequest(BaseModel):
    force: bool = Field(
        ...,
        description="Refreshes the data source objects regardless of the current state. If not set and a referenced data source object was in error state, the refresh will fail immediately.",
    )
    references: DataSourceObjectReferences = Field(
        ..., description="References to data source objects to refresh."
    )
    dataSourceId: str = Field(
        ...,
        description="Reference to a DataSource. If specified, refreshes all associated data source objects for the data source.",
    )
    isAll: bool = Field(
        ...,
        description="Refreshes all existing data source objects in the spreadsheet.",
    )


class CancelDataSourceRefreshRequest(BaseModel):
    references: DataSourceObjectReferences = Field(
        ...,
        description="References to data source objects whose refreshes are to be cancelled.",
    )
    dataSourceId: str = Field(
        ...,
        description="Reference to a DataSource. If specified, cancels all associated data source object refreshes for this data source.",
    )
    isAll: bool = Field(
        ...,
        description="Cancels all existing data source object refreshes for all data sources in the spreadsheet.",
    )


class AddTableRequest(BaseModel):
    table: Table = Field(..., description="Required. The table to add.")


class UpdateTableRequest(BaseModel):
    table: Table = Field(..., description="Required. The table to update.")
    fields: str = Field(
        ...,
        description="Required. The fields that should be updated. At least one field must be specified. The root table is implied and should not be specified. A single '*' can be used as short-hand for listing every field.",
    )


class DeleteTableRequest(BaseModel):
    tableId: str = Field(..., description="The ID of the table to delete.")


class Request(BaseModel):
    updateSpreadsheetProperties: UpdateSpreadsheetPropertiesRequest = Field(
        ..., description="Updates the spreadsheet's properties."
    )
    updateSheetProperties: UpdateSheetPropertiesRequest = Field(
        ..., description="Updates a sheet's properties."
    )
    updateDimensionProperties: UpdateDimensionPropertiesRequest = Field(
        ..., description="Updates dimensions' properties."
    )
    updateNamedRange: UpdateNamedRangeRequest = Field(
        ..., description="Updates a named range."
    )
    repeatCell: RepeatCellRequest = Field(
        ..., description="Repeats a single cell across a range."
    )
    addNamedRange: AddNamedRangeRequest = Field(..., description="Adds a named range.")
    deleteNamedRange: DeleteNamedRangeRequest = Field(
        ..., description="Deletes a named range."
    )
    addSheet: AddSheetRequest = Field(..., description="Adds a sheet.")
    deleteSheet: DeleteSheetRequest = Field(..., description="Deletes a sheet.")
    autoFill: AutoFillRequest = Field(
        ..., description="Automatically fills in more data based on existing data."
    )
    cutPaste: CutPasteRequest = Field(
        ..., description="Cuts data from one area and pastes it to another."
    )
    copyPaste: CopyPasteRequest = Field(
        ..., description="Copies data from one area and pastes it to another."
    )
    mergeCells: MergeCellsRequest = Field(..., description="Merges cells together.")
    unmergeCells: UnmergeCellsRequest = Field(..., description="Unmerges merged cells.")
    updateBorders: UpdateBordersRequest = Field(
        ..., description="Updates the borders in a range of cells."
    )
    updateCells: UpdateCellsRequest = Field(
        ..., description="Updates many cells at once."
    )
    addFilterView: AddFilterViewRequest = Field(..., description="Adds a filter view.")
    appendCells: AppendCellsRequest = Field(
        ..., description="Appends cells after the last row with data in a sheet."
    )
    clearBasicFilter: ClearBasicFilterRequest = Field(
        ..., description="Clears the basic filter on a sheet."
    )
    deleteDimension: DeleteDimensionRequest = Field(
        ..., description="Deletes rows or columns in a sheet."
    )
    deleteEmbeddedObject: DeleteEmbeddedObjectRequest = Field(
        ..., description="Deletes an embedded object (e.g, chart, image) in a sheet."
    )
    deleteFilterView: DeleteFilterViewRequest = Field(
        ..., description="Deletes a filter view from a sheet."
    )
    duplicateFilterView: DuplicateFilterViewRequest = Field(
        ..., description="Duplicates a filter view."
    )
    duplicateSheet: DuplicateSheetRequest = Field(
        ..., description="Duplicates a sheet."
    )
    findReplace: FindReplaceRequest = Field(
        ..., description="Finds and replaces occurrences of some text with other text."
    )
    insertDimension: InsertDimensionRequest = Field(
        ..., description="Inserts new rows or columns in a sheet."
    )
    insertRange: InsertRangeRequest = Field(
        ..., description="Inserts new cells in a sheet, shifting the existing cells."
    )
    moveDimension: MoveDimensionRequest = Field(
        ..., description="Moves rows or columns to another location in a sheet."
    )
    updateEmbeddedObjectPosition: UpdateEmbeddedObjectPositionRequest = Field(
        ..., description="Updates an embedded object's (e.g. chart, image) position."
    )
    pasteData: PasteDataRequest = Field(
        ..., description="Pastes data (HTML or delimited) into a sheet."
    )
    textToColumns: TextToColumnsRequest = Field(
        ..., description="Converts a column of text into many columns of text."
    )
    updateFilterView: UpdateFilterViewRequest = Field(
        ..., description="Updates the properties of a filter view."
    )
    deleteRange: DeleteRangeRequest = Field(
        ...,
        description="Deletes a range of cells from a sheet, shifting the remaining cells.",
    )
    appendDimension: AppendDimensionRequest = Field(
        ..., description="Appends dimensions to the end of a sheet."
    )
    addConditionalFormatRule: AddConditionalFormatRuleRequest = Field(
        ..., description="Adds a new conditional format rule."
    )
    updateConditionalFormatRule: UpdateConditionalFormatRuleRequest = Field(
        ..., description="Updates an existing conditional format rule."
    )
    deleteConditionalFormatRule: DeleteConditionalFormatRuleRequest = Field(
        ..., description="Deletes an existing conditional format rule."
    )
    sortRange: SortRangeRequest = Field(..., description="Sorts data in a range.")
    setDataValidation: SetDataValidationRequest = Field(
        ..., description="Sets data validation for one or more cells."
    )
    setBasicFilter: SetBasicFilterRequest = Field(
        ..., description="Sets the basic filter on a sheet."
    )
    addProtectedRange: AddProtectedRangeRequest = Field(
        ..., description="Adds a protected range."
    )
    updateProtectedRange: UpdateProtectedRangeRequest = Field(
        ..., description="Updates a protected range."
    )
    deleteProtectedRange: DeleteProtectedRangeRequest = Field(
        ..., description="Deletes a protected range."
    )
    autoResizeDimensions: AutoResizeDimensionsRequest = Field(
        ...,
        description="Automatically resizes one or more dimensions based on the contents of the cells in that dimension.",
    )
    addChart: AddChartRequest = Field(..., description="Adds a chart.")
    updateChartSpec: UpdateChartSpecRequest = Field(
        ..., description="Updates a chart's specifications."
    )
    updateBanding: UpdateBandingRequest = Field(
        ..., description="Updates a banded range"
    )
    addBanding: AddBandingRequest = Field(..., description="Adds a new banded range")
    deleteBanding: DeleteBandingRequest = Field(
        ..., description="Removes a banded range"
    )
    createDeveloperMetadata: CreateDeveloperMetadataRequest = Field(
        ..., description="Creates new developer metadata"
    )
    updateDeveloperMetadata: UpdateDeveloperMetadataRequest = Field(
        ..., description="Updates an existing developer metadata entry"
    )
    deleteDeveloperMetadata: DeleteDeveloperMetadataRequest = Field(
        ..., description="Deletes developer metadata"
    )
    randomizeRange: RandomizeRangeRequest = Field(
        ..., description="Randomizes the order of the rows in a range."
    )
    addDimensionGroup: AddDimensionGroupRequest = Field(
        ..., description="Creates a group over the specified range."
    )
    deleteDimensionGroup: DeleteDimensionGroupRequest = Field(
        ..., description="Deletes a group over the specified range."
    )
    updateDimensionGroup: UpdateDimensionGroupRequest = Field(
        ..., description="Updates the state of the specified group."
    )
    trimWhitespace: TrimWhitespaceRequest = Field(
        ...,
        description="Trims cells of whitespace (such as spaces, tabs, or new lines).",
    )
    deleteDuplicates: DeleteDuplicatesRequest = Field(
        ...,
        description="Removes rows containing duplicate values in specified columns of a cell range.",
    )
    updateEmbeddedObjectBorder: UpdateEmbeddedObjectBorderRequest = Field(
        ..., description="Updates an embedded object's border."
    )
    addSlicer: AddSlicerRequest = Field(..., description="Adds a slicer.")
    updateSlicerSpec: UpdateSlicerSpecRequest = Field(
        ..., description="Updates a slicer's specifications."
    )
    addDataSource: AddDataSourceRequest = Field(..., description="Adds a data source.")
    updateDataSource: UpdateDataSourceRequest = Field(
        ..., description="Updates a data source."
    )
    deleteDataSource: DeleteDataSourceRequest = Field(
        ..., description="Deletes a data source."
    )
    refreshDataSource: RefreshDataSourceRequest = Field(
        ...,
        description="Refreshes one or multiple data sources and associated dbobjects.",
    )
    cancelDataSourceRefresh: CancelDataSourceRefreshRequest = Field(
        ...,
        description="Cancels refreshes of one or multiple data sources and associated dbobjects.",
    )
    addTable: AddTableRequest = Field(..., description="Adds a table.")
    updateTable: UpdateTableRequest = Field(..., description="Updates a table.")
    deleteTable: DeleteTableRequest = Field(
        ..., description="A request for deleting a table."
    )


class AddNamedRangeResponse(BaseModel):
    namedRange: NamedRange = Field(..., description="The named range to add.")


class AddSheetResponse(BaseModel):
    properties: SheetProperties = Field(
        ..., description="The properties of the newly added sheet."
    )


class AddFilterViewResponse(BaseModel):
    filter: FilterView = Field(..., description="The newly added filter view.")


class DuplicateFilterViewResponse(BaseModel):
    filter: FilterView = Field(..., description="The newly created filter.")


class DuplicateSheetResponse(BaseModel):
    properties: SheetProperties = Field(
        ..., description="The properties of the duplicate sheet."
    )


class FindReplaceResponse(BaseModel):
    valuesChanged: int = Field(
        ..., description="The number of non-formula cells changed."
    )
    formulasChanged: int = Field(
        ..., description="The number of formula cells changed."
    )
    rowsChanged: int = Field(..., description="The number of rows changed.")
    sheetsChanged: int = Field(..., description="The number of sheets changed.")
    occurrencesChanged: int = Field(
        ...,
        description="The number of occurrences (possibly multiple within a cell) changed.",
    )


class UpdateEmbeddedObjectPositionResponse(BaseModel):
    position: EmbeddedObjectPosition = Field(
        ..., description="The new position of the embedded object."
    )


class UpdateConditionalFormatRuleResponse(BaseModel):
    newrule: ConditionalFormatRule = Field(
        ...,
        description="The new rule that replaced the old rule (if replacing), or the rule that was moved (if moved)",
    )
    newIndex: int = Field(..., description="The index of the new rule.")
    oldRule: Optional[ConditionalFormatRule] = Field(
        ...,
        description="The old (deleted) rule. Not set if a rule was moved (because it is the same as newRule).",
    )
    oldIndex: Optional[int] = Field(
        ...,
        description="The old index of the rule. Not set if a rule was replaced (because it is the same as newIndex).",
    )


class DeleteConditionalFormatRuleResponse(BaseModel):
    rule: ConditionalFormatRule = Field(..., description="The rule that was deleted.")


class AddProtectedRangeResponse(BaseModel):
    protectedRange: ProtectedRange = Field(
        ..., description="The newly added protected range."
    )


class AddChartResponse(BaseModel):
    chart: EmbeddedChart = Field(..., description="The newly added chart.")


class AddBandingResponse(BaseModel):
    bandedRange: BandedRange = Field(
        ..., description="The banded range that was added."
    )


class CreateDeveloperMetadataResponse(BaseModel):
    developerMetadata: DeveloperMetadata = Field(
        ..., description="The developer metadata that was created."
    )


class UpdateDeveloperMetadataResponse(BaseModel):
    developerMetadata: DeveloperMetadata = Field(
        ..., description="The updated developer metadata."
    )


class DeleteDeveloperMetadataResponse(BaseModel):
    deletedDeveloperMetadata: List[DeveloperMetadata] = Field(
        ..., description="The metadata that was deleted."
    )


class AddDimensionGroupResponse(BaseModel):
    dimensionGroups: List[DimensionGroup] = Field(
        ...,
        description="All groups of a dimension after adding a group to that dimension.",
    )


class DeleteDimensionGroupResponse(BaseModel):
    dimensionGroups: List[DimensionGroup] = Field(
        ...,
        description="All groups of a dimension after deleting a group from that dimension.",
    )


class TrimWhitespaceResponse(BaseModel):
    cellsChangedCount: int = Field(
        ..., description="The number of cells that were trimmed of whitespace."
    )


class DeleteDuplicatesResponse(BaseModel):
    duplicatesRemovedCount: int = Field(
        ..., description="The number of duplicate rows removed."
    )


class AddSlicerResponse(BaseModel):
    slicer: Slicer = Field(..., description="The newly added slicer.")


class AddDataSourceResponse(BaseModel):
    dataSource: DataSource = Field(..., description="The data source that was created.")
    dataExecutionStatus: DataExecutionStatus = Field(
        ..., description="The data execution status."
    )


class UpdateDataSourceResponse(BaseModel):
    dataSource: DataSource = Field(..., description="The updated data source.")
    dataExecutionStatus: DataExecutionStatus = Field(
        ..., description="The data execution status."
    )


class RefreshDataSourceObjectExecutionStatus(BaseModel):
    reference: DataSourceObjectReference = Field(
        ..., description="Reference to a data source object being refreshed."
    )
    dataExecutionStatus: DataExecutionStatus = Field(
        ..., description="The data execution status."
    )


class RefreshDataSourceResponse(BaseModel):
    statuses: List[RefreshDataSourceObjectExecutionStatus] = Field(
        ...,
        description="All the refresh status for the data source object references specified in the request. If isAll is specified, the field contains only those in failure status.",
    )


class RefreshCancellationState(Enum):
    REFRESH_CANCELLATION_STATE_UNSPECIFIED = "REFRESH_CANCELLATION_STATE_UNSPECIFIED"
    CANCEL_SUCCEEDED = "CANCEL_SUCCEEDED"
    CANCEL_FAILED = "CANCEL_FAILED"


class RefreshCancellationErrorCode(Enum):
    REFRESH_CANCELLATION_ERROR_CODE_UNSPECIFIED = (
        "REFRESH_CANCELLATION_ERROR_CODE_UNSPECIFIED"
    )
    EXECUTION_NOT_FOUND = "EXECUTION_NOT_FOUND"
    CANCEL_PERMISSION_DENIED = "CANCEL_PERMISSION_DENIED"
    QUERY_EXECUTION_COMPLETED = "QUERY_EXECUTION_COMPLETED"
    CONCURRENT_CANCELLATION = "CONCURRENT_CANCELLATION"
    CANCEL_OTHER_ERROR = "CANCEL_OTHER_ERROR"


class RefreshCancellationStatus(BaseModel):
    state: RefreshCancellationState = Field(
        ..., description="The state of a call to cancel a refresh in Sheets."
    )
    errorCode: RefreshCancellationErrorCode = Field(..., description="The error code.")


class CancelDataSourceRefreshStatus(BaseModel):
    reference: DataSourceObjectReference = Field(
        ...,
        description="Reference to the data source object whose refresh is being cancelled.",
    )
    refreshCancellationStatus: RefreshCancellationStatus = Field(
        ..., description="The cancellation status."
    )


class CancelDataSourceRefreshResponse(BaseModel):
    statuses: List[CancelDataSourceRefreshStatus] = Field(
        ...,
        description="The cancellation statuses of refreshes of all data source objects specified in the request. If isAll is specified, the field contains only those in failure status. Refreshing and canceling refresh the same data source object is also not allowed in the same batchUpdate.",
    )


class AddTableResponse(BaseModel):
    table: Table = Field(..., description="Output only. The table that was added.")


class Response(BaseModel):
    addNamedRange: AddNamedRangeResponse = Field(
        ..., description="A reply from adding a named range."
    )
    addSheet: AddSheetResponse = Field(..., description="A reply from adding a sheet.")
    addFilterView: AddFilterViewResponse = Field(
        ..., description="A reply from adding a filter view."
    )
    duplicateFilterView: DuplicateFilterViewResponse = Field(
        ..., description="A reply from duplicating a filter view."
    )
    duplicateSheet: DuplicateSheetResponse = Field(
        ..., description="A reply from duplicating a sheet."
    )
    findReplace: FindReplaceResponse = Field(
        ..., description="A reply from doing a find/replace."
    )
    updateEmbeddedObjectPosition: UpdateEmbeddedObjectPositionResponse = Field(
        ..., description="A reply from updating an embedded object's position."
    )
    updateConditionalFormatRule: UpdateConditionalFormatRuleResponse = Field(
        ..., description="A reply from updating a conditional format rule."
    )
    deleteConditionalFormatRule: DeleteConditionalFormatRuleResponse = Field(
        ..., description="A reply from deleting a conditional format rule."
    )
    addProtectedRange: AddProtectedRangeResponse = Field(
        ..., description="A reply from adding a protected range."
    )
    addChart: AddChartResponse = Field(..., description="A reply from adding a chart.")
    addBanding: AddBandingResponse = Field(
        ..., description="A reply from adding a banded range."
    )
    createDeveloperMetadata: CreateDeveloperMetadataResponse = Field(
        ..., description="A reply from creating a developer metadata entry."
    )
    updateDeveloperMetadata: UpdateDeveloperMetadataResponse = Field(
        ..., description="A reply from updating a developer metadata entry."
    )
    deleteDeveloperMetadata: DeleteDeveloperMetadataResponse = Field(
        ..., description="A reply from deleting a developer metadata entry."
    )
    addDimensionGroup: AddDimensionGroupResponse = Field(
        ..., description="A reply from adding a dimension group."
    )
    deleteDimensionGroup: DeleteDimensionGroupResponse = Field(
        ..., description="A reply from deleting a dimension group."
    )
    trimWhitespace: TrimWhitespaceResponse = Field(
        ..., description="A reply from trimming whitespace."
    )
    deleteDuplicates: DeleteDuplicatesResponse = Field(
        ..., description="A reply from removing rows containing duplicate values."
    )
    addSlicer: AddSlicerResponse = Field(
        ..., description="A reply from adding a slicer."
    )
    addDataSource: AddDataSourceResponse = Field(
        ..., description="A reply from adding a data source."
    )
    updateDataSource: UpdateDataSourceResponse = Field(
        ..., description="A reply from updating a data source."
    )
    refreshDataSource: RefreshDataSourceResponse = Field(
        ..., description="A reply from refreshing data source objects."
    )
    cancelDataSourceRefresh: CancelDataSourceRefreshResponse = Field(
        ..., description="A reply from cancelling data source object refreshes."
    )
    addTable: AddTableResponse = Field(..., description="A reply from adding a table.")
