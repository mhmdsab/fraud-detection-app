FROM python:3.7
COPY ./ /Fraud_APP
WORKDIR /Fraud_APP
RUN apt-get update && apt-get -y upgrade
RUN pip install -r requirments.txt
EXPOSE 22 5000
ENTRYPOINT gunicorn --bind 0.0.0.0:5000 wsgi:app
