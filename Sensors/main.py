import getopt, sys, os
import random, time 

from vehicule import Vehicule, VehiculeType
from dotenv import load_dotenv

load_dotenv()
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES"))
SLOW_START = int(os.getenv("SLOW_START"))
SLOW_STOP = int(os.getenv("SLOW_STOP"))

def main(argv):
    type = VehiculeType.ORDINARY
    sentMessages = 0

    try:
        opts, args = getopt.getopt(argv,"ht:",["type="])
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
    
    vec = Vehicule(random.randint(0,1000), type)

    while sentMessages < MAX_MESSAGES:
        time.sleep(1)
        if sentMessages < SLOW_START:
            vec.default()
        elif sentMessages > SLOW_START and sentMessages < SLOW_STOP:
            vec.slowed()
        else:
            vec.default()
        sentMessages += 1



if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print('main.py -t <vehicule type: ORDINARY, EMERGENCY, OPERATOR>')
        sys.exit(2)