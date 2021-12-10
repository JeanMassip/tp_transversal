import logging
import queue, threading, json, datetime
import random

from paho.mqtt import client as mqtt_client
from enum import IntEnum

class DENMEvent(IntEnum):
    ROADWORK = 3
    ACCIDENT = 4
    TRAFFICJAM = 5
    SLIPPERYROAD = 6
    FOG = 7

class DENMHandler:
    def __init__(self, host, port, message_queue:queue.Queue) -> None:
        self.message_queue = message_queue
        self.nb_jam = 0
        self.vehicules = {}
        self.client = mqtt_client.Client(f"Handler-{random.randint(0,100)}")
        self.client.on_connect = self.on_connect
        self.client.connect(host, port)
        self.client.loop_start()
    
    def __del__(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("DENM_Handler connected to MQTT Broker")
        else:
            logging.error("DENM_Handler failed to connect to MQTT Broker")
        
    
    def handle_message(self, event:threading.Event) -> None:
        while not event.is_set() or not self.message_queue.empty():
            message = self.message_queue.get()
            data = json.loads(message)
            msg = data["message"]
            vehicule_id = msg["station_id"]

            if vehicule_id in self.vehicules.keys():
                self.vehicules[vehicule_id]["events"].append(DENMEvent(int(msg["cause_code"])))
            else:
                if int(msg["cause_code"]) not in self.vehicules[vehicule_id]:
                    self.vehicules[vehicule_id]["events"].append(DENMEvent(int(msg["cause_code"])))
            
            self.vehicules[vehicule_id]["last_seen"] = datetime.datetime.now()
    
    def checkEvents(self):
        for data in DENMEvent:
            occurences = 0
            for key, vehicule in self.vehicules.items():
                if data.value in vehicule["events"]:
                    occurences += 1
            if occurences > 2:
                self.raiseEvent(data.value)
    
    def raiseEvent(self, eventID):
        logging.info("Raising Event")
        message = {
            "message": {
                "station_id": 0,
                "station_type": 0,
                "cause_code": eventID,
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

            

class CAMHandler:
    def __init__(self, host, port, message_queue:queue.Queue) -> None:
        self.message_queue = message_queue
        self.nb_slowed = 0
        self.vehicules = {}
        
        self.client = mqtt_client.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(host, port)
        self.client.loop_start()
    
    def __del__(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("CAM_Handler connected to MQTT Broker")
        else:
            logging.error("CAM_Handler failed to connect to MQTT Broker")
    
    def handle_message(self, event:threading.Event) -> None:
        while not event.is_set() or not self.message_queue.empty():
            message = self.message_queue.get()
            logging.debug("Handling message")
            data = json.loads(message)
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
        for key, vehicule in self.vehicules.items():
            if vehicule["speed"] >= 80 and vehicule["slowed"] == True:
                vehicule["slowed"] = False
                self.nb_slowed += 1

            if vehicule["speed"] < 80:
                vehicule["slowed"] = True
                self.nb_slowed += 1
            
            if self.nb_slowed > 2:
                self.send_slowed_event(key)
    
    def purge_vehicules(self) -> None:
        now = datetime.datetime.now()
        for key, vehicule in self.vehicules.items():
            last_seen = vehicule["last_seen"]
            if ((now - last_seen).seconds) > 15:
                del self.vehicules[key]

    def send_slowed_event(self, index) -> None:
        logging.info("Sendind Trafic JAM Event")
        message = {
            "message": {
                "station_id": self.vehicules[index]["stationID"],
                "station_type": self.vehicules[index]["stationType"],
                "cause_code": DENMEvent.TRAFFICJAM,
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
            
