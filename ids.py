import os
import json
import hashlib
import time
import logging
from pathlib import Path
import sys
import argparse
from colorama import Fore, Style
from tabulate import tabulate

REPERTOIRE_LOGS = '/var/log/ids'
FICHIER_LOG = f'{REPERTOIRE_LOGS}/ids.log'

Path(REPERTOIRE_LOGS).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=FICHIER_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%dT%H:%M:%S'))
logging.getLogger().addHandler(console_handler)

def log_info(message):
    print(Fore.GREEN + "[INFO] " + Style.RESET_ALL + message)
    logging.info(message)

def log_error(message):
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + message)
    logging.error(message)

def log_warning(message):
    print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + message)
    logging.warning(message)

def log_success(message):
    print(Fore.CYAN + "[SUCCESS] " + Style.RESET_ALL + message)
    logging.info(message)

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
        log_success(f"Calcul des hash pour {chemin_fichier} réussi.")
        return {
            'sha512': hash_sha512.hexdigest(),
            'sha256': hash_sha256.hexdigest(),
            'md5': hash_md5.hexdigest()
        }
    except Exception as e:
        log_error(f"Erreur lors du calcul des hash pour {chemin_fichier}: {e}")
        return None

def obtenir_infos_fichier(chemin_fichier):
    try:
        stats = os.stat(chemin_fichier)
        log_success(f"Informations sur {chemin_fichier} obtenues avec succès.")
        return {
            'dernier_changement': time.ctime(stats.st_mtime),
            'date_creation': time.ctime(stats.st_ctime),
            'proprietaire': stats.st_uid,
            'groupe': stats.st_gid,
            'taille': stats.st_size
        }
    except Exception as e:
        log_error(f"Erreur lors de l'obtention des informations pour {chemin_fichier}: {e}")
        return None

def surveiller_fichier(chemin_fichier):
    log_info(f"Surveillance de {chemin_fichier}")
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

def charger_config(chemin_config='config.json'):
    if not os.path.exists(chemin_config):
        log_error(f"Le fichier de configuration {chemin_config} est manquant.")
        return None

    log_info(f"Chargement du fichier de configuration à partir de : {chemin_config}")
    with open(chemin_config, 'r') as f:
        log_success(f"Chargement du fichier de configuration {chemin_config}.")
        return json.load(f)

def creer_db(fichiers, repertoires):
    db = {}
    db['temps_de_creation'] = time.ctime()
    db['fichiers'] = []

    log_info("Création de la base de données. Surveiller les fichiers et répertoires.")
    
    for fichier in fichiers:
        log_info(f"Surveillance du fichier : {fichier}")
        infos_fichier = surveiller_fichier(fichier)
        if infos_fichier:
            db['fichiers'].append({'chemin': fichier, 'infos': infos_fichier})
    
    for repertoire in repertoires:
        log_info(f"Surveillance du répertoire : {repertoire}")
        fichiers_repertoire = surveiller_repertoire(repertoire)
        db['fichiers'].extend(fichiers_repertoire)
    
    log_success("Base de données créée avec succès.")
    
    chemin_db = '/var/ids/db.json'
    os.makedirs(os.path.dirname(chemin_db), exist_ok=True)

    with open(chemin_db, 'w') as f:
        json.dump(db, f, indent=4)
    log_success(f"Base de données sauvegardée dans {chemin_db}.")
    return db

def verifier_fichiers(fichiers, repertoires):
    chemin_db = '/var/ids/db.json'
    
    if not os.path.exists(chemin_db):
        log_error(f"Le fichier {chemin_db} est manquant.")
        return None

    log_info(f"Vérification des fichiers avec le fichier de base de données à : {chemin_db}")
    
    with open(chemin_db, 'r') as f:
        db = json.load(f)

    db_actuel = creer_db(fichiers, repertoires)

    if db['temps_de_creation'] != db_actuel['temps_de_creation']:
        log_info(f"Changements détectés dans l'état des fichiers. Vérification du fichier de base : {chemin_db}")
        return {"state": "divergent", "changements": db_actuel['fichiers']}
    else:
        log_info(f"Aucun changement détecté dans l'état des fichiers. Vérification avec {chemin_db}.")
        return {"state": "ok"}

def principal():
    parser = argparse.ArgumentParser(description='Outil de surveillance de fichier')
    parser.add_argument('--build', action='store_true', help='Construire la base de données')
    parser.add_argument('--check', action='store_true', help='Vérifier les fichiers')

    args = parser.parse_args()

    if args.build:
        log_info("Commande 'build' appelée pour créer la base de données.")
        config = charger_config('config.json')
        
        if not config:
            log_error("Échec du chargement de la configuration.")
            return

        fichiers = config['fichiers']
        repertoires = config['repertoires']
        log_info("Création du fichier db.json.")
        creer_db(fichiers, repertoires)
    
    elif args.check:
        log_info("Commande 'check' appelée pour vérifier l'état des fichiers.")
        config = charger_config('config.json')
    
        
        if not config:
            log_error("Échec du chargement de la configuration.")
            return

        fichiers = config['fichiers']
        repertoires = config['repertoires']
        resultat = verifier_fichiers(fichiers, repertoires)
        
        print(Fore.CYAN + "Résultats de la vérification :\n" + Style.RESET_ALL)
        print(json.dumps(resultat, indent=4))
        log_info(f"Résultats de la vérification : {json.dumps(resultat, indent=4)}")

if __name__ == '__main__':
    principal()
