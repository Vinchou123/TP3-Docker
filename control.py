import os
import stat
import json
from datetime import datetime

def obtenir_proprietes_fichier(chemin_fichier):
    try:
        stats_fichier = os.stat(chemin_fichier)
        proprietes_fichier = {
            'nom': os.path.basename(chemin_fichier),
            'chemin': os.path.abspath(chemin_fichier),
            'taille': stats_fichier.st_size,
            'date_creation': datetime.fromtimestamp(stats_fichier.st_ctime).isoformat(),
            'date_modification': datetime.fromtimestamp(stats_fichier.st_mtime).isoformat(),
            'date_dernier_acces': datetime.fromtimestamp(stats_fichier.st_atime).isoformat(),
            'type': 'dossier' if stat.S_ISDIR(stats_fichier.st_mode) else 'fichier',
            'permissions': oct(stats_fichier.st_mode)[-3:],
            'proprietaire': stats_fichier.st_uid,
            'groupe': stats_fichier.st_gid,
        }
        return proprietes_fichier
    except FileNotFoundError:
        print(f"Le fichier '{chemin_fichier}' n'a pas été trouvé.")
        return None

# Fonction pour vérifier si un fichier a changé
def verifier_changements_fichier(chemin_fichier, proprietes_precedentes):
    proprietes_courantes = obtenir_proprietes_fichier(chemin_fichier)
    
    if not proprietes_courantes:
        return

    # Vérifier les différences
    if proprietes_precedentes and proprietes_courantes != proprietes_precedentes:
        print(f"Changement détecté dans le fichier '{chemin_fichier}'")
        print(f"Anciennes propriétés: {proprietes_precedentes}")
        print(f"Nouvelles propriétés: {proprietes_courantes}")
    else:
        print(f"Aucun changement détecté dans le fichier '{chemin_fichier}'")

    return proprietes_courantes

# Fonction pour charger la configuration depuis le fichier config.json
def charger_configuration(fichier_config='config.json'):
    try:
        with open(fichier_config, 'r', encoding='utf-8') as f:
            configuration = json.load(f)
        return configuration.get('fichiers_a_surveille', [])
    except FileNotFoundError:
        print(f"Le fichier de configuration '{fichier_config}' n'a pas été trouvé.")
        return []

# Charger les fichiers à surveiller depuis le fichier de configuration
fichiers_a_surveiller = charger_configuration()

cache_proprietes_fichiers = {}

# Vérifier chaque fichier
for fichier in fichiers_a_surveiller:
    # Si le fichier a des propriétés précédentes dans le cache, les récupérer
    proprietes_precedentes = cache_proprietes_fichiers.get(fichier)
    
    # Vérifier les changements pour le fichier
    proprietes_courantes = verifier_changements_fichier(fichier, proprietes_precedentes)
    
    # Mettre à jour les propriétés dans le cache
    if proprietes_courantes:
        cache_proprietes_fichiers[fichier] = proprietes_courantes
