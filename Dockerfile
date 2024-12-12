FROM python:3.8.3-slim-buster
WORKDIR /dir
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
COPY . .
CMD ["flask", "run"]