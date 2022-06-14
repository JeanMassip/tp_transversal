# Projet Crypto partie 2
Les vehicules doivent pouvoir communiquer entres eux avec verification
des certifications fournis par les pairs

[1] CSRBuild.py et RSAkeys.py permettent a chaque vehicule de crer sa paire
de cle RSA et une demande de signature de certificat (CSR) qui contient
sa cle publique generee et les informations le concernant a mettre dans
le certification qui sera genere par le CA

[2] Le CSR est envoye au CA qui realise la signature de certificat pour le
vehicule et le lui renvoie

[3] Le vehicule dispose maintenant de son certificat qui ets signe par le CA
et qu'il va pouvoir utiliser pour prouver son identite aupres des autres vehicules
avant initiation d'une communication

[x] Il faut coder la verification de certificat des pairs
