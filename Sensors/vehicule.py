import random, json

from enum import Enum
from paho.mqtt import client as mqtt


class VehiculeType(str, Enum):
    ORDINARY = 5
    EMERGENCY = 10
    OPERATOR = 15


broker = "localhost"
port = 1883

class Vehicule:
    def __init__(self, stationID:int, stationType:VehiculeType) -> None:
        self.stationID = stationID
        self.stationType = stationType
        self.heading = random.choice([0,180])
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt.Client(f'mqtt-station-{stationID}')
        #client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(broker, port)

    def __del__(self):
        self.client.disconnect()
        
    
    def default(self) -> None:
        message = {
            "message": {
                "station_ID": self.stationID,
                "station_type": self.stationType,
                "speed": random.randint(80, 90),
                "heading": self.heading,
                "position": "une position"
            }
        }

        self._send_message(message, "/sensors/cam")

    def slowed(self) -> None:
        message = {
            "message": {
                "station_ID": self.stationID,
                "station_type": self.stationType,
                "speed": random.randint(30, 50),
                "heading": self.heading,
                "position": "une position"
            }
        }

        self._send_message(message, "/sensors/cam")
    
    def _send_message(self, message:dict, topic:str) -> None:
        msg = json.dumps(message)
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Message sent !")
        else:
            print(f"Failed to send message...")


