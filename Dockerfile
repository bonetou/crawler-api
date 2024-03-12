FROM python:3.11.7 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.7

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pyppeteer-install
COPY ./app /code/app

RUN pip install "uvicorn[standard]"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
