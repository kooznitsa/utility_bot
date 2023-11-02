FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/bot

WORKDIR /home/bot

COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install poetry
RUN poetry install

COPY . ./

CMD ["poetry", "run", "python3", "main.py"]