FROM ubuntu:18.04
MAINTAINER clement.limousin@student-cs.fr 

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

COPY Fil_rouge /opt/

RUN pip install -r requirement.txt
WORKDIR /opt/

CMD["gunicorn3", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]