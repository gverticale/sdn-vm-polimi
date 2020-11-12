apt update && apt upgrade -y
export DEBIAN_FRONTEND=noninteractive
apt-get install -y build-essential git vim emacs
apt-get install -y curl wget iperf arping socat tcpdump hping3 tshark 
apt-get install -y python pyflakes pylint python-dev python-pip
apt-get install -y openvswitch-switch
# apt-get install -y default-jre-headless

# JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
# echo "export JAVA_HOME="$JAVA_HOME > /etc/profile.d/set-java-home.sh
