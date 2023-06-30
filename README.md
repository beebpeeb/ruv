# Starlette + htmx

A small Python web application which uses [starlette][] and [htmx][]
to demonstrate an approach to [HTML over the Wire][html-over-the-wire].

Data validation is provided by [pydantic][].

HTML templating is provided by [jinja2][].

## Install

Make sure you have Python >= 3.11 and [Poetry] installed, then run the
following:

```sh
poetry install 
```

## Run

To run the app in development mode:

```sh
poetry run uvicorn app:app --reload
```

Open [localhost:8000](http://localhost:8000/) in your web browser to see the running app.

## Test

There are currently no tests.



[html-over-the-wire]: https://dev.to/rajasegar/html-over-the-wire-is-the-future-of-web-development-542c
[htmx]: https://htmx.org/
[jinja2]: https://pypi.org/project/Jinja2/
[poetry]: https://python-poetry.org/
[pydantic]: https://pydantic.dev/
[starlette]: https://pypi.org/project/starlette/
