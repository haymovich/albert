FROM fedora:36
WORKDIR /root
RUN dnf install --assumeyes git-all
RUN dnf install --assumeyes python3-pip
RUN git clone https://github.com/haymovich/albert.git
WORKDIR albert
RUN python3 setup.py
RUN bash
RUN python3 albert.py -pipe -example