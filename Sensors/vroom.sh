#!/bin/bash
###########################################
# Script de lancement des véhicules LXC
# Date de modif : 10/01/2022
# Auteur : kossivijunior@yahoo.fr
# Version : 1.0
###########################################

# Déclaration du nom des véhicules

vehicules=(1 2 3)

# Lancement des Véhicules

for vehicule in ${vehicules[@]}

do
	sudo lxc-copy --name=vehiculemodel -N $vehicule -e
done

# Attente de X minutes pour laisser le temps aux containers
# d exécuter le script et d envoyer les message à la passerelle

sleep 30

# Une fois le temps d'attente écoulé, on arrête les containers

# Arrêt  des Véhicules

for vehicule in ${vehicules[@]}

do

sudo lxc-stop $vehicule

done
