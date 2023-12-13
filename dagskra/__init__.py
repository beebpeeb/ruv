from pathlib import Path

from starlette.applications import Starlette
from starlette.config import Config

from dagskra.app import routes


config = Config(Path(".env"))

DEBUG = config("DEBUG", cast=bool, default=False)

app = Starlette(debug=DEBUG, routes=routes)

app.state.AUTHOR = "Paul Burt"
app.state.TITLE = "Dagskrá RÚV"
