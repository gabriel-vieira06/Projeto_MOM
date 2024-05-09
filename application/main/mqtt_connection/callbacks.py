from application.configs.broker_configs import mqtt_broker_configs

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f'CONECTADO AO TÓPICO: {client}')
        client.subscribe(f'{mqtt_broker_configs["TOPIC"]}/#')
    else:
        print(f'ERRO: {reason_code}')

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    print(f'CLIENTE INSCRITO EM {mqtt_broker_configs["TOPIC"]}')

def on_message(client, userdata, message):
    print(f'MESSAGEM RECEBIDA: {message.payload}')
    print(f'TOPICO REMETENTE: {message.topic}')

