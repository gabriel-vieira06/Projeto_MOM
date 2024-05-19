from tkinter import *
import json
import paho.mqtt.client as mqtt
from random import randint
from application.configs.broker_configs import mqtt_broker_configs

sensor_count  = 0
client_count  = 0

topics = []

thread_active = True

class SensorCard:

    global sensor_count
    global topics

    def __init__(self):
        self.name          = None
        self.period        = None
        self.topic         = None
        self.min           = None
        self.max           = None
        self.static_value  = None
        self.value_choice  = None

    def get_name(self):
        return self.name.get()
    
    def get_period(self):
        return int(self.period.get())
    
    def get_topic(self):
        sensor_topic = self.topic.get()
        if sensor_topic not in topics:
            topics.append(sensor_topic)
        return self.topic.get()
    
    def get_min(self):
        return int(self.min.get())
    
    def get_max(self):
        return int(self.max.get())
    
    def get_static_value(self):
        return int(self.static_value.get())
    
    def get_value_choice(self):
        return self.value_choice.get()

def create_sensor():

    global sensor_count

    sensor_card = SensorCard()

    # NOME DO SENSOR
    name_label  = Label(GUI_Sensores, text="NOME")
    name_label.grid(column=0)
    name_string = StringVar(GUI_Sensores)
    name_string.set(f'Sensor {sensor_count}')
    Entry(GUI_Sensores, textvariable=name_string).grid(column=1, row=name_label.grid_info()['row'])

    # PERÍODO DE AMOSTRA DO SENSOR
    period_label  = Label(GUI_Sensores, text="PERÍODO")
    period_label.grid(column=0)
    period_string = StringVar(GUI_Sensores)
    period_string.set('5')
    Entry(GUI_Sensores, textvariable=period_string).grid(column=1, row=period_label.grid_info()['row'])
    
    # TÓPICO DO SENSOR
    topic_label   = Label(GUI_Sensores, text="TÓPICO")
    topic_label.grid(column=0)
    topic_string  = StringVar(GUI_Sensores)
    topic_string.set('exemplo')
    Entry(GUI_Sensores, textvariable=topic_string).grid(column=1, row=topic_label.grid_info()['row'])

    # VALOR MÍNIMO
    min_label     = Label(GUI_Sensores, text="MIN")
    min_label.grid(column=2, row=name_label.grid_info()['row'])
    min_string    = StringVar(GUI_Sensores)
    min_string.set('0')
    Entry(GUI_Sensores, textvariable=min_string).grid(column=3, row=min_label.grid_info()['row'])

    # VALOR MÁXIMO
    max_label     = Label(GUI_Sensores, text="MAX")
    max_label.grid(column=4, row=name_label.grid_info()['row'])
    max_string    = StringVar(GUI_Sensores)
    max_string.set('10')
    Entry(GUI_Sensores, textvariable=max_string).grid(column=5, row=max_label.grid_info()['row'])
   
    # VALOR ESTÁTICO
    static_label  = Label(GUI_Sensores, text="VALOR ESTÁTICO")
    static_label.grid(column=2, row=period_label.grid_info()['row'])
    static_string = StringVar(GUI_Sensores)
    static_string.set('5')
    Entry(GUI_Sensores, textvariable=static_string).grid(column=3, row=static_label.grid_info()['row'], columnspan=3)

    # RADIO BUTTONS
    radio_choice  = IntVar()
    radio_choice.set(1)
    Radiobutton(GUI_Sensores, variable=radio_choice, value=1).grid(column=6, row=max_label.grid_info()['row'])
    Radiobutton(GUI_Sensores, variable=radio_choice, value=2).grid(column=6, row=static_label.grid_info()['row'])

    sensor_count += 1

    sensor_card.name = name_string
    sensor_card.period = period_string
    sensor_card.topic = topic_string
    sensor_card.min = min_string
    sensor_card.max = max_string
    sensor_card.static_value = static_string
    sensor_card.value_choice = radio_choice

    publish_sensor(sensor_card)


def publish_sensor(sensor: SensorCard):
    mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.connect(host=mqtt_broker_configs["HOST"],
                        port=mqtt_broker_configs["PORT"])
    
    def send_message():
        if sensor.get_value_choice() == 1:
            sensor_read = randint(sensor.get_min(), sensor.get_max())
        else:
            sensor_read = sensor.get_static_value()
        
        if sensor.get_value_choice() == 1 and sensor_read == sensor.get_max():
            mqtt_client.publish(topic=f'{mqtt_broker_configs["TOPIC"]}/{sensor.get_topic()}',
                            payload=f'Leitura do {sensor.get_name()}: {sensor_read} (MÁXIMO)')
        else:
            mqtt_client.publish(topic=f'{mqtt_broker_configs["TOPIC"]}/{sensor.get_topic()}',
                                payload=f'Leitura do {sensor.get_name()}: {sensor_read}')
        
        GUI_Sensores.after(1000*sensor.get_period(), send_message)
    
    send_message()

def send_topics():

    global topics

    mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.connect(host=mqtt_broker_configs["HOST"],
                        port=mqtt_broker_configs["PORT"])
    
    def publish_topics():
        mqtt_client.publish(topic=f'{mqtt_broker_configs["TOPIC"]}/topics', payload=f'{json.dumps(topics)}')
        GUI_Sensores.after(1000, publish_topics)
    
    publish_topics()


GUI_Sensores = Tk()

GUI_Sensores.title("Projeto MOM - Sensores")

# LABEL TITULO DA JANELA DOS SENSORES
sensor_title_label = Label(GUI_Sensores, text="Configuração dos Sensores")
sensor_title_label.grid(column=1, row=0, columnspan=5)

# ADICIONA SENSOR
button_add_sensor  = Button(GUI_Sensores, text="Criar Sensor", command=create_sensor)
button_add_sensor.grid(column=0,row=1)

send_topics()

GUI_Sensores.mainloop()
