# TP3 Dév : IDS

## IDS - Outil de Surveillance et de Calcul de Hash

### Installation

Cloner mon [repo](https://github.com/Vinchou123/TP3-Docker.git) dans votre environnement de travail :
```
git clone https://github.com/Vinchou123/TP3-Docker.git
```

Déplacer vous dans le dossier :
```
cd TP3-Docker
```


#### Prérequis

Avant d'installer l'outil, assurez-vous d'avoir Python 3 installé ainsi que les outils nécessaires à l'exécution du script.

Pour vérifier faites ce commande :

```
python3 --version
```

Si vous n'avez pas installé Python faites ces commandes : 
```
sudo dnf update
sudo dnf install python3
```

Puis revérifier : 
```
python3 --version
```
Vous devriez maintenant voir une version de Python 3 s'afficher.

Puis installer les paquets colorama et tabulate pour un jolie rendu : 
```
sudo pip3 install colorama
sudo pip3 install tabulate
```

### Usage

Pour créer le fichier db.json en utilisant un fichier de configuration :
```
sudo python3 ids.py --build
```

Pour vérifier l'état des fichiers par rapport à une base de données existante :
```
sudo python3 ids.py --check
```

#### Aide

Pour afficher les options disponibles, exécutez la commande suivante :

```
sudo python3 ids.py --help
```


### Pour lancer l'IDS et lancer à intervalles réguliers le service

copier le fichier ou créer le en faisant :
```
sudo nano /etc/systemd/system/ids.service
```

Ajouter ça en remplaçant votre chemin absolue ou se situe le script ids.py :

commande pour connaitre le chemin absolue du fichier :
```
[vince@VM-TP3-DOCKER TP3-Docker]$ realpath ids.py
```

```
[Unit]
Description=Surveillance de fichiers et répertoires avec IDS
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/vince/TP3-Docker/ids.py --build
WorkingDirectory=/home/vince/TP3-Docker
Restart=on-failure
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ids

[Install]
WantedBy=multi-user.target
```

Enregistrez et quittez en appuyant sur CTRL+X puis Y.

Créez le fichier ids.timer :
```
sudo nano /etc/systemd/system/ids.timer
```

Ajoutez le contenu suivant :

Ps: Si vous ne voulez pas qu'il se relance même après un redémarrage mettre Persistent= false
```
[Unit]
Description=Lancer le service IDS à intervalles réguliers

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Persistent=true 

[Install]
WantedBy=timers.target
```

OnBootSec=5min : permet de lancer le fichier 5 minutes après le démarrage.
OnUnitActiveSec=15min : Relancer toutes les 15 minutes.

####  Activer et démarrer les unités

Rechargez les configurations systemd pour prendre en compte les nouveaux fichiers :
```
sudo systemctl daemon-reload
```

Activez et démarrez le timer pour que le service soit exécuté à intervalles réguliers :
```
sudo systemctl enable ids.timer
sudo systemctl start ids.timer
```

Pour vérifier le statut du timer et du service :
```
sudo systemctl status ids.timer
sudo systemctl status ids.service
```

Pour vérifiez le prochain démarrage du timer :
```
sudo systemctl list-timers --all
```



## Bonus

Le script Python bonus.py permet de surveiller différents aspects du système, tels que l'utilisation du disque, la mémoire vive (RAM), la température matérielle, les ports ouverts, les utilisateurs connectés, l'historique des connexions, les containers Docker, les ports en écoute, les connexions réseau actives et les processus actifs.

### Fonctionnalités

Utilisation des partitions : Affiche l'utilisation actuelle des partitions de disque.  
Consommation de mémoire vive (RAM) : Affiche l'utilisation de la RAM en temps réel.  
Température et santé du matériel : Affiche les informations de température matérielle (nécessite lm_sensors).  
Ports ouverts sur la machine : Scanne et affiche les ports ouverts sur la machine.  
Utilisateurs connectés : Affiche la liste des utilisateurs actuellement connectés.  
Historique des connexions : Affiche l'historique des connexions récentes.  
État des containers Docker : Affiche l'état des containers Docker actifs.  
Ports en écoute : Affiche les ports réseau actuellement en écoute.  
Connexions réseau actives : Affiche les connexions réseau établies.  
Processus actifs : Affiche les processus actuellement en cours d'exécution.  


### Utilisation

Assurez-vous que les outils nécessaires comme psutil, sensors, nmap, docker sont installés sur votre système pour bénéficier de toutes les fonctionnalités du script.

Le script utilise la bibliothèque Python psutil pour récupérer des informations sur le système. Vous pouvez l'installer avec la commande suivante :
```
pip install psutil
```

Pour récupérer les informations de température du matériel, le script utilise l'outil sensors. Si ce n'est pas déjà installé, vous pouvez l'installer avec :
```
sudo dnf install lm_sensors
```

Le script utilise nmap pour scanner les ports ouverts. Si ce n'est pas déjà installé, vous pouvez l'installer avec :
```
sudo dnf install nmap
```

Le script peut surveiller l'état des containers Docker. Pour cela, vous devez avoir Docker installé. Si Docker n'est pas encore installé, vous pouvez le faire avec :
```
sudo dnf install docker
```

Une fois ces outils installés, vous pourrez lancer le script avec :
```
python3 bonus.py
```

Ps: sans oublier d'être dans le répertoire du script.