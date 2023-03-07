# syntax=docker/dockerfile:1
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

USER root
WORKDIR /root

COPY ENTRYPOINT.sh /

# basic-startup.sh
RUN apt update && apt upgrade -y
RUN apt-get -y install sudo
RUN apt-get install -y build-essential screen
RUN apt-get install -y curl wget iperf arping socat tcpdump hping3 tshark
RUN apt-get install -y openvswitch-switch
RUN apt-get install -y iproute2 iputils-ping net-tools openvswitch-testcontroller

# mininet-setup.sh
RUN mkdir mininet; curl -sL https://github.com/mininet/mininet/archive/master.tar.gz | tar xz -C mininet --strip=1
RUN mininet/util/install.sh -nfv

# ryu-setup.sh
RUN sudo apt-get --no-install-recommends install -y python3-networkx
RUN mkdir ryu; curl -sL https://github.com/faucetsdn/ryu/archive/master.tar.gz | tar xz -C ryu --strip=1
RUN cd ryu; pip3 install .
RUN cd ..
RUN mkdir flowmanager; curl -sL https://github.com/martimy/flowmanager/archive/master.tar.gz | tar xz -C flowmanager --strip=1

RUN rm -rf /var/lib/apt/lists/*
RUN chmod +x /ENTRYPOINT.sh 
RUN ln /usr/bin/ovs-testcontroller /usr/bin/controller

# Mininet Fix
EXPOSE 6633 6653 6640

EXPOSE 8181 8080 8008

ENTRYPOINT ["/ENTRYPOINT.sh"]