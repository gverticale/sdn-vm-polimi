# sudo apt-get install -y gcc python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip python-networkx
sudo apt-get --no-install-recommends install -y python3-networkx

mkdir ryu; curl -sL https://github.com/faucetsdn/ryu/archive/master.tar.gz | tar xz -C ryu --strip=1
cd ryu; pip3 install .
cd ..

mkdir flowmanager; curl -sL https://github.com/martimy/flowmanager/archive/master.tar.gz | tar xz -C flowmanager --strip=1

