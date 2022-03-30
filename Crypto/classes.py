#!/usr/bin/python3.7
#############################################
#
#
#############################################
'''
# Creation dune classe python
class Point:
	"Definition dun point geometrique"

""" Définition des attributs """

# Creation dune instance de la classe Point

p = Point()
print(p)

# Affichage de l'attribut doc de l'objet p
# l'attribut prédéfini doc est associé aux
# chaînes de documentation de la classe

print(p.__doc__)

# Définition de plusieurs instances (objets)
# de la classe point

a=Point()
b=Point()

print(a)
print(b)

p.x=1
p.y=2
print("p : x =", p.x, "y =", p.y)

#La syntaxe pour accéder à un attribut
#est la suivante : on va utiliser la
#variable qui contient la référence à
#l’objet et on va mettre un point .
#puis le nom de l’attribut.

a.x = 1
a.y = 2
b = a
print("a : x =", a.x, "y =", a.y)
print("b : x =", b.x, "y =", b.y)
a.x = 3
a.y = 4
print("a : x =", a.x, "y =", a.y)
print("b : x =", b.x, "y =", b.y)
'''

""" Définition des méthodes """

# En gros, ici, j'attribue des attribus propres
# (x=1) et (y=2) à l'instance a de la classe Point
# Une fois que j'appelle la méthode deplace de la
# classe Point avec 2 arguments : dx et dy,
#	self.x = self.x + dx
#       self.y = self.y + dy
# Permettent de prendre l'attribut x de l'instant
# qui appel la méthode et d'y ajouter le nombre
# dx qui a été fourni en paramètre au moment de
# l'appel de la méthode deplace. La même opération
# est effectuée pour y et dy
# PRECISION : self fait référence à l'instance de l'objet
# qui appelle la méthode

class Point:
	# Création de la méthode constructeur __init__
	# Elle sert à initialiser dès toute sorte de choses
	# dès la création d'une instance de la classe
	def __init__(self, x, y, z):
		self.__x=x
		self.__y=y
		self.__z=z

	# Définition d'une méthode de la classe Point
	def calcul(self, dx, dy, dz):
		self.__x = self.__x + dx - dz
		self.__y = self.__y + dy - dz
		self.__z = self.__z + dz - dz

# Création d'une instance de la classe Point
a = Point(5,10,15)
#a.x = 1
#a.y = 2
#a.z = 3
#print("a : x =", a.x, "y =", a.y, "z =", a.z)
# Appel de la méthode calcul de la classe Point
# En fournissant les arguments dx, dy et dz
#a.calcul(3, 5, 9)
#print("a : x =", a.x, "y =", a.y, "z =", a.z)

