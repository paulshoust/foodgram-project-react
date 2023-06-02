FROM python:3.7-slim

COPY ./ /app

WORKDIR /app

COPY ./foodgram/requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

WORKDIR /app/foodgram/foodgram/

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
