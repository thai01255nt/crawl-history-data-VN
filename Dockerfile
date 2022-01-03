FROM python:3.8.0-slim as builder
RUN apt-get update && apt-get upgrade -y \
&& apt-get install gcc libgomp1 -y \
&& apt-get clean
COPY requirements.txt /app/requirements.txt
WORKDIR app
RUN pip install --user -r requirements.txt

COPY ./src /app/src
COPY ./app /app/app
COPY ./.env /app
COPY ./server.py /app

CMD [ "python", "server.py" ]
