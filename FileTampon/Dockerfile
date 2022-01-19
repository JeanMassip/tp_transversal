FROM python:3.8-alpine
# Copie des fichiers d'applicatif et entrypoint
COPY main.py requirements.txt entrypoint.sh .
# Mise à jour du dépôt et des paquets
RUN apk update && apk upgrade
# Installation des paquets essentiels
RUN apk add openssh-server openssh-client syslog-ng bind-tools
# Copie du fichier de conf syslog
COPY filetamponsyslog-ng.conf /etc/syslog-ng/
# Instllation des dépendances pythons
RUN pip install -r requirements.txt
# Définition de l'entrypoint à lancer
# au démaragge du container
ENTRYPOINT ["./ip.sh"]
