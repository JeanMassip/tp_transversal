#/bin/bash

# A exécuter avec un argument qui est
# le nom du container

# Définition du nom du container, bridge
# ip du container et passerelle réseau
bridge="brvehicules"
container=$1
ip="192.168.0.2/24"
gateway="192.168.0.1"

# récupération du pid du container
pid=`sudo docker inspect -f '{{.State.Pid}}' $container`

echo $pid
# Lien symbolique pour avoir accès
# aux namespaces docker
cd /var/run
sudo ln -s /var/run/docker/netns netns

# Identification du namespace du container
netns=`sudo ip netns identify $pid`
echo $netns
#echo $netns
# Assignation des noms à donner
# aux veth

hostveth=veth0$container
containerveth=veth1$container

# Création des 2 veth, côté hôté et container
sudo ip link add $hostveth type veth peer name $containerveth
sudo ip link set $containerveth netns $netns

# Ajout du veth côté hôte
# au bridge sur l'hôte
sudo ip link set dev $hostveth master $bridge

# Assignation d'une ip au veth dans le container
sudo ip netns exec $netns ip addr add $ip dev $containerveth

# Activation du veth dans le container
sudo ip netns exec $netns ip link set $containerveth up

# Activation du veth sur l'hôte
sudo ip link set $hostveth up
