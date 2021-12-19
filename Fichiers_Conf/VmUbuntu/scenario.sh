#!/bin/bash
##########################################
# Script de lancement du scenario
# des véhicules
##########################################

# Definition des variables d'environnement

SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

# Definition des variables de type de véhicule

ORDINARY=ORDINARY
EMERGENCY=EMERGENCY
OPERATOR=OPERATOR

# Definition de variables globales

LOG=/var/log/vehicule.log

# Selection aléatoire d'un type de véhicule

ARRAY=($ORDINARY $EMERGENCY $OPERATOR)
NUMRANDOM=$((RANDOM%3))
TYPE=${ARRAY[$NUMRANDOM]}

#echo "TYPE=$TYPE"

# Test d'Exécution du script avec un type de véhicule

date >> $LOG 2>&1

#echo "/usr/local/bin/main.py -t $TYPE" >> $LOG

/usr/local/bin/main.py -t $TYPE >> $LOG 2>&1
