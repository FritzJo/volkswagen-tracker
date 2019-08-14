FROM python:rc-alpine

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY ./src /app

CMD [ "python", "-u", "./app.py" ]