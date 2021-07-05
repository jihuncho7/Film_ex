FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3-pip && apt-get clean

WORKDIR /djangoproject

ADD . /djangoproject
RUN pip3 install -r prod.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 80
CMD ["gunicorn", "djangoProject.wsgi:application", "--bind", "0.0.0.0:80" ]
