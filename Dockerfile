FROM python:3

WORKDIR /usr/src/app

COPY ["requirements.txt",  "./"]
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "src.server:app", "-b", "0.0.0.0:8000" ]
