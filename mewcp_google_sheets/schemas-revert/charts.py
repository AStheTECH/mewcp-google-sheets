from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from .other import (
    TextFormat,
    ColorStyle,
    FilterSpec,
    SortSpec,
    EmbeddedObjectPosition,
    HorizontalAlign,
    DataExecutionStatus,
    GridRange,
    DataSourceColumnReference
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


class ChartAggregateType(Enum):
    CHART_AGGREGATE_TYPE_UNSPECIFIED = "CHART_AGGREGATE_TYPE_UNSPECIFIED"
    AVERAGE = "AVERAGE"
    COUNT = "COUNT"
    MAX = "MAX"
    MEDIAN = "MEDIAN"
    MIN = "MIN"
    SUM = "SUM"


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


class BasicChartStackedType(Enum):
    BASIC_CHART_STACKED_TYPE_UNSPECIFIED = "BASIC_CHART_STACKED_TYPE_UNSPECIFIED"
    NOT_STACKED = "NOT_STACKED"
    STACKED = "STACKED"
    PERCENT_STACKED = "PERCENT_STACKED"


class BasicChartCompareMode(Enum):
    BASIC_CHART_COMPARE_MODE_UNSPECIFIED = "BASIC_CHART_COMPARE_MODE_UNSPECIFIED"
    DATUM = "DATUM"
    CATEGORY = "CATEGORY"


class PieChartLegendPosition(Enum):
    PIE_CHART_LEGEND_POSITION_UNSPECIFIED = "PIE_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    LABELED_LEGEND = "LABELED_LEGEND"


class BubbleChartLegendPosition(Enum):
    BUBBLE_CHART_LEGEND_POSITION_UNSPECIFIED = "BUBBLE_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    INSIDE_LEGEND = "INSIDE_LEGEND"


class WaterfallChartStackedType(Enum):
    WATERFALL_STACKED_TYPE_UNSPECIFIED = "WATERFALL_STACKED_TYPE_UNSPECIFIED"
    STACKED = "STACKED"
    SEQUENTIAL = "SEQUENTIAL"

class TextPosition(BaseModel):
    horizontalAlignment: HorizontalAlign = Field(..., description="Horizontal alignment setting for the piece of text.")

class ChartAxisViewWindowOptions(BaseModel):
    viewWindowMin: int = Field(..., description="The minimum numeric value to be shown in this view window. If unset, will automatically determine a minimum value that looks good for the data.")
    viewWindowMax: int = Field(..., description="The maximum numeric value to be shown in this view window. If unset, will automatically determine a maximum value that looks good for the data.")
    viewWindowMode: ViewWindowMode = Field(..., description="The view window's mode.")

class BasicChartAxis(BaseModel):
    position: BasicChartAxisPosition = Field(..., description="The position of this axis.")
    title: str = Field(..., description="The title of this axis. If set, this overrides any title inferred from headers of the data.")
    format: TextFormat = Field(..., description="The format of the title. Only valid if the axis is not associated with the domain. The link field is not supported.")
    titleTextPosition: TextPosition = Field(..., description="The axis title text position.")
    viewWindowOptions: ChartAxisViewWindowOptions = Field(..., description="The view window options for this axis.")

class ChartSourceRange(BaseModel):
    sources: List[GridRange] = Field(..., description="The ranges of data for a series or domain. Exactly one dimension must have a length of 1, and all sources in the list must have the same dimension with length 1. The domain (if it exists) & all series must have the same number of source ranges. If using more than one source range, then the source range at a given offset must be in order and contiguous across the domain and series.")

class ChartDateTimeRule(BaseModel):
    type: ChartDateTimeRuleType = Field(..., description="The type of date-time grouping to apply.")


class ChartHistogramRule(BaseModel):
    minValue: int = Field(..., description="The minimum value at which items are placed into buckets. Values that are less than the minimum are grouped into a single bucket. If omitted, it is determined by the minimum item value.")
    maxValue: int = Field(..., description="The maximum value at which items are placed into buckets. Values greater than the maximum are grouped into a single bucket. If omitted, it is determined by the maximum item value.")
    intervalSize: int = Field(..., description="The size of the buckets that are created. Must be positive.")


class ChartGroupRule(BaseModel):
    dateTimeRule: ChartDateTimeRule = Field(..., description="A ChartDateTimeRule.")
    histogramRule: ChartHistogramRule = Field(..., description="A ChartHistogramRule")

class ChartData(BaseModel):
    groupRule: ChartGroupRule = Field(..., description="The rule to group the data by if the ChartData backs the domain of a data source chart. Only supported for data source charts.")
    aggregateType: ChartAggregateType = Field(..., description="The aggregation type for the series of a data source chart. Only supported for data source charts.")
    sourceRange: ChartSourceRange = Field(..., description="The source ranges of the data.")
    columnReference: DataSourceColumnReference = Field(..., description="The reference to the data source column that the data reads from.")

class BasicChartDomain(BaseModel):
    domain: ChartData = Field(..., description="The data of the domain. For example, if charting stock prices over time, this is the data representing the dates.")
    reversed: bool = Field(..., description="True to reverse the order of the domain values (horizontal axis).")


class LineStyle(BaseModel):
    width: int = Field(..., description="The thickness of the line, in px.")
    type: LineDashType = Field(..., description="The dash type of the line.")


class DataLabel(BaseModel):
    type: DataLabelType = Field(..., description="The type of the data label.")
    textFormat: TextFormat = Field(..., description="The text format used for the data label. The link field is not supported.")
    placement: DataLabelPlacement = Field(..., description="The placement of the data label relative to the labeled data.")
    customLabelData: ChartData = Field(..., description="Data to use for custom labels. Only used if type is set to CUSTOM. This data must be the same length as the series or other element this data label is applied to. In addition, if the series is split into multiple source ranges, this source data must come from the next column in the source data.")


class PointStyle(BaseModel):
    size: int = Field(..., description="The point size. If empty, a default size is used.")
    shape: PointShape = Field(..., description="The point shape. If empty or unspecified, a default shape is used.")


class BasicSeriesDataPointStyleOverride(BaseModel):
    index: int = Field(..., description="The zero-based index of the series data point.")
    colorStyle: ColorStyle = Field(..., description="Color of the series data point. If empty, the series default is used. If color is also set, this field takes precedence.")
    pointStyle: PointStyle = Field(..., description="Point style of the series data point. Valid only if the chartType is AREA, LINE, or SCATTER. COMBO charts are also supported if the series chart type is AREA, LINE, or SCATTER. If empty, the series default is used.")


class BasicChartSeries(BaseModel):
    series: ChartData = Field(..., description="The data being visualized in this chart series.")
    targetAxis: BasicChartAxisPosition = Field(..., description="The minor axis that will specify the range of values for this series. For example, if charting stocks over time, the 'Volume' series may want to be pinned to the right with the prices pinned to the left, because the scale of trading volume is different than the scale of prices. It is an error to specify an axis that isn't a valid minor axis for the chart's type.")
    type: BasicChartType = Field(..., description="The type of this series. Valid only if the chartType is COMBO. Different types will change the way the series is visualized. Only LINE, AREA, and COLUMN are supported.")
    lineStyle: LineStyle = Field(..., description="The line style of this series. Valid only if the chartType is AREA, LINE, or SCATTER. COMBO charts are also supported if the series chart type is AREA or LINE.")
    dataLabel: DataLabel = Field(..., description="Information about the data labels for this series.")
    colorStyle: ColorStyle = Field(..., description="The color for elements (such as bars, lines, and points) associated with this series. If empty, a default color is used. If color is also set, this field takes precedence.")
    pointStyle: PointStyle = Field(..., description="The style for points associated with this series. Valid only if the chartType is AREA, LINE, or SCATTER. COMBO charts are also supported if the series chart type is AREA, LINE, or SCATTER. If empty, a default point style is used.")
    styleOverrides: List[BasicSeriesDataPointStyleOverride] = Field(..., description="Style override settings for series data points.")


class BasicChartSpec(BaseModel):
    chartType: BasicChartType = Field(..., description="The type of the chart.")
    legendPosition: BasicChartLegendPosition = Field(..., description="The position of the chart legend.")
    axis: List[BasicChartAxis] = Field(..., description="The axis on the chart.")
    domains: List[BasicChartDomain] = Field(..., description="The domain of data this is charting. Only a single domain is supported.")
    series: List[BasicChartSeries] = Field(..., description="The data this chart is visualizing.")
    headerCount: int = Field(..., description="The number of rows or columns in the data that are 'headers'. If not set, Google Sheets will guess how many rows are headers based on the data. (Note that BasicChartAxis.title may override the axis title inferred from the header values.)")
    threeDimensional: bool = Field(..., description="True to make the chart 3D. Applies to Bar and Column charts.")
    interpolateNulls: bool = Field(..., description="If some values in a series are missing, gaps may appear in the chart (e.g, segments of lines in a line chart will be missing). To eliminate these gaps set this to true. Applies to Line, Area, and Combo charts.")
    stackedType: BasicChartStackedType = Field(..., description="The stacked type for charts that support vertical stacking. Applies to Area, Bar, Column, Combo, and Stepped Area charts.")
    lineSmoothing: bool = Field(..., description="Gets whether all lines should be rendered smooth or straight by default. Applies to Line charts.")
    compareMode: BasicChartCompareMode = Field(..., description="The behavior of tooltips and data highlighting when hovering on data and chart area.")
    totalDataLabel: DataLabel = Field(..., description="Controls whether to display additional data labels on stacked charts which sum the total value of all stacked values at each value along the domain axis.")


class DataSourceChartProperties(BaseModel):
    dataSourceId: str = Field(..., description="ID of the data source that the chart is associated with.")
    dataExecutionStatus: DataExecutionStatus = Field(..., description="Output only. The data execution status.")

class PieChartSpec(BaseModel):
    legendPosition: PieChartLegendPosition = Field(..., description="Where the legend of the pie chart should be drawn.")
    domain: ChartData = Field(..., description="The data that covers the domain of the pie chart.")
    series: ChartData = Field(..., description="The data that covers the one and only series of the pie chart.")
    threeDimensional: bool = Field(..., description="True if the pie is three dimensional.")
    pieHole: int = Field(..., description="The size of the hole in the pie chart.")

class BubbleChartSpec(BaseModel):
    legendPosition: BubbleChartLegendPosition = Field(..., description="Where the legend of the chart should be drawn.")
    bubbleLabels: ChartData = Field(..., description="The data containing the bubble labels. These do not need to be unique.")
    domain: ChartData = Field(..., description="The data containing the bubble x-values. These values locate the bubbles in the chart horizontally.")
    series: ChartData = Field(..., description="The data containing the bubble y-values. These values locate the bubbles in the chart vertically.")
    groupIds: ChartData = Field(..., description="The data containing the bubble group IDs. All bubbles with the same group ID are drawn in the same color. If bubbleSizes is specified then this field must also be specified but may contain blank values. This field is optional.")
    bubbleSizes: ChartData = Field(..., description="The data containing the bubble sizes. Bubble sizes are used to draw the bubbles at different sizes relative to each other. If specified, groupIds must also be specified. This field is optional.")
    bubbleOpacity: int = Field(..., description="The opacity of the bubbles between 0 and 1.0. 0 is fully transparent and 1 is fully opaque.")
    bubbleBorderColorStyle: ColorStyle = Field(..., description="The bubble border color. If bubbleBorderColor is also set, this field takes precedence.")
    bubbleMaxRadiusSize: int = Field(..., description="The max radius size of the bubbles, in pixels. If specified, the field must be a positive value.")
    bubbleMinRadiusSize: int = Field(..., description="The minimum radius size of the bubbles, in pixels. If specific, the field must be a positive value.")
    bubbleTextStyle: TextFormat = Field(..., description="The format of the text inside the bubbles. Strikethrough, underline, and link are not supported.")


class CandlestickDomain(BaseModel):
    data: ChartData = Field(..., description="The data of the CandlestickDomain.")
    reversed: bool = Field(..., description="True to reverse the order of the domain values (horizontal axis).")

class CandlestickSeries:
    data: ChartData = Field(..., description="The data of the CandlestickSeries.")

class CandlestickData(BaseModel):
    lowSeries: CandlestickSeries = Field(..., description="The range data (vertical axis) for the low/minimum value for each candle. This is the bottom of the candle's center line.")
    openSeries: CandlestickSeries = Field(..., description="The range data (vertical axis) for the open/initial value for each candle. This is the bottom of the candle body. If less than the close value the candle will be filled. Otherwise the candle will be hollow.")
    closeSeries: CandlestickSeries = Field(..., description="The range data (vertical axis) for the close/final value for each candle. This is the top of the candle body. If greater than the open value the candle will be filled. Otherwise the candle will be hollow.")
    highSeries: CandlestickSeries = Field(..., description="The range data (vertical axis) for the high/maximum value for each candle. This is the top of the candle's center line.")


class CandlestickChartSpec(BaseModel):
    domain: CandlestickDomain = Field(..., description="The domain data (horizontal axis) for the candlestick chart. String data will be treated as discrete labels, other data will be treated as continuous values.")
    data: CandlestickData = Field(..., description="The Candlestick chart data. Only one CandlestickData is supported.")


class OrgChartNodeSize(Enum):
    ORG_CHART_LABEL_SIZE_UNSPECIFIED = "ORG_CHART_LABEL_SIZE_UNSPECIFIED"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class HistogramChartLegendPosition(Enum):
    HISTOGRAM_CHART_LEGEND_POSITION_UNSPECIFIED = "HISTOGRAM_CHART_LEGEND_POSITION_UNSPECIFIED"
    BOTTOM_LEGEND = "BOTTOM_LEGEND"
    LEFT_LEGEND = "LEFT_LEGEND"
    RIGHT_LEGEND = "RIGHT_LEGEND"
    TOP_LEGEND = "TOP_LEGEND"
    NO_LEGEND = "NO_LEGEND"
    INSIDE_LEGEND = "INSIDE_LEGEND"

class HistogramSeries(BaseModel):
    barColorStyle: ColorStyle = Field(..., description="The color of the column representing this series in each bucket. This field is optional. If barColor is also set, this field takes precedence.")
    data: ChartData = Field(..., description="The data for this histogram series.")

class HistogramChartSpec(BaseModel):
    series: List[HistogramSeries] = Field(..., description="The series for a histogram may be either a single series of values to be bucketed or multiple series, each of the same length, containing the name of the series followed by the values to be bucketed for that series.")
    legendPosition: HistogramChartLegendPosition = Field(..., description="The position of the chart legend.")
    showItemDividers: bool = Field(..., description="Whether horizontal divider lines should be displayed between items in each column.")
    bucketSize: int = Field(..., description="By default the bucket size (the range of values stacked in a single column) is chosen automatically, but it may be overridden here.")
    outlierPercentile: int = Field(..., description="The outlier percentile is used to ensure that outliers do not adversely affect the calculation of bucket sizes. For example, setting an outlier percentile of 0.05 indicates that the top and bottom 5% of values when calculating buckets. The values are still included in the chart, they will be added to the first or last buckets instead of their own buckets. Must be between 0.0 and 0.5.")

class OrgChartSpec(BaseModel):
    nodeSize: OrgChartNodeSize = Field(..., description="The size of the org chart nodes.")
    nodeColorStyle: ColorStyle = Field(..., description="The color of the org chart nodes. If nodeColor is also set, this field takes precedence.")
    selectedNodeColorStyle: ColorStyle = Field(..., description="The color of the selected org chart nodes. If selectedNodeColor is also set, this field takes precedence.")
    labels: ChartData = Field(..., description="The data containing the labels for all the nodes in the chart. Labels must be unique.")
    parentLabels: Optional[ChartData] = Field(..., description="The data containing the label of the parent for the corresponding node. A blank value indicates that the node has no parent and is a top-level node. This field is optional.")
    tooltips: Optional[ChartData] = Field(..., description="The data containing the tooltip for the corresponding node. A blank value results in no tooltip being displayed for the node. This field is optional.")


class WaterfallChartDomain(BaseModel):
    data: ChartData = Field(..., description="The data of the WaterfallChartDomain.")
    reversed: bool = Field(..., description="True to reverse the order of the domain values (horizontal axis).")


class WaterfallChartColumnStyle(BaseModel):
    label: str = Field(..., description="The label of the column's legend.")
    colorStyle: ColorStyle = Field(..., description="The color of the column. If color is also set, this field takes precedence.")


class WaterfallChartCustomSubtotal(BaseModel):
    subtotalIndex: int = Field(..., description="The zero-based index of a data point within the series. If dataIsSubtotal is true, the data point at this index is the subtotal. Otherwise, the subtotal appears after the data point with this index. A series can have multiple subtotals at arbitrary indices, but subtotals do not affect the indices of the data points.")
    label: str = Field(..., description="A label for the subtotal column.")
    dataIsSubtotal: bool = Field(..., description="True if the data point at subtotalIndex is the subtotal. If false, the subtotal will be computed and appear after the data point.")


class WaterfallChartSeries(BaseModel):
    data: ChartData = Field(..., description="The data being visualized in this series.")
    positiveColumnsStyle: WaterfallChartColumnStyle = Field(..., description="Styles for all columns in this series with positive values.")
    negativeColumnsStyle: WaterfallChartColumnStyle = Field(..., description="Styles for all columns in this series with negative values.")
    subtotalColumnsStyle: WaterfallChartColumnStyle = Field(..., description="Styles for all subtotal columns in this series.")
    hideTrailingSubtotal: bool = Field(..., description="True to hide the subtotal column from the end of the series. By default, a subtotal column will appear at the end of each series. Setting this field to true will hide that subtotal column for this series.")
    customSubtotals: List[WaterfallChartCustomSubtotal] = Field(..., description="Custom subtotal columns appearing in this series. The order in which subtotals are defined is not significant. Only one subtotal may be defined for each data point.")
    dataLabel: DataLabel = Field(..., description="Information about the data labels for this series.")

class WaterfallChartSpec(BaseModel):
    domain: WaterfallChartDomain = Field(..., description="The domain data (horizontal axis) for the waterfall chart.")
    series: WaterfallChartSeries = Field(..., description="The data this waterfall chart is visualizing.")
    stackedType: WaterfallChartStackedType = Field(..., description="The stacked type.")
    firstValueIsTotal: bool = Field(..., description="True to interpret the first value as a total.")
    hideConnectorLines: bool = Field(..., description="True to hide connector lines between columns.")
    connectorLineStyle: LineStyle = Field(..., description="The line style for the connector lines.")
    totalDataLabel: DataLabel = Field(..., description="Controls whether to display additional data labels on stacked charts which sum the total value of all stacked values at each value along the domain axis. stackedType must be STACKED and neither CUSTOM nor placement can be set on the totalDataLabel.")


class TreemapChartColorScale(BaseModel):
    minValueColorStyle: ColorStyle = Field(..., description="The background color for cells with a color value less than or equal to minValue. Defaults to #dc3912 if not specified. If minValueColor is also set, this field takes precedence.")
    midValueColorStyle: ColorStyle = Field(..., description="The background color for cells with a color value at the midpoint between minValue and maxValue. Defaults to #efe6dc if not specified. If midValueColor is also set, this field takes precedence.")
    maxValueColorStyle: ColorStyle = Field(..., description="The background color for cells with a color value greater than or equal to maxValue. Defaults to #109618 if not specified. If maxValueColor is also set, this field takes precedence.")
    noDataColorStyle: ColorStyle = Field(..., description="The background color for cells that have no color data associated with them. Defaults to #000000 if not specified. If noDataColor is also set, this field takes precedence.")

class TreemapChartSpec(BaseModel):
    labels: ChartData = Field(..., description="The data that contains the treemap cell labels.")
    parentLabels: ChartData = Field(..., description="The data the contains the treemap cells' parent labels.")
    sizeData: ChartData = Field(..., description="The data that determines the size of each treemap data cell. This data is expected to be numeric. The cells corresponding to non-numeric or missing data will not be rendered. If colorData is not specified, this data is used to determine data cell background colors as well.")
    colorData: ChartData = Field(..., description="The data that determines the background color of each treemap data cell. This field is optional. If not specified, sizeData is used to determine background colors. If specified, the data is expected to be numeric. colorScale will determine how the values in this data map to data cell background colors.")
    textFormat: TextFormat = Field(..., description="The text format for all labels on the chart. The link field is not supported.")
    levels: int = Field(..., description="The number of data levels to show on the treemap chart. These levels are interactive and are shown with their labels. Defaults to 2 if not specified.")
    hintedLevels: int = Field(..., description="The number of additional data levels beyond the labeled levels to be shown on the treemap chart. These levels are not interactive and are shown without their labels. Defaults to 0 if not specified.")
    minValue: int = Field(..., description="The minimum possible data value. Cells with values less than this will have the same color as cells with this value. If not specified, defaults to the actual minimum value from colorData, or the minimum value from sizeData if colorData is not specified.")
    maxValue: int = Field(..., description="The maximum possible data value. Cells with values greater than this will have the same color as cells with this value. If not specified, defaults to the actual maximum value from colorData, or the maximum value from sizeData if colorData is not specified.")
    headerColorStyle: ColorStyle = Field(..., description="The background color for header cells. If headerColor is also set, this field takes precedence.")
    colorScale: TreemapChartColorScale = Field(..., description="The color scale for data cells in the treemap chart. Data cells are assigned colors based on their color values. These color values come from colorData, or from sizeData if colorData is not specified. Cells with color values less than or equal to minValue will have minValueColor as their background color. Cells with color values greater than or equal to maxValue will have maxValueColor as their background color. Cells with color values between minValue and maxValue will have background colors on a gradient between minValueColor and maxValueColor, the midpoint of the gradient being midValueColor. Cells with missing or non-numeric color values will have noDataColor as their background color.")
    hideToolTips: bool = Field(..., description="True to hide tooltips.")


class KeyValueFormat(BaseModel):
    textFormat: TextFormat = Field(..., description="Text formatting options for key value. The link field is not supported.")
    position: TextPosition = Field(..., description="Specifies the horizontal text positioning of key value. This field is optional. If not specified, default positioning is used.")


class ComparisonType(Enum):
    COMPARISON_TYPE_UNDEFINED = "COMPARISON_TYPE_UNDEFINED"
    ABSOLUTE_DIFFERENCE = "ABSOLUTE_DIFFERENCE"
    PERCENTAGE_DIFFERENCE = "PERCENTAGE_DIFFERENCE"

class BaselineValueFormat(BaseModel):
    comparisonType: ComparisonType = Field(..., description="The comparison type of key value with baseline value.")
    textFormat: TextFormat = Field(..., description="Text formatting options for baseline value. The link field is not supported.")
    position: TextPosition = Field(..., description="Specifies the horizontal text positioning of baseline value. This field is optional. If not specified, default positioning is used.")
    description: Optional[str] = Field(..., description="Description which is appended after the baseline value. This field is optional.")
    positiveColorStyle: ColorStyle = Field(..., description="Color to be used, in case baseline value represents a positive change for key value. This field is optional. If positiveColor is also set, this field takes precedence.")
    negativeColorStyle: ColorStyle = Field(..., description="Color to be used, in case baseline value represents a negative change for key value. This field is optional. If negativeColor is also set, this field takes precedence.")


class ChartNumberFormatSource(Enum):
    CHART_NUMBER_FORMAT_SOURCE_UNDEFINED = "CHART_NUMBER_FORMAT_SOURCE_UNDEFINED"
    FROM_DATA = "FROM_DATA"
    CUSTOM = "CUSTOM"


class ChartCustomNumberFormatOptions(BaseModel):
    prefix: Optional[str] = Field(..., description="Custom prefix to be prepended to the chart attribute. This field is optional.")
    suffix: Optional[str] = Field(..., description="Custom suffix to be appended to the chart attribute. This field is optional.")


class ChartHiddenDimensionStrategy(Enum):
    CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED = "CHART_HIDDEN_DIMENSION_STRATEGY_UNSPECIFIED"
    SKIP_HIDDEN_ROWS_AND_COLUMNS = "SKIP_HIDDEN_ROWS_AND_COLUMNS"
    SKIP_HIDDEN_ROWS = "SKIP_HIDDEN_ROWS"
    SKIP_HIDDEN_COLUMNS = "SKIP_HIDDEN_COLUMNS"
    SHOW_ALL = "SHOW_ALL"

class ScorecardChartSpec(BaseModel):
    keyValueData: ChartData = Field(..., description="The data for scorecard key value.")
    baselineValueData: Optional[ChartData] = Field(..., description="The data for scorecard baseline value. This field is optional.")
    aggregateType: Optional[ChartAggregateType] = Field(..., description="The aggregation type for key and baseline chart data in scorecard chart. This field is not supported for data source charts. Use the ChartData.aggregateType field of the keyValueData or baselineValueData instead for data source charts. This field is optional.")
    keyValueFormat: KeyValueFormat = Field(..., description="Formatting options for key value.")
    baselineValueFormat: BaselineValueFormat = Field(..., description="Formatting options for baseline value. This field is needed only if baselineValueData is specified.")
    scaleFactor: Optional[int] = Field(..., description="Value to scale scorecard key and baseline value. For example, a factor of 10 can be used to divide all values in the chart by 10. This field is optional.")
    numberFormatSource: Optional[ChartNumberFormatSource] = Field(..., description="The number format source used in the scorecard chart. This field is optional.")
    customFormatOptions: Optional[ChartCustomNumberFormatOptions] = Field(..., description="Custom formatting options for numeric key/baseline values in scorecard chart. This field is used only when numberFormatSource is set to CUSTOM. This field is optional.")

class ChartSpec(BaseModel):
    title: str = Field(..., description="The title of the chart.")
    altText: str = Field(..., description="The alternative text that describes the chart. This is often used for accessibility.")
    titleTextFormat: TextFormat = Field(..., description="The title text format. Strikethrough, underline, and link are not supported.")
    titleTextPosition: TextPosition = Field(..., description="The title text position. This field is optional.")
    subtitle: str = Field(..., description="The subtitle of the chart.")
    subtitleTextFormat: TextFormat = Field(..., description="The subtitle text format. Strikethrough, underline, and link are not supported.")
    subtitleTextPosition: TextPosition = Field(..., description="The subtitle text position. This field is optional.")
    fontName: str = Field(..., description="The name of the font to use by default for all chart text (e.g. title, axis labels, legend). If a font is specified for a specific part of the chart it will override this font name.")
    maximized: bool = Field(..., description="True to make a chart fill the entire space in which it's rendered with minimum padding. False to use the default padding. (Not applicable to Geo and Org charts.)")
    backgroundColorStyle: ColorStyle = Field(..., description="The background color of the entire chart. Not applicable to Org charts.")
    dataSourceChartProperties: DataSourceChartProperties = Field(..., description="If present, the field contains data source chart specific properties.")
    filterSpecs: List[FilterSpec] = Field(..., description="The filters applied to the source data of the chart. Only supported for data source charts.")
    sortSpecs: List[SortSpec] = Field(..., description="The order to sort the chart data by. Only a single sort spec is supported. Only supported for data source charts.")
    hiddenDimensionStrategy: ChartHiddenDimensionStrategy = Field(..., description="Determines how the charts will use hidden rows or columns.")
    basicChart: BasicChartSpec = Field(..., description="A basic chart specification, can be one of many kinds of charts. See BasicChartType for the list of all charts this supports.")
    pieChart: PieChartSpec = Field(..., description="A pie chart specification.")
    bubbleChart: BubbleChartSpec = Field(..., description="A bubble chart specification.")
    candlestickChart: CandlestickChartSpec = Field(..., description="A candlestick chart specification.")
    orgChart: OrgChartSpec = Field(..., description="An org chart specification.")
    histogramChart: HistogramChartSpec = Field(..., description="A histogram chart specification.")
    waterfallChart: WaterfallChartSpec = Field(..., description="A waterfall chart specification.")
    treemapChart: TreemapChartSpec = Field(..., description="A treemap chart specification.")
    scorecardChart: ScorecardChartSpec = Field(..., description="A scorecard chart specification.")

class EmbeddedObjectBorder(BaseModel):
    colorStyle: ColorStyle = Field(..., description="The color of the border. If color is also set, this field takes precedence.")

class EmbeddedChart(BaseModel):
    chartId: int = Field(..., description="The ID of the chart.")
    spec: ChartSpec = Field(..., description="The specification of the chart.")
    position: EmbeddedObjectPosition = Field(..., description="The position of the chart.")
    border: EmbeddedObjectBorder = Field(..., description="The border of the chart.")


