import logging

from paho.mqtt import client as mqtt_client

def main():
    client = mqtt_client.Client("EventCentral")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect()
    client.subscribe("/gw/denm")
    logging.info("started listening for messages on /gw/denm")
    client.loop_start()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to the MQTT Broker !")
    else:
        logging.error("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    logging.DEBUG("MESSAGE RECEIVED")
    message = msg.payload.decode("utf-8")
    logging.info("Message published to queue")
    client.publish(topic="/denm/latest", payload=message)
    client.publish(topic="/denm/save", payload=message)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    main()
