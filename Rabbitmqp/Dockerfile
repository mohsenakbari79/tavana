FROM rabbitmq:3.8-management
COPY ./rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
RUN rabbitmq-plugins enable --offline rabbitmq_auth_backend_http rabbitmq_mqtt  
