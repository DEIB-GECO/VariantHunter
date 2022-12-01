FROM python:3.9-slim
ADD . /backend/app
WORKDIR /backend/app
RUN pip install -r requirements.txt