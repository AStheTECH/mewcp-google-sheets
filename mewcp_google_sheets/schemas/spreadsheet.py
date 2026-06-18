from enum import Enum
from typing import List
from pydantic import BaseModel, Field

from .other import (
    GridRange,
    DataSourceColumn,
    ThemeColorType,
    ColorStyle
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
    hours: int = Field(..., description="Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value '24:00:00' for scenarios like business closing time")
    minutes: int = Field(..., description="Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.")
    seconds: int = Field(..., description="Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.")
    nanos: int = Field(..., description="Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999.")

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

class DataSource(BaseModel):
    dataSourceId: str
    spec: DataSourceSpec
    calculatedColumns: DataSourceColumn
    sheetId: int

class NamedRange(BaseModel):
    namedRangeId: str = Field(..., description="The ID of the named range.")
    name: str = Field(..., description="The name of the named range.")
    range: GridRange = Field(..., description="The range this represents.")

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



class Spreadsheet(BaseModel):
    spreadsheetId: str
    properties: SpreadsheetProperties
    sheets: List[Sheet]
    namedRanges: List[NamedRange]
    spreadsheetUrl: str
    developerMetadata: List[DeveloperMetadata]
    dataSources: List[DataSource]
    dataSourceSchedules: List[DataSourceRefreshSchedule]
