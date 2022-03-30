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
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding
from dotenv import load_dotenv

### Définission des variables globales ####
CSRfile="CSR.pem"
backend=default_backend()

## Définition des fonctions ####

def loadcsr(CSRfile):

	with open(CSRfile, "rb") as csr_file_object:
                csr = x509.load_pem_x509_csr(csr_file_object.read(),backend=backend)

	return csr

def loadcsrpublickey(csr):

	public_key=csr.public_key()

#	Convert the publickey from the CSR to .PEM format
#	public_key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
#                format=serialization.PublicFormat.SubjectPublicKeyInfo)
#	print(public_key_bytes)

	return public_key

def retrieveinfos(csr):
	# On récupère les valeurs des différents
	# attribus dans l'objet de type NAME
	# qui est retourné par csr.subject
	# ce objet contient beaucoup d'attributs
	# dont les attributs C, ST, L, CN, O et OU

	print(csr.subject.rfc4514_string())

	# METHODE 1 AVEC LA METHODE GET_ATTRIBUTES_FOR_OID #

	COMMON_NAME=csr.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
	COUNTRY_NAME=csr.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value
	LOCALITY_NAME=csr.subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value
	STATE_NAME=csr.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value
	ORGANIZATIONAL_NAME=csr.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
	ORGANIZATIONAL_UNIT_NAME=csr.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value

	# METHODE 2 AVEC ITERATION POUR RECUPERER TOUS LES ATTRIBUTS DE L'OBJET NAME #

	Attributelist=[]

	for attribute in csr.subject:
		Attributelist.append(attribute.value)

	Country=Attributelist[0]
	State=Attributelist[1]
	Locality=Attributelist[2]
	Comon_Name=Attributelist[3]
	Organizational=Attributelist[4]
	Organizational_Unit=Attributelist[5]

	return Country,State,Locality,Comon_Name,Organizational,Organizational_Unit

	# Méthode alternative : utilisation de name.fc4514_string() #

#### Appel des fonctions ####

csr=loadcsr(CSRfile)
public_key=loadcsrpublickey(csr)
print(retrieveinfos(csr))
print(public_key)

