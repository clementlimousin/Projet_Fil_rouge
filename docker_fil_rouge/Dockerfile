FROM ubuntu:18.04
MAINTAINER clement.limousin@student-cs.fr 

RUN apt-get update -y
RUN apt-get install python3-pip -y

RUN mkdir /app

COPY requirements.txt requirements.txt
COPY Fil_rouge /app/

RUN pip3 install -r requirement.txt
WORKDIR /app/

CMD python app.py