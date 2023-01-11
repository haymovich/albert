FROM jenkins/agent
USER root
RUN apt update 
RUN apt install -y curl sudo pip python3 git
RUN ln -sf python3 /usr/bin/python
RUN git clone https://github.com/haymovich/albert.git
