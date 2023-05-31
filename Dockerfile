FROM python:3.7-slim

RUN mkdir /app

COPY backend/foodgram/requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir


COPY backend/foodgram/ /app

WORKDIR /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]