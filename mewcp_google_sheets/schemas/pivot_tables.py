from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from other import (
    GridRange,
    DataExecutionStatus,
    ExtendedValue,
    SortOrder,
    DataSourceColumnReference,
    BooleanCondition,
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

class PivotFilterCriteria(BaseModel):
    visibleValues: List[str] = Field(..., description="Values that should be included. Values not listed here are excluded.")
    condition: BooleanCondition = Field(..., description="A condition that must be true for values to be shown. ( visibleValues does not override this -- even if a value is listed there, it is still hidden if it does not meet the condition.)")
    visibileByDefault: bool = Field(..., description="Whether values are visible by default. If true, the visibleValues are ignored, all values that meet condition (if specified) are shown. If false, values that are both in visibleValues and meet condition are shown.")

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
    groups: List[ManualRuleGroup] = Field(..., description="The list of group names and the corresponding items from the source data that map to each group name.")


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
    type: DateTimeRuleType = Field(..., description="The type of date-time grouping to apply.")

class PivotGroupRule(BaseModel):
    manualRule: ManualRule = Field(..., description="A ManualRule.")
    histogramRule: HistogramRule = Field(..., description="A HistogramRule.")
    dateTimeRule: DateTimeRule = Field(..., description="A DateTimeRule.")


class PivotGroupLimit(BaseModel):
    countLimit: int = Field(..., description="The count limit.")
    applyOrder: int = Field(..., description="The order in which the group limit is applied to the pivot table. Pivot group limits are applied from lower to higher order number. Order numbers are normalized to consecutive integers from 0.")

class PivotGroup(BaseModel):
    showTotals: bool = Field(..., description="True if the pivot table should include the totals for this grouping.")
    valueMetadata: PivotGroupValueMetadata = Field(..., description="Metadata about values in the grouping.")
    sortOrder: SortOrder = Field(..., description="The order the values in this group should be sorted.")
    valueBucket: PivotGroupSortValueBucket = Field(..., description="The bucket of the opposite pivot group to sort by. If not specified, sorting is alphabetical by this group's values.")
    repeatHeadings: bool = Field(..., description="True if the headings in this pivot group should be repeated. This is only valid for row groupings and is ignored by columns. By default, we minimize repetition of headings by not showing higher level headings where they are the same")
    label: str = Field(..., description="The labels to use for the row/column groups which can be customized. For example, in the following pivot table, the row label is Region (which could be renamed to State) and the column label is Product (which could be renamed Item).")
    groupRule: PivotGroupRule = Field(..., description="The group rule to apply to this row/column group.")
    groupLimit: PivotGroupLimit = Field(..., description="The count limit on rows or columns to apply to this pivot group.")
    sourceColumnOffset: int = Field(..., description="The column offset of the source range that this grouping is based on.")
    dataSourceColumnReference: DataSourceColumnReference = Field(..., description="The reference to the data source column this grouping is based on.")

class PivotFilterSpec(BaseModel):
    filterCriteria: PivotFilterCriteria = Field(..., description="The criteria for the column.")
    columnOffsetIndex: int = Field(..., description="The zero-based column offset of the source range.")
    dataSourceColumnReference: DataSourceColumnReference = Field(..., description="The reference to the data source column.")

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
    summarizeFunction: PivotValueSummarizeFunction = Field(..., description="A function to summarize the value. If formula is set, the only supported values are SUM and CUSTOM. If sourceColumnOffset is set, then CUSTOM is not supported.")
    name: str = Field(..., description="A name to use for the value.")
    calculatedDisplayType: PivotValueCalculatedDisplayType = Field(..., description="If specified, indicates that pivot values should be displayed as the result of a calculation with another pivot value.")
    sourceColumnOffset: int = Field(..., description="The column offset of the source range that this value reads from.")
    formula: str = Field(..., description="A custom formula to calculate the value. The formula must start with an = character.")
    dataSourceColumnReference: DataSourceColumnReference = Field(..., description="The reference to the data source column that this value reads from.")

class PivotValueLayout(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"

class PivotTable(BaseModel):
    rows: List[PivotGroup] = Field(...,  description="Each row grouping in the pivot table.")
    columns: List[PivotGroup] = Field(..., description="Each column grouping in the pivot table.")
    criteria: Dict[int, PivotFilterCriteria] = Field(..., description="An optional mapping of filters per source column offset.The filters are applied before aggregating data into the pivot table. The map's key is the column offset of the source range that you want to filter, and the value is the criteria for that column")
    filterSpecs: List[PivotFilterSpec] = Field(..., description="The filters applied to the source columns before aggregating data for the pivot table. Both criteria and filterSpecs are populated in responses. If both fields are specified in an update request, this field takes precedence.")
    values: List[PivotValue] = Field(..., description="A list of values to include in the pivot table.")
    valueLayout: PivotValueLayout = Field(..., description="Whether values should be listed horizontally (as columns) or vertically (as rows).")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="Output only. The data execution status for data source pivot tables.")
    source: GridRange = Field(..., description="The range the pivot table is reading data from.")
    dataSourceId: str = Field(..., description="The ID of the data source the pivot table is reading data from.")
