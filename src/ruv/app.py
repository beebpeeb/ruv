import json
import logging
from pathlib import Path

import httpx
from babel.dates import format_date
from pydantic import BaseModel, ConfigDict, NaiveDatetime
from pydantic.alias_generators import to_camel
from starlette.applications import Starlette
from starlette.config import Config
from starlette.requests import Request
from starlette.routing import Route
from starlette.templating import Jinja2Templates


class Listing(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, str_strip_whitespace=True)

    description: str
    live: bool
    start_time: NaiveDatetime
    title: str

    @property
    def details(self) -> str:
        return self.description.removesuffix(" e.").rstrip()

    @property
    def human_readable_date(self) -> str:
        return format_date(self.start_time.date(), locale="is", format="full")

    @property
    def repeat(self) -> bool:
        return self.description.endswith(" e.")

    @property
    def time(self) -> str:
        return f"{self.start_time:%H:%M}"


http = httpx.AsyncClient()


async def get_listings() -> list[Listing]:
    listings: list[Listing] = []
    try:
        response = await http.get("https://apis.is/tv/ruv")
        results = response.json()["results"]
        listings = [Listing.model_validate(listing) for listing in results]
    except (httpx.RequestError, json.JSONDecodeError, LookupError) as error:
        logging.error(error)
    return listings


templates = Jinja2Templates(Path("templates"))


def index_route(request: Request):
    context = dict(request=request)
    return templates.TemplateResponse("index.html", context)


async def listings_route(request: Request, today: str | None = None):
    listings = await get_listings()
    if listings:
        today = listings[0].human_readable_date
    context = dict(request=request, listings=listings, today=today)
    return templates.TemplateResponse("_listings.html", context)


routes = (
    Route("/", index_route),
    Route("/_listings", listings_route),
)

config = Config(Path(".env"))

DEBUG = config("DEBUG", cast=bool, default=False)

app = Starlette(debug=DEBUG, routes=routes)

app.state.AUTHOR = "Paul Burt"
app.state.TITLE = "Dagskrá RÚV"
