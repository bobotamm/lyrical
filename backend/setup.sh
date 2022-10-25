sudo rabbitmq-server start --detach
sudo rabbitmqctl add_user lyrical lyrical
sudo rabbitmqctl add_vhost lyrical
sudo rabbitmqctl set_permissions -p lyrical lyrical ".*" ".*" ".*"