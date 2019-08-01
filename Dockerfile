FROM python:3

RUN mkdir -p /home/dash_app
WORKDIR /home/dash_app

COPY dash_app /home/dash_app
RUN pip install --no-cache-dir -r docker/requirements.txt

EXPOSE 5006
WORKDIR /home/dash_app

ENV PYTHONPATH /home/
ENV APP_SETTINGS deploy

CMD [ "python3", "-m", "index" ]
