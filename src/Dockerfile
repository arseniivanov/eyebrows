FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get -y install libglib2.0-0
RUN apt-get -y install libgtk2.0-dev
RUN apt-get install -y python3-pip \
    python3-dev \
    build-essential \
    cmake

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd 

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh

EXPOSE 8000 2222

ENTRYPOINT ["init.sh"]
