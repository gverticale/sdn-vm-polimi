#!/bin/bash

# Install necessary packages
# sudo apt-get install -y gcc python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip python-networkx
sudo apt-get --no-install-recommends install -y python3-networkx python3-pip

# Use the RYU_VERSION from the environment variable if set, otherwise use the default value
RYU_VERSION=${RYU_VERSION:-d6cda4f427ff8de82b94c58aa826824a106014c2}

mkdir -p ryu
curl -sL "https://github.com/faucetsdn/ryu/archive/${RYU_VERSION}.tar.gz" | tar xz -C ryu --strip=1
cd ryu
pip3 install .
cd ..

# Use the FLOW_MANAGER_VERSION from the environment variable if set, otherwise use the default value
FLOW_MANAGER_VERSION=${FLOW_MANAGER_VERSION:-75cbb146b49b722fabc06e2199c8be18ed5d768a}

mkdir -p flowmanager
curl -sL "https://github.com/martimy/flowmanager/archive/${FLOW_MANAGER_VERSION}.tar.gz" | tar xz -C flowmanager --strip=1
