# TP3 Dév : IDS

## IDS - Outil de Surveillance et de Calcul de Hash

### Installation

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

#### Aide

Pour afficher les options disponibles, exécutez la commande suivante :

```
python3 ids.py --help
```

Pour créer le fichier db.json en utilisant un fichier de configuration :
```
python3 ids.py --build
```

Pour vérifier l'état des fichiers par rapport à une base de données existante :
```
python3 ids.py --check
```

