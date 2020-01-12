FROM debian:buster
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install Flask

#Prepare project folder
RUN mkdir /opt/cpl-manager/
COPY app/ /opt/cpl-manager/

#Go to app and run
WORKDIR /opt/cpl-manager/
ENV FLASK_RUN_PORT=80
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 80
CMD ["flask", "run"]
