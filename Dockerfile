# The builder image, used to build the virtual environment
FROM python:3.12-rc-buster AS builder

RUN pip install poetry==2.0.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Only installs the dependencies while avoiding installation of the current project in the virtual environment created.
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR 

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-rc-slim-buster AS runtime


ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

# RUN pip install poetry && poetry install && pip uninstall poetry

ENTRYPOINT [ "fastapi", "run" ]