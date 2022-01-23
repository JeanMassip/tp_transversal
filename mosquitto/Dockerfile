FROM alpine:latest
#FROM eclipse-mosquitto:latest
# Copie des fichiers d'applicatif et entrypoint
#COPY main.py requirements.txt handler.py receiver.py 
COPY entrypoint.sh ./
# Mise à jour du dépôt et des paquets
RUN apk update && apk upgrade
# Installation des paquets essentiels
RUN apk add openssh-server openssh-client syslog-ng bind-tools mosquitto
# Copie du fichier de conf syslog
#COPY passerellesyslog-ng.conf /etc/syslog-ng/syslog-ng.conf
# Instllation des dépendances pythons
#RUN pip install -r requirements.txt
# Définition de l'entrypoint à lancer
# au démaragge du container
#EXPOSE ..
ENTRYPOINT ["./entrypoint.sh"]
