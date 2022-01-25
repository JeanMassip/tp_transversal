import pika, sys, os, logging, requests

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='denm_save')
    channel.basic_consume(queue='denm_save', on_message_callback=callback, auto_ack=True)
    logging.info("Started consumming on denm_save")
    channel.start_consuming()

def callback(ch, method, properties, body):
    logging.info("message received")
    res = requests.post("http://apibdd:5000/events", data=body)
    if res.ok:
        logging.info("Event stored in db")
    else:
        logging.error("Could not store event in db")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    main()
