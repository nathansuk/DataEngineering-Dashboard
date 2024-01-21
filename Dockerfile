# syntax=docker/dockerfile:1
FROM python:3.7-slim
WORKDIR /code
ENV FLASK_APP=app.py
ENV LISTEN_PORT=5000
EXPOSE 5000
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]