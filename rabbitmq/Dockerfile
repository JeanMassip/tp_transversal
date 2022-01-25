#FROM alpine:latest
#FROM rabbitmq:alpine
#FROM rabbitmq:latest
FROM rabbitmq:3.9-alpine
# Copie des fichiers d'applicatif et entrypoint
#COPY main.py requirements.txt handler.py receiver.py 
COPY entrypoint.sh ./
# Mise à jour du dépôt et des paquets
RUN apk update && apk upgrade
#RUN apt update && apt upgrade -y
# Installation des paquets essentiels
RUN apk add openssh-server openssh-client syslog-ng bind-tools
#RUN apt install openssh-server openssh-client syslog-ng iproute2 -y
#bind-tools
# Copie du fichier de conf syslog
#COPY passerellesyslog-ng.conf /etc/syslog-ng/syslog-ng.conf
# Instllation des dépendances pythons
#RUN pip install -r requirements.txt
# Définition de l'entrypoint à lancer
# au démaragge du container
#EXPOSE ..
#EXPOSE ..
ENTRYPOINT ["./entrypoint.sh"]
