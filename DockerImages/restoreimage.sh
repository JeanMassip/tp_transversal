#!/bin/bash
# Programme qui va restorer une image docker qui a été
# sauvegardée au fomat .tar
# Argument à fournir : nom du fichier .tar de l'image
# à restorer
# Utilisation restoreimage.sh <NomImageARestorer.tar>
# ! A lancer avec les droits sudo.

sudo docker load < $1
