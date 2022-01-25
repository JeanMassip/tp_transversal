import logging
import queue
import threading
import json
import datetime
import random

from paho.mqtt import client as mqtt_client
from enum import IntEnum


class DENMEvent(IntEnum):
    NORMAL = 1
    ROADWORK = 3
    ACCIDENT = 4
    TRAFFICJAM = 5
    SLIPPERYROAD = 6
    FOG = 7


class DENMHandler:
    def __init__(self, host, port, message_queue: queue.Queue) -> None:
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

    def handle_message(self, event: threading.Event) -> None:
        while not event.is_set() or not self.message_queue.empty():
            message = self.message_queue.get()
            data = json.loads(message)
            msg = data["message"]
            vehicule_id = msg["station_id"]

            if vehicule_id in self.vehicules.keys():
                self.vehicules[vehicule_id]["events"].append(
                    DENMEvent(int(msg["cause_code"])))
            else:
                if int(msg["cause_code"]) not in self.vehicules[vehicule_id]:
                    self.vehicules[vehicule_id]["events"].append(
                        DENMEvent(int(msg["cause_code"])))

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
    def __init__(self, host, port, message_queue: queue.Queue) -> None:
        self.message_queue = message_queue
        self.nb_slowed = 0
        self.vehicules = {}
        self.slowed = False

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

    def handle_message(self, event: threading.Event) -> None:
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
            if self.vehicules[vehicule_id]["speed"] >= 80:
                self.vehicules[vehicule_id]["slowed"] = False
            else:
                self.vehicules[vehicule_id]["slowed"] = True

            self.check_speed()

    def check_speed(self) -> None:
        nbslowed = 0
        for key, vehicule in self.vehicules.items():
            if vehicule["speed"] < 80:
                nbslowed += 1
        print(nbslowed)
        if nbslowed > 2 and not self.slowed:
            self.slowed = True
            self.send_slowed_event(key)

        if nbslowed <= 2 and self.slowed:
            self.slowed = False
            self.send_normal_event(key)

    def purge_vehicules(self) -> None:
        now = datetime.datetime.now()
        toDelete = []
        for key, vehicule in self.vehicules.items():
            last_seen = vehicule["last_seen"]
            if ((now - last_seen).seconds) > 15:
                toDelete.append(key)

        for key in toDelete:
            del self.vehicules[key]

    def send_slowed_event(self, index) -> None:
        logging.info("Sending Trafic JAM Event")
        logging.debug(self.vehicules[index])
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        message = {
            "message": {
                "station_id": self.vehicules[index]["station_id"],
                "station_type": self.vehicules[index]["station_type"],
                "cause_code": DENMEvent.TRAFFICJAM,
                "cause_name": "Ralentissements",
                "position": "une position",
                "time": dt_string
            }
        }

        msg = json.dumps(message)
        result = self.client.publish("/gw/events", msg)
        status = result[0]
        if status == 0:
            logging.info("Message sent !")
        else:
            logging.error(f"Failed to send message, error : {status}")

    def send_normal_event(self, index) -> None:
        logging.info("Sending Normal Event")
        logging.debug(self.vehicules[index])
        message = {
            "message": {
                "station_id": self.vehicules[index]["station_id"],
                "station_type": self.vehicules[index]["station_type"],
                "cause_code": DENMEvent.NORMAL,
                "cause_name": "Normal",
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
