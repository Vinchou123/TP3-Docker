import os
import stat
import json
from datetime import datetime

# Fonction pour obtenir les propriétés d'un fichier
def get_file_properties(file_path):
    try:
        file_stats = os.stat(file_path)
        file_properties = {
            'nom': os.path.basename(file_path),
            'chemin': os.path.abspath(file_path),
            'taille': file_stats.st_size,
            'date_creation': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            'date_modification': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            'date_dernier_acces': datetime.fromtimestamp(file_stats.st_atime).isoformat(),
            'type': 'dossier' if stat.S_ISDIR(file_stats.st_mode) else 'fichier',
            'permissions': oct(file_stats.st_mode)[-3:],
            'proprietaire': file_stats.st_uid,
            'groupe': file_stats.st_gid,
        }
        return file_properties
    except FileNotFoundError:
        print(f"Le fichier '{file_path}' n'a pas été trouvé.")
        return None

# Fonction pour vérifier si un fichier a changé
def check_file_changes(file_path, previous_properties):
    current_properties = get_file_properties(file_path)
    
    if not current_properties:
        return

    # Vérifier les différences
    if previous_properties and current_properties != previous_properties:
        print(f"Changement détecté dans le fichier '{file_path}'")
        print(f"Anciennes propriétés: {previous_properties}")
        print(f"Nouvelles propriétés: {current_properties}")
    else:
        print(f"Aucun changement détecté dans le fichier '{file_path}'")

    return current_properties

# Fonction pour charger la configuration à partir du fichier config.json
def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('fichiers_a_surveille', [])
    except FileNotFoundError:
        print(f"Le fichier de configuration '{config_file}' n'a pas été trouvé.")
        return []

# Charger les fichiers à surveiller depuis le fichier de configuration
files_to_check = load_config()

# Dictionnaire pour stocker les propriétés des fichiers surveillés
file_properties_cache = {}

# Vérifier chaque fichier
for file in files_to_check:
    # Si le fichier a des propriétés précédentes dans le cache, les récupérer
    previous_properties = file_properties_cache.get(file)
    
    # Vérifier les changements pour le fichier
    current_properties = check_file_changes(file, previous_properties)
    
    # Mettre à jour les propriétés dans le cache
    if current_properties:
        file_properties_cache[file] = current_properties
