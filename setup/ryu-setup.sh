# sudo apt-get install -y gcc python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip python-networkx
sudo apt-get --no-install-recommends install -y python-pip python3-networkx

# mkdir ryu; curl -sL https://github.com/osrg/ryu/archive/master.tar.gz | tar xz -C ryu --strip=1
# pip install ./ryu

sudo apt-get install -y ryu-bin
sudo sed -ri 's/(log_config_file.*)/#\1/' /etc/ryu/ryu.conf

mkdir flowmanager; curl -sL https://github.com/martimy/flowmanager/archive/master.tar.gz | tar xz -C flowmanager --strip=1

