from typing import Callable
import paho.mqtt.client as mqtt
import time


class mqtt_client:

    def __init__(self, host: str, port: int, reconnect_interval: float) -> None:

        self.client = mqtt.Client(transport='websockets')

        # if we should need username and password to connect to the broker
        # client.username_pw_set(username="edge",password="cloud")

        # callback functions
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connected_flag = False
        self.client.disconnect_flag = True

        self.__connect(host, port, reconnect_interval)

    def __connect(self, host: str, port: int, reconnect_interval: float) -> None:
        try:
            # connect to broker
            self.client.connect(host, port)
        except:
            print('Connection failed. Trying again...')
            time.sleep(reconnect_interval)
            self.__connect(host, port, reconnect_interval)

    def __on_connect(self, client, userdata, flags, rc) -> None:
        if rc == 0:
            self.client.connected_flag = True
            self.client.disconnect_flag = False
            print("Connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def __on_disconnect(self, client, userdata, rc) -> None:
        print("Disconnecting reason  " + str(rc))
        self.client.connected_flag = False
        self.client.disconnect_flag = True

    def publish(self, topic: str, data) -> None:
        self.client.publish(topic, data)
        #print(f'health_monitoring: {data}')

    def subcribe(self, topic: str) -> None:
        self.client.subscribe(topic)
        print(f'Subscribed: {topic}')

    def set_on_message(self, func: Callable) -> None:
        self.client.on_message = func
        self.client.loop_start()
