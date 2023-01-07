FROM python:3.10


RUN apt-get --yes update
RUN apt-get --yes install libopenblas-dev libomp-dev build-essential
# RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install "poetry>=1.0"
RUN poetry config virtualenvs.create false
WORKDIR /app

COPY poetry.lock pyproject.toml /app/

COPY . /app

RUN poetry install
# ENV PATH="${HOME}/.local/bin:${PATH}"

CMD ["poetry", "run", "python3", "server.py"]