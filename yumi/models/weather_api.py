# First create the model for our output parser
from textwrap import dedent
from typing import Literal

from langchain_core.pydantic_v1 import BaseModel, Field


class WeatherLookup(BaseModel):
    """Schema for the weather lookup API structured Output"""

    city: str = Field(
        ...,
        title="City",
        description=dedent(
            """\
        City name, state code (only for the US) and country code divided by comma.
        Please use ISO 3166 country codes when possible.
        """
        ),
    )
    units: Literal["imperial", "metric"] = Field(
        "imperial",
        title="Unit",
        description=dedent(
            """\
        This is the unit you want the temperature to be in (imperial
        for F or metric for C). Default is imperial if not specified.
        """
        ),
    )
