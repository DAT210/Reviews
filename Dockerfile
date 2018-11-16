FROM python:3.7-alpine

LABEL maintainer="Group-3 - Reviews"

WORKDIR /home/reviews
COPY requirements.txt ./
COPY reviews reviews
COPY app.py config.py app.py ./

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV FLASK_APP=app.py
ENV FLASK_CONFIG=docker

CMD [ "python", "app.py" ]