FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install pip --upgrade
RUN pip install -r requirements.txt --no-cache-dir
COPY foodgram_back/ .
CMD python manage.py runserver 0:8000