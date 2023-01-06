FROM tiangolo/uvicorn-gunicorn

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ADD ./stanza_resources /app/stanza_resources

ADD . /app



