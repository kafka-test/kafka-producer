FROM registry.access.redhat.com/ubi8/python-38:latest

USER root

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

USER 1001

CMD [ "python", "./app.py" ]