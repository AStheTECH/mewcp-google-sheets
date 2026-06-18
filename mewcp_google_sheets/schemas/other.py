from enum import Enum
from typing import List

from pydantic import BaseModel, Field


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


class SortOrder(Enum):
    SORT_ORDER_UNSPECIFIED = "SORT_ORDER_UNSPECIFIED"
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


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
    foregroundColorStyle: ColorStyle = Field(..., description="The foreground color to sort by; cells with this foreground color are sorted to the top. Mutually exclusive with backgroundColor, and must be an RGB-type color.")
    backgroundColorStyle: ColorStyle = Field(..., description="The background fill color to sort by; cells with this fill color are sorted to the top. Mutually exclusive with foregroundColor, and must be an RGB-type color.")
    dimensionIndex: int = Field(..., description="The dimension the sort should be applied to.")
    dataSourceColumnReference: DataSourceColumnReference = Field(..., description="Reference to a data source column")


class GridCoordinate(BaseModel):
    sheetId: int = Field(..., description="The sheet this coordinate is on.")
    rowIndex: int = Field(..., description="The row index of the coordinate.")
    columnIndex: int = Field(..., description="The column index of the coordinate.")

class OverlayPosition(BaseModel):
    anchorCell: GridCoordinate = Field(..., description="The cell the object is anchored to.")
    offsetXPixels: int = Field(..., description="The horizontal offset, in pixels, that the object is offset from the anchor cell.")
    offsetYPixels: int = Field(..., description="The vertical offset, in pixels, that the object is offset from the anchor cell.")
    widthPixels: int = Field(..., description="The width of the object, in pixels. Defaults to 600.")
    heightPixels: int = Field(..., description="The height of the object, in pixels. Defaults to 371.")

class EmbeddedObjectPosition(BaseModel):
    sheetId: int = Field(..., description="The sheet this is on. Set only if the embedded object is on its own sheet. Must be non-negative")
    overlayPosition: OverlayPosition = Field(..., description="The position at which the object is overlaid on top of a grid.")
    newSheet: bool = Field(..., description="If true, the embedded object is put on a new sheet whose ID is chosen for you. Used only when writing.")
