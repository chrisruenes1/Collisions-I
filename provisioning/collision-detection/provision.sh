if [[ -z $1 ]]; then
    echo 'must specify target ip address';
    exit 1;
fi
PI_IP=$1

# install circuit python
ssh $PI_IP 'sudo apt-get update &&\
    sudo apt-get upgrade &&\
    sudo apt-get install python3-pip &&\
    sudo pip3 install --upgrade setuptools &&\
    cd ~ && sudo pip3 install --upgrade adafruit-python-shell &&\
    wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py &&\
    sudo python3 raspi-blinka.py &&\
    sudo pip3 install adafruit-circuitpython-vcnl4010'
# TODO need to add a script that runs this and fires the gun on change
# TODO need to run a service in the background for this script