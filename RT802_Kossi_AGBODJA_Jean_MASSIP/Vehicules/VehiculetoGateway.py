#!/usr/bin/python3
##############################################
# Programme d'envoie du certificat et des
# messages MQTT à la gateway
##############################################

import getopt, sys, os
import random, time
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding


from vehicule import Vehicule, VehiculeType
from dotenv import load_dotenv

load_dotenv()
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES"))
SLOW_START = int(os.getenv("SL OW_START"))
SLOW_STOP = int(os.getenv("SLOW_STOP"))

def main(argv):
    Gateway_url="http://urlgateway:5000/auth"
    Crt_file = "crtvehicule.pem"

    try:
        with open(Crt_file, "r") as Crt_file_object:
            public_key = serialization.load_pem_public_key(Crt_file_object.read(),backend=default_backend())
    except:
        print("[-] Impossible de charger le certificat du véhicule")
        raise

    try:
        response=requests.post(Gateway_url,data=public_key)
    except :
        print("[-] Impossible d'envoyer le certificat à la gateway")
        raise

    # Si le gateway envoie un OK, alors
    # on envoie les messages MQTT

    if response.status_code==200:

        type = VehiculeType.ORDINARY
        sentMessages = 0

        try:
            opts, args = getopt.getopt(argv, "ht:", ["type="])
        except getopt.GetoptError:
            print('main.py -t <vehicule type: ORDINARY, EMERGENCY, OPERATOR>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('main.py -t <vehicule type: ORDINARY, EMERGENCY, OPERATOR>')
                sys.exit()
            elif opt in ("-t", "--type"):
                if arg == 'ORDINARY':
                    type = VehiculeType.ORDINARY
                elif arg == "EMERGENCY":
                    type = VehiculeType.EMERGENCY
                elif arg == "OPERATOR":
                    type == VehiculeType.OPERATOR

        vec = Vehicule(random.randint(1, 1000), type)

        while sentMessages < MAX_MESSAGES:
            time.sleep(1)
            if sentMessages < SLOW_START:
                vec.default()
            elif sentMessages > SLOW_START and sentMessages < SLOW_STOP:
                vec.slowed()
            else:
                vec.default()
            sentMessages += 1
    else:
        print("[-] La vérification du certificat du véhicule a échoué")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print('main.py -t <vehicule type: ORDINARY, EMERGENCY, OPERATOR>')
        sys.exit(2)
