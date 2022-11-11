pip install -r requirements.txt
sudo apt-get install rabbitmq-server -y
sudo rabbitmq-server -detached
sudo rabbitmqctl add_user lyrical lyrical
sudo rabbitmqctl add_vhost lyrical
sudo rabbitmqctl set_permissions -p lyrical lyrical ".*" ".*" ".*"
git clone https://github.com/Andydid1/DeforumStableDiffusionLocal.git
git clone https://github.com/fashni/MxLRC.git
# sh ./DeforumStableDiffusionLocal/env_setup.sh
