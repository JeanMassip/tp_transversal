import queue

from paho.mqtt import client as mqtt_client

class Receiver:
    def __init__(self, host, port) -> None:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client()
        self.client.on_connect = on_connect
        self.client.connect(host, port)
    
    def __del__(self):
        self.client.disconnect()
    
    def start(self, queue:queue.Queue, topic):
        def on_message(client, userdata, msg):
            message = msg.payload.decode("utf-8")
            queue.put(message)
        
        self.client.on_message = on_message
        self.client.subscribe(topic)
    
    def stop(self, topic):
        self.client.unsubscribe(topic)