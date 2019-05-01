FROM ubuntu:16.04

ENV APACHE_RUN_USER  www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR   /var/log/apache2
ENV APACHE_PID_FILE  /var/run/apache2/apache2.pid
ENV APACHE_RUN_DIR   /var/run/apache2
ENV APACHE_LOCK_DIR  /var/lock/apache2
ENV APACHE_LOG_DIR   /var/log/apache2
RUN mkdir -p $APACHE_RUN_DIR
RUN mkdir -p $APACHE_LOCK_DIR
RUN mkdir -p $APACHE_LOG_DIR

# Install.
#RUN echo "deb http://archive.ubuntu.com/ubuntu bionic main universe" >> /etc/apt/sources.list
#RUN echo "deb http://archive.ubuntu.com/ubuntu bionic-security main universe" >> /etc/apt/sources.list
#RUN echo "deb http://archive.ubuntu.com/ubuntu bionic-updates main universe" >> /etc/apt/sources.list

RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y apache2 && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y nano vim git byobu curl git htop man unzip vim wget fabric python python-yaml libyaml-dev && \
  #apt-get install -y python-dev python-setuptools gcc python-pip  && \
  rm -rf /var/lib/apt/lists/*

# Add files.
ADD ./root/.bashrc /root/.bashrc
ADD ./root/.gitconfig /root/.gitconfig

# Define working directory.
WORKDIR /root
 
EXPOSE 8080

CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]