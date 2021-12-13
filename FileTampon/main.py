import logging, pika
from paho.mqtt import client as mqtt_client

def main():
    #Receive message from MQTT broker
    client = mqtt_client.Client("FileTampon")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect()
    client.subscribe("/denm/save")
    logging.info("started listening for messages on /denm/save")
    client.loop_start()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to the MQTT Broker !")
    else:
        logging.error("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    logging.DEBUG("MESSAGE RECEIVED")
    message = msg.payload.decode("utf-8")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='denm_save')
    channel.basic_publish(exchange='', routing_key='denm_save', body=message)
    logging.info("Message sent to queue")
    connection.close()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    main()
