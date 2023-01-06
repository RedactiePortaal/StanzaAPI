FROM tiangolo/uvicorn-gunicorn

ADD . /app

RUN pip install -r requirements.txt

