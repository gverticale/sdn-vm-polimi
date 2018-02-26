sudo apt install -y gcc python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip

git clone git://github.com/osrg/ryu.git 
pushd ryu
pip install .
popd
