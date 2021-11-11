# publisher
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

client = mqtt.Client('publisher')
client.connect('localhost', 1883)
#client.connect('mqtt.eclipseprojects.io')


while True:
    randNumber = uniform(20.0, 21.0)
    client.publish('health_monitoring', randNumber)
    print(f'Just published {randNumber:10.2f} to Topic health_monitoring')
    time.sleep(1)
