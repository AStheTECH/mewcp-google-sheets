from enum import Enum
from typing import List
from pydantic import BaseModel, Field

from .other import (
    ExtendedValue,
    ColorStyle,
    BooleanCondition,
    HorizontalAlign,
    TextFormat,
    DataExecutionStatus,
    DataSourceColumnReference,
    FilterSpec,
    SortSpec
)

from .pivot_tables import (
    PivotTable
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
    condition: BooleanCondition = Field(..., description="The condition that data in the cell must match.")
    inputMessage: str = Field(..., description="A message to show the user when adding data to the cell.")
    strict: bool = Field(..., description="True if invalid data should be rejected.")
    showCustomUi: bool = Field(..., description="True if the UI should be customized based on the kind of condition. If true, 'List' conditions will show a dropdown.")


class DataSourceTableColumnSelectionType(Enum):
    DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED = "DATA_SOURCE_TABLE_COLUMN_SELECTION_TYPE_UNSPECIFIED"
    SELECTED = "SELECTED"
    SYNC_ALL = "SYNC_ALL"

class DataSourceFormula(BaseModel):
    dataSourceId: str = Field(..., description="The ID of the data source the formula is associated with.")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="Output only. The data execution status.")

class DataSourceTable(BaseModel):
    dataSourceId: str = Field(..., description="The ID of the data source the data source table is associated with.")
    columnSelectionType: DataSourceTableColumnSelectionType = Field(..., description="he type to select columns for the data source table. Defaults to SELECTED.")
    columns: List[DataSourceColumnReference] = Field(..., description="Columns selected for the data source table. The columnSelectionType must be SELECTED.")
    filterSpecs: List[FilterSpec] = Field(..., description="Filter specifications in the data source table.")
    sortSpec: List[SortSpec] = Field(..., description="Sort specifications in the data source table. The result of the data source table is sorted based on the sort specifications in order.")
    rowLimit: int = Field(..., description="The limit of rows to return. If not set, a default limit is applied. Please refer to the Sheets editor for the default and max limit.")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="Output only. The data execution status.")

class DisplayFormat(Enum):
    DISPLAY_FORMAT_UNSPECIFIED = "DISPLAY_FORMAT_UNSPECIFIED"
    DEFAULT = "DEFAULT"
    LAST_NAME_COMMA_FIRST_NAME = "LAST_NAME_COMMA_FIRST_NAME"
    EMAIL = "EMAIL"

class PersonProperties(BaseModel):
    email: str = Field(..., description="Required. The email address linked to this person. This field is always present.")
    displayFormat: DisplayFormat = Field(..., description="Optional. The display format of the person chip. If not set, the default display format is used.")


class RichLinkProperties(BaseModel):
    uri: str = Field(..., description="Required. The URI to the link. This is always present.")
    mimeType: str = Field(..., description="Output only. The MIME type of the link, if there's one (for example, when it's a file in Drive).")

class Chip(BaseModel):
    personProperties: PersonProperties = Field(..., description="Properties of a linked person.")
    richLinkProperties: RichLinkProperties = Field(..., description="Properties of a rich link.")

class ChipRun(BaseModel):
    startIndex: int = Field(..., description="Required. The zero-based character index where this run starts, in UTF-16 code units.")
    chip: Chip = Field(..., description="Optional. The chip of this run.")

class CellData(BaseModel):
    userEnteredValued: ExtendedValue = Field(..., description="The value the user entered in the cell.")
    effectiveValue: ExtendedValue = Field(..., description="The effective value of the cell. For cells with formulas, this is the calculated value. For cells with literals, this is the same as the userEnteredValue. This field is read-only.")
    formattedValue: str = Field(..., description="The formatted value of the cell. This is the value as it's shown to the user. This field is read-only.")
    userEnteredFormat: CellFormat = Field(..., description="The format the user entered for the cell. When writing, the new format will be merged with the existing format.")
    effectiveFormat: CellFormat = Field(..., description="The effective format being used by the cell. This includes the results of applying any conditional formatting and, if the cell contains a formula, the computed number format. If the effective format is the default format, effective format will not be written. This field is read-only.")
    hyperlink: str = Field(..., description="A hyperlink this cell points to, if any. If the cell contains multiple hyperlinks, this field will be empty. This field is read-only. To set it, use a =HYPERLINK formula in the userEnteredValue.formulaValue field. A cell-level link can also be set from the userEnteredFormat.textFormat field. Alternatively, set a hyperlink in the textFormatRun.format.link field that spans the entire cell.")
    note: str = Field(..., description="Any note on the cell.")
    textFormatRuns: TextFormatRun = Field(..., description="Runs of rich text applied to subsections of the cell. Runs are only valid on user entered strings, not formulas, bools, or numbers. Properties of a run start at a specific index in the text and continue until the next run. Runs will inherit the properties of the cell unless explicitly changed. When writing, the new runs will overwrite any prior runs. When writing a new userEnteredValue, previous runs are erased.")
    dataValidation: DataValidationRule = Field(..., description="A data validation rule on the cell, if any. When writing, the new data validation rule will overwrite any prior rule.")
    pivotTable: PivotTable = Field(..., description="A pivot table anchored at this cell. The size of pivot table itself is computed dynamically based on its data, grouping, filters, values, etc. Only the top-left cell of the pivot table contains the pivot table definition. The other cells will contain the calculated values of the results of the pivot in their effectiveValue fields.")
    dataSourceTable: DataSourceTable = Field(..., description="A data source table anchored at this cell. The size of data source table itself is computed dynamically based on its configuration. Only the first cell of the data source table contains the data source table definition. The other cells will contain the display values of the data source table result in their effectiveValue fields.")
    dataSourceFormula: DataSourceFormula = Field(..., description="Output only. Information about a data source formula on the cell. The field is set if userEnteredValue is a formula referencing some DATA_SOURCE sheet, e.g. =SUM(DataSheet!Column).")
    chipRuns: List[ChipRun] = Field(..., description="Optional. Runs of chips applied to subsections of the cell. Properties of a run start at a specific index in the text and continue until the next run. When reading, all chipped and non-chipped runs are included. Non-chipped runs will have an empty Chip. When writing, only runs with chips are included. Runs containing chips are of length 1 and are represented in the user-entered text by an “@” placeholder symbol. New runs will overwrite any prior runs. Writing a new userEnteredValue will erase previous runs.")
