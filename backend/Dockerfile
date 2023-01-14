FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install pip --upgrade
RUN pip install -r requirements.txt --no-cache-dir
COPY foodgram_back/ .
CMD gunicorn --bind 0.0.0.0:8000 foodgram_back.wsgi
