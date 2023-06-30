from datetime import date, datetime
from json import JSONDecodeError
import logging

from babel.dates import format_date
from httpx import AsyncClient, RequestError
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


class Listing(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, str_strip_whitespace=True)

    description: str
    live: bool
    start_time: datetime
    title: str

    @property
    def details(self) -> str:
        return self.description.removesuffix(" e.").rstrip()

    @property
    def repeat(self) -> bool:
        return self.description.endswith(" e.")

    @property
    def time(self) -> str:
        return self.start_time.strftime("%H:%M")


async def get_listings() -> list[Listing]:
    async with AsyncClient() as client:
        listings = []
        try:
            logging.info("Fetching schedule data")
            response = await client.get("https://apis.is/tv/ruv")
            results = response.json()["results"]
            listings = [Listing.model_validate(listing) for listing in results]
        except (RequestError, JSONDecodeError, LookupError) as error:
            logging.error(error)
        return listings


templates = Jinja2Templates(directory="templates")


def homepage_route(request: Request):
    today = format_date(date.today(), format="full", locale="is")
    context = dict(request=request, today=today)
    return templates.TemplateResponse("index.html", context)


async def listings_route(request: Request):
    listings = await get_listings()
    context = dict(request=request, listings=listings)
    return templates.TemplateResponse("_listings.html", context)


routes = [
    Route("/", homepage_route),
    Route("/_listings", listings_route),
    Mount("/static", StaticFiles(directory="static")),
]


app = Starlette(debug=True, routes=routes)

app.state.AUTHOR = "Paul Burt"
app.state.TITLE = "Dagskrá RÚV"
