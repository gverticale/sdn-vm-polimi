sudo apt install -y openvswitch-switch

git clone git://github.com/mininet/mininet
pushd mininet
git checkout
popd
mininet/util/install.sh -n
# mininet/util/install.sh -nfv
