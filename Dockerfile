FROM python:3.8-alpine

RUN mkdir /code
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python", "server.py" ]