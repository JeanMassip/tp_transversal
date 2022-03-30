#!/usr/bin/python3.7
####################################
# Programme qui va extraire les
# informations nécéssairs à partir
# du CSR pour pouvoir les inclure
# dans le certificat final qui sera
# fournis par l'AC
####################################

### Importation des modules ###

import os
import string
import datetime
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding
from dotenv import load_dotenv

### Définission des variables globales ####

backend=default_backend()
envfile=".env"
private_key_file="CAPrivateCARSAKey.pem"
one_day = datetime.timedelta(1, 0, 0)

## Définition des fonctions ####

''' Importation de la clé privée RSA depuis un fichier sur disque '''

def loadprivatekeyfromfile(private_key_file):
	# Récupération de la clé AES-256(mot de passe)
	# qui va permettre de déchiffrer la clé privée RSA
	# depuis les variables d'environnement (fichier .env)

	Password=bytes(os.getenv('Password'), 'utf-8')

	# Vérification de l'existence
	# du fichier de la clé privée

	if not os.path.exists(private_key_file):
		return "[-] Le fichier " + private_key_file + " qui contient la clé privée n'existe pas"
	else:
		try:
			with open(private_key_file, "rb") as private_key_file_object:
				private_key = serialization.load_pem_private_key(private_key_file_object.read(),backend=backend,
				password = Password)

		except:
			print("[-] Impossible de charger la clé privée depuis le fichier " + private_key_file)
			raise
		else:

			print("[+] La clé privée a été chargé depuis le fichier " + private_key_file)
			return private_key

''' Importation du CSR depuis un fichier sur disque '''

def loadcsr(CSRfile):

	try:
		with open(CSRfile, "rb") as csr_file_object:
                	csr = x509.load_pem_x509_csr(csr_file_object.read(),backend=backend)
	except:
		raise
	else:
		return csr

''' Extraction de la clé publique depuis le CSR '''

def loadcsrpublickey(csr):

	public_key=csr.public_key()

#	Convert the publickey from the CSR to .PEM format
#	public_key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
#                format=serialization.PublicFormat.SubjectPublicKeyInfo)
#	print(public_key_bytes)

	return public_key

''' Extraction des informations nécessaires pour créer le certificat
à partir du CSR '''

def retrieveinfos(csr):
	# On récupère les valeurs des différents
	# attribus dans l'objet de type NAME
	# qui est retourné par csr.subject
	# ce objet contient beaucoup d'attributs
	# dont les attributs C, ST, L, CN, O et OU

	# UTILISATION DE LA METHODE GET_ATTRIBUTES_FOR_OID #

	COMMON_NAME=csr.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
	COUNTRY_NAME=csr.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value
	LOCALITY_NAME=csr.subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value
	STATE_NAME=csr.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value
	ORGANIZATION_NAME=csr.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
	ORGANIZATIONAL_UNIT_NAME=csr.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value

	return COMMON_NAME,COUNTRY_NAME,LOCALITY_NAME,STATE_NAME,ORGANIZATION_NAME,ORGANIZATIONAL_UNIT_NAME

''' Création du builder et remplissage des champs du certificat '''

