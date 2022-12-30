FROM fedora:36
WORKDIR /root
RUN dnf install --assumeyes git-all
RUN dnf install --assumeyes python3-pip
RUN git clone https://github.com/haymovich/albert.git 
WORKDIR /root/albert
RUN useradd -ms /bin/bash albert