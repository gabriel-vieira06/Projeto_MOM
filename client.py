from tkinter import *
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import json
from application.configs.broker_configs import mqtt_broker_configs

client_count  = 0

topics = []

thread_active = True

class ClientCard:

    global client_count

    def __init__(self):
        self.selected_topics = []
        self.text_box        = None
        self.msg             = None

    def lambda_show_message(self):
        self.text_box.insert(END, self.msg+"\n")
        
    def show_message(self, client, userdata, message):
        self.msg = message.payload.decode()
        GUI_Clientes.after(10, self.lambda_show_message)
    
    def client_connected(self, client, userdata, flags, reason_code, properties):

        chosen_topics = []
        def get_selected_topics():
            for i, var in enumerate(self.selected_topics):
                if var == 1:
                    chosen_topics.append(topics[i])
        
        if reason_code == 0:
            get_selected_topics()
            for topic in chosen_topics:
                client.subscribe(f'{mqtt_broker_configs["TOPIC"]}/{topic}')
        else:
            print(f'ERRO: {reason_code}')
        

def create_client():

    global client_count

    client_card = ClientCard()

    def connect_client_wrapper():
        connect_client(client_card)

    def update_client_topics():
        for i in range(len(topic_selection)):
            client_card.selected_topics[i] = topic_selection[i].get()


    topic_title_label = Label(GUI_Clientes, text="Tópicos disponíveis:")
    topic_title_label.grid(column=0)

    count_rows = 0
    topic_selection = [IntVar() for _ in range(len(topics))]

    for i,topic in enumerate(topics):
        topic_selection[i] = IntVar(GUI_Clientes)
        topic_selection[i].set(0)
        topic_check     = Checkbutton(GUI_Clientes, text=topic, variable=topic_selection[i], command=update_client_topics)
        topic_check.grid(column=0, sticky="w")
        client_card.selected_topics.append(topic_selection[i].get())
        count_rows += 1
    
    message_text = scrolledtext.ScrolledText(GUI_Clientes, width=50, height=10)
    message_text.grid(column=1, 
                      row=topic_title_label.grid_info()['row']+1, 
                      rowspan=count_rows)
    
    client_card.text_box = message_text

    button_connect_client = Button(GUI_Clientes, text="Conectar Cliente", command=connect_client_wrapper)
    button_connect_client.grid(column=1)

def connect_client(client_card: ClientCard):

    mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.on_connect = client_card.client_connected
    mqtt_client.on_message = client_card.show_message

    mqtt_client.connect(host=mqtt_broker_configs["HOST"],
                        port=mqtt_broker_configs["PORT"],
                        keepalive=mqtt_broker_configs["KEEPALIVE"])

    mqtt_client.loop_start()

def get_topics():

    def topic_callback(client, userdata, message):
        global topics
        
        topics = json.loads(message.payload.decode())

    def topic_subscribe(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            client.subscribe(f'{mqtt_broker_configs["TOPIC"]}/topics')
        else:
            print(f'ERRO: {reason_code}')

    mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    mqtt_client.on_connect = topic_subscribe
    mqtt_client.on_message = topic_callback

    mqtt_client.connect(host=mqtt_broker_configs["HOST"],
                        port=mqtt_broker_configs["PORT"],
                        keepalive=mqtt_broker_configs["KEEPALIVE"])
    
    mqtt_client.loop_start()
    
GUI_Clientes = Tk()

GUI_Clientes.title("Projeto MOM - Clientes")

# LABEL TITULO DA JANELA DOS CLIENTES
client_title_label = Label(GUI_Clientes, text="Configuração dos Clientes")
client_title_label.grid(column=1, row=0, columnspan=5)

# ADICIONA CLIENTE
button_add_client  = Button(GUI_Clientes, text="Criar Cliente", command=create_client)
button_add_client.grid(column=0,row=1)

get_topics()

GUI_Clientes.mainloop()
