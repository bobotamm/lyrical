<<<<<<< HEAD
sudo rabbitmq-server start --detach
sudo rabbitmqctl add_user lyrical lyrical
sudo rabbitmqctl add_vhost lyrical
sudo rabbitmqctl set_permissions -p lyrical lyrical ".*" ".*" ".*"
=======
pip install -r requirements.txt
sudo apt-get install rabbitmq-server
sudo rabbitmq-server -detached
sudo rabbitmqctl add_user lyrical lyrical
sudo rabbitmqctl add_vhost lyrical
sudo rabbitmqctl set_permissions -p lyrical lyrical ".*" ".*" ".*"
celery -A app.celery worker --pool=solo --concurrency=1 --detach
git clone https://github.com/Andydid1/DeforumStableDiffusionLocal.git
# sh ./DeforumStableDiffusionLocal/env_setup.sh
>>>>>>> fbf274906c5f46225e092f2576f3050feac4e8c3
