import logging
import queue
import random

from paho.mqtt import client as mqtt_client

class Receiver:
    def __init__(self, host, queue:queue.Queue) -> None:  
        self.client = mqtt_client.Client(f"receiver-{random.randint(0,100)}")
        self.message_queue = queue
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.host = host
    
    def __del__(self):
        self.client.disconnect()
    
    def start(self, queue:queue.Queue, topic):
        logging.info(f"Started listening for messages on {topic}")
        self.client.connect(self.host)
        self.client.subscribe(topic)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        logging.debug("MESSAGE RECEIVED")
        message = msg.payload.decode("utf-8")
        self.message_queue.put(message)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.error("Failed to connect, return code %d\n", rc)


    
    def stop(self, topic):
        self.client.loop_stop()
        self.client.unsubscribe(topic)

