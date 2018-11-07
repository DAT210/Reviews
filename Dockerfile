FROM python:3.7-alpine

LABEL maintainer="Group-3 - Reviews"

COPY ./ ./app

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV NAME World
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

#CMD [ "python", "reviews/app.py" ]