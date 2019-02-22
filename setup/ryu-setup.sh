sudo apt install -y gcc python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip python-networkx

mkdir ryu; curl -sL https://github.com/osrg/ryu/archive/master.tar.gz | tar xz -C ryu --strip=1
pip install ./ryu

mkdir flowmanager; curl -sL https://github.com/martimy/flowmanager/archive/master.tar.gz | tar xz -C flowmanager --strip=1

