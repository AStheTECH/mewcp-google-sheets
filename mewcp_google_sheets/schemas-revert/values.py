from typing import List

from .api_types import Dimension
from pydantic import BaseModel, Field


class ValueRange(BaseModel):
    range: str = Field(..., description="The range the values cover, in A1 notation. For output, this range indicates the entire requested range, even though the values will exclude trailing rows and columns. When appending values, this field represents the range to search for a table, after which values will be appended.")
    majorDimension: Dimension = Field(..., description="The major dimension of the values.")
    values: List = Field(..., description="The data that was read or to be written. This is an array of arrays, the outer array representing all the data and each inner array representing a major dimension. Each item in the inner array corresponds with one cell. For output, empty trailing rows and columns will not be included.For input, supported value types are: bool, string, and double. Null values will be skipped. To set a cell to an empty value, set the string value to an empty string.")
