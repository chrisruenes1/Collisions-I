if [[ -z $1 ]]; then
    echo 'must specify target ip address';
    exit 1;
fi
PI_IP=$1
scp index_server.py $PI_IP:~/Desktop
scp start-index-flask-server.service $PI_IP:~
scp environment.conf $PI_IP:~
ssh $PI_IP 'sudo mv start-index-flask-server.service /usr/lib/systemd/system &&\
    sudo mkdir /etc/systemd/system/start-index-flask-server.service.d &&\
    sudo mv environment.conf /etc/systemd/system/start-index-flask-server.service.d &&\
    sudo systemctl enable start-index-flask-server'
