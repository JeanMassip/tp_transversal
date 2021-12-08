import logging
import queue, threading, json, datetime

from paho.mqtt import client as mqtt_client

class DENMHandler:
    def __init__(self, host, port, message_queue:queue.Queue) -> None:
        self.message_queue = message_queue
        self.nb_jam = 0
        self.vehicules = {}
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("DENM_Handler connected to MQTT Broker")
            else:
                logging.error("DENM_Handler failed to connect to MQTT Broker")
        
        self.client = mqtt_client.Client()
        self.client.on_connect = on_connect
        self.client.connect(host, port)
    
    def __del__(self) -> None:
        self.client.disconnect()
    
    def handle_message(self, event:threading.Event) -> None:
        while not event.is_set() or not self.message_queue.empty():
            message = self.message_queue.get()
            data = json.load(message)
            msg = data["message"]
            vehicule_id = msg["station_id"]

            if vehicule_id in self.vehicules.keys():
                self.vehicules[vehicule_id].append(int(msg["causeCode"]))
            else:
                self.vehicules[vehicule_id] = [int(msg["causeCode"])]

class CAMHandler:
    def __init__(self, host, port, message_queue:queue.Queue) -> None:
        self.message_queue = message_queue
        self.nb_slowed = 0
        self.vehicules = {}
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("CAM_Handler connected to MQTT Broker")
            else:
                logging.error("CAM_Handler failed to connect to MQTT Broker")
        
        self.client = mqtt_client.Client()
        self.client.on_connect = on_connect
        self.client.connect(host, port)
    
    def __del__(self) -> None:
        self.client.disconnect()
    
    def handle_message(self, event:threading.Event) -> None:
        while not event.is_set() or not self.message_queue.empty():
            message = self.message_queue.get()
            data = json.load(message)
            msg = data["message"]
            vehicule_id = msg["station_id"]

            if vehicule_id in self.vehicules.keys():
                self.vehicules[vehicule_id]["speed"] = msg["speed"]
            else:
                self.vehicules[vehicule_id] = msg
            
            self.vehicules[vehicule_id]["last_seen"] = datetime.datetime.now()
            self.vehicules[vehicule_id]["slowed"] = False

            self.purge_vehicules()
            self.check_speed()

    def check_speed(self) -> None:
        for index, vehicule in self.vehicules:
            if vehicule["speed"] >= 80 and vehicule["slowed"] == True:
                vehicule["slowed"] = False
                self.nb_slowed += 1

            if vehicule["speed"] < 80:
                vehicule["slowed"] = True
                self.nb_slowed += 1
            
            if self.nb_slowed > 2:
                self.send_slowed_event(index)
    
    def purge_vehicules(self) -> None:
        now = datetime.datetime.now()
        for index, vehicule in self.vehicules:
            last_seen = vehicule["last_seen"]
            if ((now - last_seen).second) > 15:
                del self.vehicules[index]

    def send_slowed_event(self, index) -> None:
        message = {
            "message": {
                "stationID": self.vehicules[index]["stationID"],
                "stationType": self.vehicules[index]["stationType"],
                "causeCode": 5,
                "position": "une position"
            }
        }
        
        msg = json.dumps(message)
        result = self.client.publish("/gw/events", msg)
        status = result[0]
        if status == 0:
            logging.info("Message sent !")
        else:
            logging.error(f"Failed to send message, error : {status}")
            
