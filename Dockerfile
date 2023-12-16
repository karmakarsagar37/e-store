FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y git && apt-get clean

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]