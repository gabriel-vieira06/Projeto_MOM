import paho.mqtt.client as mqtt
from application.configs.broker_configs import mqtt_broker_configs

mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                          client_id='Sensor')
mqtt_client.connect(host=mqtt_broker_configs["HOST"],
                    port=mqtt_broker_configs["PORT"])
mqtt_client.publish(topic=mqtt_broker_configs["TOPIC"],
                    payload="MENSAGEM TESTE")