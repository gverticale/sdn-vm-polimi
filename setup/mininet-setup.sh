# mkdir mininet; curl -sL https://github.com/mininet/mininet/archive/master.tar.gz | tar xz -C mininet --strip=1

# mininet/util/install.sh -n

sudo apt-get install -y mininet
mkdir mininet
mkdir mininet/util
curl -sL https://raw.githubusercontent.com/mininet/mininet/master/util/m > mininet/util/m
chmod u+x mininet/util/m
