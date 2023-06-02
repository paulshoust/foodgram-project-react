FROM python:3.7-slim


WORKDIR /app

COPY ./foodgram/requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir


COPY . .



CMD ["gunicorn", "app.foodgram.foodgram.wsgi:application", "--bind", "0:8000"]