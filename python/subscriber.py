import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print(f'received message: {message.payload.decode()}')

client = mqtt.Client('subber')
client.connect('localhost', 1883)

client.loop_start()
client.subscribe('health_monitoring')

client.on_message = on_message

time.sleep(30)

client.loop_stop()