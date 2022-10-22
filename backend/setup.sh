pip install -r requirements.txt
sudo apt-get install rabbitmq-server
sudo rabbitmq-server start --detached
sudo rabbitmqctl add_user lyrical lyrical
sudo rabbitmqctl add_vhost lyrical
sudo rabbitmqctl set_permissions -p lyrical lyrical ".*" ".*" ".*"
celery -A app.celery worker --detached
git clone https://github.com/Andydid1/DeforumStableDiffusionLocal.git
# sh ./DeforumStableDiffusionLocal/env_setup.sh