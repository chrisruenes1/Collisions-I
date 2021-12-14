if [[ -z $1 ]]; then
    echo 'must specify target ip address';
    exit 1;
fi
PI_IP=$1
scp start-tone-generator-flask-server.service $PI_IP:~
scp environment.conf $PI_IP:~
scp -r tone_generator_code $PI_IP:~/Desktop
scp -r tone_generator_dependencies $PI_IP:~/Desktop
scp -r utils $PI_IP:~/Desktop

ssh $PI_IP 'sudo mv start-tone-generator-flask-server.service /usr/lib/systemd/system &&\
    sudo mkdir /etc/systemd/system/start-tone-generator-flask-server.service.d &&\
    sudo mv environment.conf /etc/systemd/system/start-tone-generator-flask-server.service.d &&\
    sudo systemctl enable start-tone-generator-flask-server'