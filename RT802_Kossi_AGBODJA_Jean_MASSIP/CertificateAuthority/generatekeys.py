#!/usr/bin/python3
#######################################
# Programme qui va générer une paire
# de clés RSA pour le CA et les
# enregistrer dans dans des fichiers
# sur disque + signature de clé
# publique pour en faire un certificat
# autosigné
#######################################

### Importation des modules ###

import os
import sys
import string
from secrets import choice
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding
from dotenv import load_dotenv
import datetime

### Définission des variables globales ####

backend=default_backend()
envfile=".env"
key_size=2048
public_exponent=65537
one_day = datetime.timedelta(1, 0, 0)

### Définition des fonctions ####

''' Création du fichier des variables
d'environnement avec les permissions 1600 '''

def createenvfile(envfile):
        try:
                os.umask(0)

                file=open(os.open(envfile, os.O_CREAT | os.O_WRONLY, 0o1600), 'w')
                file.close

                return "[+] Le fichier " + envfile + " a été crée"
        except:
                print("[-] Impossible de créer le fichier " + envfile)
                raise

def genprivrsakeypasswd(envfile):
        Alphabet = string.ascii_letters + string.digits + string.punctuation
        Password = ''.join(choice(Alphabet) for i in range(20))

        # Ajout du mot de passe dans le fichier .env
        # des variables d'environnement
        try:
                with open(envfile, 'w') as envfile:
                        envfile.write("Password="+Password+"\n")
        except:
                print("[-] Impossible d'écrire dans le fichier " + envfile)
                sys.exit(1)
        else:
                envfile.close()
                load_dotenv()

''' Génération de la clé privée RSA '''

def genrsaprivatekey(public_exponent, key_size, backend):
        try:
                private_key=rsa.generate_private_key(public_exponent, key_size, backend=backend)
                return private_key
        except :
                raise

''' Dérivation de la clé publique RSA à partir de la clé privée RSA '''

def derivrsapublickey(private_key):
        try:
                public_key=private_key.public_key()
                return public_key
        except:
                raise


''' Convertion de la clé publique (Grand Integer) dans un format .PEM human-readable '''

def convpublickey(public_key):
        try:
                public_key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo)

                return public_key_bytes

        except:
                raise

''' Convertion de la clé privée privée (Grand Integer) dans un format .PEM human-readable '''

def convprivatekey(private_key):

        # Transformer le Password du type str() classique
        # qui se trouve dans le fichier des variables
        # d'environnement .env vers le type bytes() pour
        # pouvoir l'utiliser pour chiffrer la clé privée
        # RSA qui sera générée

        Password=bytes(os.getenv('Password'), 'utf-8')

        try:
                private_key_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(Password))

                return private_key_bytes

        except:
                raise

        ## Enregistrement des clés dans des fichiers sur disque ##

def saveprivatekeytofile(private_in_pem):
        private_key_file="ca-private-key.pem"

        try:

                os.umask(0)
                with open(os.open(private_key_file, os.O_CREAT | os.O_WRONLY, 0o1600), 'wb+') as private_key_file_obj:
                        private_key_file_obj.write(private_in_pem)

                private_key_file_obj.close()

                return "La clé Privé a été générée dans le fichier " + private_key_file

        except:
                raise

def savepublickeytofile(public_in_pem):
        public_key_file="ca-public-key.pem"

        try:
                os.umask(0)

                with open(os.open(public_key_file, os.O_CREAT | os.O_WRONLY, 0o1644), 'wb+') as public_key_file_obj:
                        public_key_file_obj.write(public_in_pem)

                public_key_file_obj.close()

                return "La clé publique a été générée dans le fichier " + public_key_file

        except:
                raise


''' Création du builder et remplissage des champs du certificat '''

def fillcertificate(one_day):
	# Utilisation de la classe X509.CertificateBuilder
	# Pour créer l'objet qui va nous permettre de
	# manipuler les champs du certificat

	certificatebuilder = x509.CertificateBuilder()

	# Remplissage des champs des noms du CA(issuer) et du bénéficiaire du certificat(subject)
	# Ici, on a le même issuer et subject car c'est un certificat autosigné pour le CA

	certificatebuilder = certificatebuilder.subject_name(x509.Name([
				x509.NameAttribute(NameOID.COMMON_NAME, 'ca.projet.local')]))

	certificatebuilder = certificatebuilder.issuer_name(x509.Name([
				x509.NameAttribute(NameOID.COMMON_NAME, 'ca.projet.local')]))


	# Ajout de la période de validité, du Seriual Number et de la clé publique du CA

	certificatebuilder = certificatebuilder.not_valid_before(datetime.datetime.today() - one_day)
	certificatebuilder = certificatebuilder.not_valid_after(datetime.datetime.today() + (one_day * 90))
	certificatebuilder = certificatebuilder.serial_number(x509.random_serial_number())
	certificatebuilder = certificatebuilder.public_key(public_key)

	# Ajout des extensions

	certificatebuilder = certificatebuilder.add_extension(
						x509.SubjectAlternativeName([x509.DNSName('ca.projet.local')]),critical=False)

	# Cette extension indique que le certificat
	# ne pourra pas être utilisé pour signer d'autres
	# certificats

	certificatebuilder = certificatebuilder.add_extension(
						x509.BasicConstraints(ca=True, path_length=None),critical=True)

	return certificatebuilder

''' Signature du certificat avec la clé privée de l'AC '''

def signcertificate(certificatebuilder,backend,private_key):

	certificate = certificatebuilder.sign(private_key=private_key, algorithm=hashes.SHA256(),backend=backend)

	return certificate

''' Enregistrement du certificat dans un fichier sur disque '''

def savecrttofile(certificate):
	crt_file="CAcrt.pem"

	try:
		os.umask(0)

		with open(os.open(crt_file, os.O_CREAT | os.O_WRONLY, 0o1600), 'wb+') as crt_file_obj:
			crt_file_obj.write(certificate.public_bytes(Encoding.PEM))

			crt_file_obj.close()

	except:
		raise
	else:
		return "La clé publique a été générée dans le fichier " + crt_file

#### Appel des fonctions ####

createenvfile(envfile)
genprivrsakeypasswd(envfile)
private_key=genrsaprivatekey(public_exponent, key_size, backend)
public_key=derivrsapublickey(private_key)
public_in_pem=convpublickey(public_key)
private_in_pem=convprivatekey(private_key)
saveprivatekeytofile(private_in_pem)
savepublickeytofile(public_in_pem)
certificatebuilder=fillcertificate(one_day)
certificate=signcertificate(certificatebuilder,backend,private_key)
savecrttofile(certificate)
