import getopt, sys
import random, time 

from vehicule import Vehicule, VehiculeType

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

    while sentMessages < 35:
        time.sleep(1)
        if sentMessages < 10:
            vec.default()
        elif sentMessages > 10 and sentMessages < 20:
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