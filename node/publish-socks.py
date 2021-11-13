#Note demo scripts have limited or no error detection and use
#timers to wait for events. They assume everything works ok
#www.steves-internet-guide.com
#contact steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
##Grateful for any feedback
#uses websockets publish-subscribe and receive message
import paho.mqtt.client as paho
import time
broker="broker.mqttdashboard.com"
broker="iot.eclipse.org"
broker="localhost"
#port= 80
#port=1883
port= 9001
sub_topic="health_monitoring"

def on_message(client, userdata, message):
    print(f'received message: {message.payload.decode()}')

client= paho.Client("subscriber", transport='websockets')       #create client object

client.on_message = on_message        #assign function to callback

print("connecting to broker ",broker,"on port ",port)
client.connect(broker,port)           
client.loop_start()
print("subscribing to ",sub_topic)
client.subscribe(sub_topic)
time.sleep(4)

client.disconnect()

