FROM ubuntu:18.04
MAINTAINER clement.limousin@student-cs.fr 

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

RUN mkdir /app

COPY requirements.txt requirements.txt
COPY Fil_rouge /app/

RUN pip3 install -r requirements.txt
WORKDIR /app/

CMD ["gunicorn3", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]