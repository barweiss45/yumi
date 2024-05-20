from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate

from util import get_current_time

get_weather_api_template = dedent(
    """\
        You are a very friendly and helpful Assistant. Please help the user with their
        weather related queries. Please do you best to determine what city and country,
        and state if in the US, the user is asking about. If you are unsure then chose
        the most likely city and country.

        User: {query}"""
)

get_weather_generative_template = dedent(
    """\
        This is the response from api.openweather.com about the current weather
        conditions. Based on this response, can you please create a friendly weather
        report and include relevant emojis that are fun and personalized to me?

        {weather_api_response}
    """
    + f"""\
    \n
    Also, please provide the current date and time, which is {get_current_time()}
    US Eastern Time."""
)

GET_WEATHER_API_PROMPT = ChatPromptTemplate.from_template(
    template=get_weather_api_template
)

GET_WEATHER_GENERATIVE_PROMPT = ChatPromptTemplate.from_template(
    template=get_weather_generative_template
)
