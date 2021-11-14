import paho.mqtt.client as mqtt

class mqtt_client:

    def __init__(self, host = 'localhost', port = 9001) -> None:

        self.client = mqtt.Client(transport='websockets')
        
        # if we should need username and password to connect to the broker
        # client.username_pw_set(username="edge",password="cloud")

        # callback function
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connected_flag = False
        self.client.disconnect_flag = True

        try:
            self.client.connect(host,port) #connect to broker
        except:
            print('connection failed')
            exit(1)


    def __on_connect(self, client, userdata, flags, rc):
        if rc==0:
            self.client.connected_flag = True
            self.client.disconnect_flag = False
            print("connected OK")
        else:
            print("Bad connection Returned code=",rc)

    def __on_disconnect(self, client, userdata, rc):
        print("disconnecting reason  "  +str(rc))
        self.client.connected_flag = False
        self.client.disconnect_flag = True

    def publish(self, topic:str, data):
        self.client.publish(topic, data)
        #print(f'health_monitoring: {data}')

    def subcribe(self, topic:str):
        self.client.subscribe(topic)
        print(f'subscribed: {topic}')

    def set_on_message(self, func):
        self.client.on_message = func
        self.client.loop_start()
