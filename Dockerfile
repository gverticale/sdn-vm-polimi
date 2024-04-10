# syntax=docker/dockerfile:1
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG MININET_VERSION=6eb8973c0bfd13c25c244a3871130c5e36b5fbd7
ARG RYU_VERSION=d6cda4f427ff8de82b94c58aa826824a106014c2
ARG FLOW_MANAGER_VERSION=75cbb146b49b722fabc06e2199c8be18ed5d768a

ENV MININET_VERSION=$MININET_VERSION
ENV RYU_VERSION=$RYU_VERSION
ENV FLOW_MANAGER_VERSION=$FLOW_MANAGER_VERSION

USER root
WORKDIR /root

COPY .Xresources /root/

RUN apt update && apt upgrade -y
RUN apt-get -y install sudo vim x11-xserver-utils xterm wireshark-qt wget
RUN apt-get update && apt-get install -y --no-install-recommends python-tk

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
RUN apt-get update && apt-get install -y --no-install-recommends git netcat

# basic-startup.sh
COPY setup/basic-setup.sh basic-setup.sh
RUN chmod +x ./basic-setup.sh
RUN ./basic-setup.sh
RUN rm basic-setup.sh

RUN apt-get install -y iproute2 iputils-ping net-tools openvswitch-testcontroller
RUN ln /usr/bin/ovs-testcontroller /usr/bin/controller

# mininet-setup.sh
COPY setup/mininet-setup.sh mininet-setup.sh
RUN chmod +x ./mininet-setup.sh
RUN ./mininet-setup.sh
RUN rm mininet-setup.sh

# ryu-setup.sh
COPY setup/ryu-setup.sh ryu-setup.sh
RUN chmod +x ./ryu-setup.sh
RUN ./ryu-setup.sh
RUN rm ryu-setup.sh

WORKDIR /root

# Mininet Fix
EXPOSE 6633 6653 6640

EXPOSE 8181 8080 8008

COPY docker-sdn/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD [ "/bin/bash" ]
