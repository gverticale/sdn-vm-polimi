sudo apt get gcc install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip
git clone git://github.com/osrg/ryu.git 
pushd ryu
# sudo python ./setup.py install 
pip install .
popd
