#!/usr/bin/python3
##################################
# Programme qui permet de créer
# un CSR (Certificate Signing
# Request) à envoyer à l'autorite
# de certification
##################################

# Importation des modules #

import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding
from dotenv import load_dotenv
import uuid

# Définition des variables globales #

backend=default_backend()
private_key_file="PrivateRSAKey.pem"


## Définition des fonctions ##

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


''' Création du builder et remplissage des champs du CSR '''

def buildcsr():
	try:

		builder = x509.CertificateSigningRequestBuilder()

		# Remplissage des champs du CSR : le Common_Name
		builder = builder.subject_name(x509.Name([
					       x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
					       x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Marne"),
					       x509.NameAttribute(NameOID.LOCALITY_NAME, u"Reims"),
					       x509.NameAttribute(NameOID.COMMON_NAME, str(uuid.uuid4())),
					       x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Peugeot'),
   					       x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'PSA GROUP')


		]))

		# Ajout de l'extension BasicConstraints
		# avec le flag CA=false qui limite le
		# certificat qui sera fournis à certaines
		# actions, le certificat ne peut pas réaliser
		# des actions d'une CA (Signature de nouveau
		# certificats ...)
		# le flag critical=True signifie que cette
		# extension (BasicConstraints) doit être
		# obligatoirement traité par les systèmes
		# et logiciels
		builder = builder.add_extension(x509.BasicConstraints(ca=False, path_length=None),critical=True)

	except:
		print("[-] Impossible de remplir les champs du CSR")
		raise
	else:
		print("[+] Les champs du CSR ont été remplis")
		return builder

''' Création de la demande de signature '''

def requestcert(private_key,backend,builder):
	try:
		# Utilisation de la méthode sign pour
		# créer la request object CSR en utilisant
		# sa clé privée. Pourquoi ? : les CSR sont
		# autosignés avant d'être envoyé au CA, cela
		# permet de s'assurer que le demandeur du
		# certificat possède bien la clé privée
		# correspondante. Cette méthode extrait donc
		# la clé publique de la clé privée, l'incorpore
		# dans le CSR et signe le tout avec sa clé privée
		request = builder.sign(private_key,hashes.SHA256(),backend)
	except:
		raise
	else:
		print("[+] La demande de signature a été crée")
		return request

''' Enregistrement du CSR sur disque '''

def savecsrtodisk(request):
	csr_file="CSR.pem"

	try:
		os.umask(0)

		with open(os.open(csr_file, os.O_CREAT | os.O_WRONLY, 0o1600), 'wb+') as csr_file_obj:
			csr_file_obj.write(request.public_bytes(Encoding.PEM))

			csr_file_obj.close()

	except:
		raise

	else:
		return "[+] Le CSR a été générée dans le fichier " + csr_file

''' Envoie du CSR qui vient d'être généré au CA 

def sendcsrtoca(csr,caadress,endpoint):
	csrurl="http://ca.projet.local/csr"
	data=
    	response=requests.post(csrurl,data=csr)


	crturl=response.text "http://ca.projet.local/crt"

	return crturl

'''

# Comment on s'assure que seul se véhicule peut aller télécharger le certificat ?
# Etant donné que c'est du HTTP, n'importe qui qui sniff le traffic et récupère
# l'URL du CRT peut aller télécharger le CRT
# Si on fait du HTTPS, d'où vient le certificat qui est utilisé pour faire du HTTPS ?
# Comment le véhicule peut faire confiance à ce certificat ?
# On fera mieux de passer en un envoie manuel par FTP entre le CA et les véhicules 

''' Téléchargement du CRT signé par le CA

def downloadcrt(caadress,crturl):

	crt=requests.get(crturl)

	# Write CRT to file
	with open(crtfile) as crtfileobj:
		crtfileobj.write(crt)
		crtfileobj.close()

'''

######### APPEL DES FONCTIONS ##############
load_dotenv()
private_key=loadprivatekeyfromfile(private_key_file)
builder=buildcsr()
request=requestcert(private_key,backend,builder)
print(savecsrtodisk(request))
