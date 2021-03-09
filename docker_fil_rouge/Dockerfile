FROM python:3.8
MAINTAINER clement.limousin@student-cs.fr 

ADD .aws .aws/
COPY *.py requirements.txt ./

RUN pip3 install -r requirements.txt

ENV AWS_SHARED_CREDENTIALS_FILE=/.aws/credentials
ENV AWS_CONFIG_FILE=/.aws/config
ENV AWS_PROFILE=csloginstudent

CMD ["python3","app.py"]