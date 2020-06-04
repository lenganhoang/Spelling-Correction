FROM python:3.6-slim-buster

COPY . /app
ADD . .

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/main.py"]