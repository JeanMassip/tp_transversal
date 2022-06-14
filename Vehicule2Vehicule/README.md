# Projet Crypto partie 2

Objectif : Les vehicules doivent pouvoir communiquer entres eux avec verification
des certifications fournis par les pairs

[1] CSRBuild.py et RSAkeys.py permettent a chaque vehicule de crer sa paire
de cle RSA et une demande de signature de certificat (CSR) qui contient
sa cle publique generee et les informations le concernant a mettre dans
le certification qui sera genere par le CA

[2] Vehicule2CA.py permet a un vehicule d'envoyer son CSR au CA avec VehiculetoCA.py
qui va realiser la signature de certificat pour le vehicule et le lui renvoyer

[3] Le vehicule dispose maintenant de son certificat qui est signe par le CA
et qu'il va pouvoir utiliser pour prouver son identite aupres des autres vehicules
avant initiation d'une communication

[4] Vehicule2Vehicule.py permet l'envoie de du certificat signe au vehicule pair, puis,
si le certificat est valide par le vehicule pair, alors, on peut envoyer les messages MQTT 


[x] Il faut coder la verification de certificat des pairs, comment on fait ?, Une partie
est en Go et l'autre partie est en Python.

[x] Il faudrait modifier le code pour que la verification des signatures soite faite par les
2 vehicules qui souihaitent communiquer avant envoie de messages MQTT
