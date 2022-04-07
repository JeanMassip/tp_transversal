# Projet RT802

## Fonctionnement de l'authentification des véhicule

## Broker_New

Dans ce dossier est contenu tous le code qui s'occupe de recevoir et trier les messages CAM et DENM.
Dans le fichier main.go, nous avons créer une structure "Broker" qui continent deux Receiver, des thread dédier a la reception des messages MQTT.
Nous avons également lancer un serveur HTTP, qui a un seul endpoint "/auth".
Dans ce endpoint nous attendons un fichier PEM, envoyé en text/plain qui correspond au certificat signé d'un vehicule.
Dans le fichier pki/pki.go nous avons une fonction qui valide la signature du certificat, en se servant du certificat de l'Authorité de Certification.
Si la signature est validé, nous notifions le Broker, qui commencera a prendre en compte les message du véhicule concerné.
Le cas échéant les messages du véhicule seront ignoré.

## Certificate Authority

Dans ce dossier nous avons les scripts python chargé de générer un paire de clé RSA, et de auto-signer la clé publique afin de générer le certificat de notre autorité.
Nous avons ensuite un fichier app.py qui lance un serveur HTTP avec un seul endpoint "/sign_csr" qui attend un fichier PEM en text/plain, détaillant le csr d'un véhicule.
Nous signons ensuite le csr, et renvoyons un certificat signé au véhicule.
