PI_IP=pi@$1
COLOR="$2"
valid_colors=("blue" "pink" "yellow")
if [[ ! $valid_colors =~ $COLOR ]]; then
    echo "invalid color"
    exit 1
fi

ssh-copy-id -i ~/.ssh/id_rsa.pub $PI_IP

./generate_index_server $COLOR

ssh $PI_IP "sudo apt update -y && sudo pip install flask &&\
    sudo apt-get install -y raspberrypi-ui-mods xinit xserver-xorg &&\
    sudo apt-get install -y xrdp"

cd index && provision.sh $PI_IP
cd .. && cd collision-detection && provision.sh $PI_IP
cd .. && cd motors && provision.sh $PI_IP
cd .. && cd tone_generator && provision.sh $PI_IP
cd .. && cd tone_generator && provision.sh $PI_IP

# TODO watergun provisions

ssh $PI_IP 'sudo reboot'


