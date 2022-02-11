FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000", ]