def fillcertificate(one_day,COMMON_NAME,COUNTRY_NAME,LOCALITY_NAME,STATE_NAME,ORGANIZATION_NAME,ORGANIZATIONAL_UNIT_NAME):

	# Definition des variables
	# pour remplir les champs
	# issuer du certificat

	ISSUER_NAME="ca.projet.local"
	ISSUER_COUNTRY="FR"
	ISSUER_LOCALITY="Reims"
	ISSUER_STATE="Marne"
	ISSUER_ORGANIZATION="MASTER RT"
	ISSUER_ORGANIZATIONAL_UNIT="URCA"

	# Utilisation de la classe X509.CertificateBuilder
	# Pour créer l'objet qui va nous permettre de
	# manipuler les champs du certificat

	certificatebuilder = x509.CertificateBuilder()

	# Remplissage des champs du certificat qui sera crée

	certificatebuilder = certificatebuilder.issuer_name(x509.Name([
				x509.NameAttribute(NameOID.COMMON_NAME, ISSUER_NAME),
				x509.NameAttribute(NameOID.COUNTRY_NAME, ISSUER_COUNTRY),
				x509.NameAttribute(NameOID.LOCALITY_NAME, ISSUER_LOCALITY),
				x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, ISSUER_STATE),
				x509.NameAttribute(NameOID.ORGANIZATION_NAME, ISSUER_ORGANIZATION),
				x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ISSUER_ORGANIZATIONAL_UNIT)
				]))


	certificatebuilder = certificatebuilder.subject_name(x509.Name([
				x509.NameAttribute(NameOID.COMMON_NAME, COMMON_NAME),
				x509.NameAttribute(NameOID.COUNTRY_NAME, COUNTRY_NAME),
				x509.NameAttribute(NameOID.LOCALITY_NAME, LOCALITY_NAME),
				x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, STATE_NAME),
				x509.NameAttribute(NameOID.ORGANIZATION_NAME, ORGANIZATION_NAME),
				x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ORGANIZATIONAL_UNIT_NAME)
				]))

	# Ajout de la période de validité, du Serial Number et de la clé publique du CA

	certificatebuilder = certificatebuilder.not_valid_before(datetime.datetime.today() - one_day)
	certificatebuilder = certificatebuilder.not_valid_after(datetime.datetime.today() + (one_day * 90))
	certificatebuilder = certificatebuilder.serial_number(x509.random_serial_number())
	certificatebuilder = certificatebuilder.public_key(public_key)

	# Ajout des extensions

	# Cette extension indique que le certificat
	# ne pourra pas être utilisé pour signer d'autres
	# certificats

	certificatebuilder = certificatebuilder.add_extension(
						x509.BasicConstraints(ca=False, path_length=None),critical=True)

	return certificatebuilder

''' Signature du certificat avec la clé privée de l'AC '''

def signcertificate(certificatebuilder,backend,private_key):

	certificate = certificatebuilder.sign(private_key=private_key, algorithm=hashes.SHA256(),backend=backend)

	return certificate

''' Enregistrement du certificat dans un fichier sur disque '''

def savecrttofile(certificate):
	crt_file="CRT.pem"

	try:
		os.umask(0)

		with open(os.open(crt_file, os.O_CREAT | os.O_WRONLY, 0o1600), 'wb+') as crt_file_obj:
			crt_file_obj.write(certificate.public_bytes(Encoding.PEM))

			crt_file_obj.close()

	except:
		raise
	else:
		return "[+] Le certificat a été générée dans le fichier " + crt_file


''' Journalisation des informations concernant le certificat qui a été généré '''

def logcert(certificate):
	# Definition d'un fichier de log
	# qui va contenir l'historique de tous
	# les certificats générés
	Log_file="GeneratedCrt.txt"

	# Journalisation dans le fichier de jurnalisation
	# S on arrive pas à journaliser, on ne va pas plus loin
	try:
		os.umask(0)

		with open(os.open(Log_file, os.O_CREAT | os.O_WRONLY, 0o1600), 'a') as Log_file_obj:
			Log_file_obj.write("Serial_Number="+str(certificate.serial_number)+","
					  +"Before="+str(certificate.not_valid_before)+","
					  +"After="+str(certificate.not_valid_after)+","
					  +"Signature="+str(certificate.signature)+","
					  +certificate.subject.rfc4514_string()+"\n")

			Log_file_obj.close()

	except:
		raise
	else:
		return "[+] Le certificat a été journalisé dans le fichier " + Log_file

''' Vérification de la fourniture du bon nombre d'arguments'''

def checkarguments():
	if int(len(sys.argv))-1 != 1 :
		print("[i] Utilisation du script :")
		print("Fournir l'argument suivant :")
		print("[1] Le nom du fichier CSR du véhicule")
		sys.exit(1)
	else:
		global CSRfile
		CSRfile=sys.argv[1]


### Appel des fonctions ####

checkarguments()
load_dotenv()
private_key=loadprivatekeyfromfile(private_key_file)
csr=loadcsr(CSRfile)
public_key=loadcsrpublickey(csr)
infos=retrieveinfos(csr)

COMMON_NAME=infos[0]
COUNTRY_NAME=infos[1]
LOCALITY_NAME=infos[2]
STATE_NAME=infos[3]
ORGANIZATION_NAME=infos[4]
ORGANIZATIONAL_UNIT_NAME=infos[5]

certificatebuilder=fillcertificate(one_day,COMMON_NAME,COUNTRY_NAME,LOCALITY_NAME,STATE_NAME,ORGANIZATION_NAME,ORGANIZATIONAL_UNIT_NAME)
certificate=signcertificate(certificatebuilder,backend,private_key)
print(savecrttofile(certificate))
logcert(certificate)



