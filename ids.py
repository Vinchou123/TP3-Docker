import os
import json
import hashlib
import time
import logging
from pathlib import Path
import sys


REPERTOIRE_LOGS = '/var/log/ids'
FICHIER_LOG = f'{REPERTOIRE_LOGS}/ids.log'
Path(REPERTOIRE_LOGS).mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=FICHIER_LOG, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def calculer_hash(chemin_fichier):
    try:
        hash_sha512 = hashlib.sha512()
        hash_sha256 = hashlib.sha256()
        hash_md5 = hashlib.md5()
        with open(chemin_fichier, 'rb') as f:
            for bloc_octets in iter(lambda: f.read(4096), b""):
                hash_sha512.update(bloc_octets)
                hash_sha256.update(bloc_octets)
                hash_md5.update(bloc_octets)
        return {
            'sha512': hash_sha512.hexdigest(),
            'sha256': hash_sha256.hexdigest(),
            'md5': hash_md5.hexdigest()
        }
    except Exception as e:
        logging.error(f"Erreur lors du calcul des hash pour {chemin_fichier}: {e}")
        return None

def obtenir_infos_fichier(chemin_fichier):
    try:
        stats = os.stat(chemin_fichier)
        return {
            'dernier_changement': time.ctime(stats.st_mtime),
            'date_creation': time.ctime(stats.st_ctime),
            'proprietaire': stats.st_uid,
            'groupe': stats.st_gid,
            'taille': stats.st_size
        }
    except Exception as e:
        logging.error(f"Erreur lors de l'obtention des informations pour {chemin_fichier}: {e}")
        return None

def surveiller_fichier(chemin_fichier):
    logging.info(f"Surveillance de {chemin_fichier}")
    infos_fichier = obtenir_infos_fichier(chemin_fichier)
    if infos_fichier:
        hashes = calculer_hash(chemin_fichier)
        if hashes:
            infos_fichier.update(hashes)
            return infos_fichier
    return None

def surveiller_repertoire(chemin_repertoire):
    rapports_fichiers = []
    for racine, dossiers, fichiers in os.walk(chemin_repertoire):
        for fichier in fichiers:
            chemin_fichier = os.path.join(racine, fichier)
            rapport_fichier = surveiller_fichier(chemin_fichier)
            if rapport_fichier:
                rapports_fichiers.append(rapport_fichier)
    return rapports_fichiers

def charger_config(chemin_config='/home/vince/TP3-Docker/config.json'):
    if not os.path.exists(chemin_config):
        logging.error(f"Le fichier de configuration {chemin_config} est manquant.")
        return None

    with open(chemin_config, 'r') as f:
        return json.load(f)

def creer_db(fichiers, repertoires):
    db = {}
    db['temps_de_creation'] = time.ctime()
    db['fichiers'] = []
    
    for fichier in fichiers:
        infos_fichier = surveiller_fichier(fichier)
        if infos_fichier:
            db['fichiers'].append({'chemin': fichier, 'infos': infos_fichier})
    
    for repertoire in repertoires:
        fichiers_repertoire = surveiller_repertoire(repertoire)
        db['fichiers'].extend(fichiers_repertoire)
    
    return db

def verifier_fichiers(fichiers, repertoires, chemin_config='/home/vince/TP3-Docker/config.json'):
    chemin_db = os.path.join(os.path.dirname(chemin_config), 'db.json')
    
    if not os.path.exists(chemin_db):
        logging.error(f"Le fichier {chemin_db} est manquant.")
        return None

    with open(chemin_db, 'r') as f:
        db = json.load(f)

    db_actuel = creer_db(fichiers, repertoires)

    if db['temps_de_creation'] != db_actuel['temps_de_creation']:
        logging.info("L'état des fichiers a changé.")
        return {"etat": "divergent", "changements": db_actuel['fichiers']}
    else:
        logging.info("Aucun changement détecté.")
        return {"etat": "ok"}


def principal():
    config = charger_config()

    if not config:
        logging.error("Échec du chargement de la configuration.")
        return

    fichiers = config['fichiers']
    repertoires = config['repertoires']

    if '--build' in sys.argv:
        logging.info("Création du fichier db.json.")
        db = creer_db(fichiers, repertoires)

        chemin_config = '/home/vince/TP3-Docker/config.json'
        chemin_db = os.path.join(os.path.dirname(chemin_config), 'db.json')

        os.makedirs(os.path.dirname(chemin_db), exist_ok=True)
        
        with open(chemin_db, 'w') as f:
            json.dump(db, f, indent=4)
    elif '--check' in sys.argv:
        resultat = verifier_fichiers(fichiers, repertoires)
        print(json.dumps(resultat, indent=4))


if __name__ == '__main__':
    principal()
