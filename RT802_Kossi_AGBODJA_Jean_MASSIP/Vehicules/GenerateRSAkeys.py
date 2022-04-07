#!/usr/bin/python3
########################################
# Pogramme de génération de la paire de
# clé Privée/Publique RSA d'une taille
# de 2048bits et enregistrement sur disque
# Auteur : Massip/Agbodja
# Date de modification : 20/03/2022
# Version : 1.0
########################################

# Importation des modules #

import os
import string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from secrets import choice
from dotenv import load_dotenv

# Définition des variables globales #

public_exponent=65537
key_size=2048
backend=default_backend()
envfile=".env"

## Définition des fonctions ##

''' Création du fichier des variables
d'environnement avec les permissions 1600 '''

def createenvfile(envfile):
	try:
		os.umask(0)

		file=open(os.open(envfile, os.O_CREAT | os.O_WRONLY, 0o1600), 'w')
		file.close

		print("[+] Le fichier " + envfile + " a été crée")
	except:
		print("[-] Impossible de créer le fichier " + envfile)
		raise

	## Génération de la clé privée et publique ##

''' Génération d'un mot de passe de 20 caractères pour chiffer la clé privée RSA '''
''' Le chiffrement de la clé privée se fera avec l'algorithme AES-256-CBC '''

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

	## Convertion des clés dans un format human-readable .PEM ##

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
#		encryption_algorithm=serialization.NoEncryption())
		encryption_algorithm=serialization.BestAvailableEncryption(Password))

		return private_key_bytes

	except:
		raise

	## Enregistrement des clés dans des fichiers sur disque ##

def saveprivatekeytofile(private_in_pem):
	private_key_file="PrivateRSAKey.pem"

	try:

		os.umask(0)

		with open(os.open(private_key_file, os.O_CREAT | os.O_WRONLY, 0o1600), 'wb+') as private_key_file_obj:
			private_key_file_obj.write(private_in_pem)

		private_key_file_obj.close()

		return "La clé Privé a été générée dans le fichier " + private_key_file

	except:
		raise

def savepublickeytofile(public_in_pem):
	public_key_file="PublicRSAKey.pem"

	try:
		os.umask(0)

		with open(os.open(public_key_file, os.O_CREAT | os.O_WRONLY, 0o1644), 'wb+') as public_key_file_obj:
			public_key_file_obj.write(public_in_pem)

		public_key_file_obj.close()

		return "La clé publique a été générée dans le fichier " + public_key_file

	except:
		raise

'''
def privbytestokey(private_in_pem, backend):
	#Fonction de déchiffrement de la clé privée RSA #
	#Retourne une erreure si le mot de passe fournis
	#n'est pas le bon mot de passe qui a servi à 
	#chiffrer la clé

	nencryptprivate="nencryptprivate"
	Password=bytes(os.getenv('Password'), 'utf-8')

	try:
		nencryptprivate_key = serialization.load_pem_private_key(private_in_pem, backend=backend,
		password=Password)
		print(nencryptprivate_key)
	except:
		raise
'''

## Appel des fonctions ##

createenvfile(envfile)
genprivrsakeypasswd(envfile)
private_key=genrsaprivatekey(public_exponent, key_size, backend)
public_key=derivrsapublickey(private_key)
public_in_pem=convpublickey(public_key)
private_in_pem=convprivatekey(private_key)

print(saveprivatekeytofile(private_in_pem))
print(savepublickeytofile(public_in_pem))
