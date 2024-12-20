import os
import stat
import json
from datetime import datetime

def get_file_properties(file_path):
    try:
        file_stats = os.stat(file_path)
        
        def format_date(timestamp):
            return datetime.fromtimestamp(timestamp).strftime('%d %b %Y à %H:%M:%S')

        file_properties = {
            'nom': os.path.basename(file_path),
            'chemin': os.path.abspath(file_path),
            'taille': file_stats.st_size,
            'date_creation': format_date(file_stats.st_ctime),
            'date_modification': format_date(file_stats.st_mtime),
            'date_dernier_acces': format_date(file_stats.st_atime),
            'type': 'dossier' if stat.S_ISDIR(file_stats.st_mode) else 'fichier',
            'permissions': oct(file_stats.st_mode)[-3:],
            'proprietaire': file_stats.st_uid,  
            'groupe': file_stats.st_gid,    
        }

        return file_properties
    except FileNotFoundError:
        print(f"Le fichier '{file_path}' n'a pas été trouvé.")
        return None

def save_properties_to_json(file_paths, output_json):
    all_properties = []

    for file_path in file_paths:
        file_properties = get_file_properties(file_path)
        if file_properties:
            all_properties.append(file_properties)

    if all_properties:
        with open(output_json, 'w', encoding='utf-8') as json_file:
            json.dump(all_properties, json_file, indent=4, ensure_ascii=False)
        print(f"Les propriétés des fichiers ont été sauvegardées dans '{output_json}'.")

file_paths = ['/etc/ssh/sshd_config', '/etc/shadow']
output_json = 'proprietes_fichiers.json'

save_properties_to_json(file_paths, output_json)
