#!/bin/bash

# Use the MININET_VERSION from the environment variable if set, otherwise use the default value
MININET_VERSION=${MININET_VERSION:-6eb8973c0bfd13c25c244a3871130c5e36b5fbd7}

mkdir -p mininet
curl -sL "https://github.com/mininet/mininet/archive/${MININET_VERSION}.tar.gz" | tar xz -C mininet --strip=1

mininet/util/install.sh -nfv
