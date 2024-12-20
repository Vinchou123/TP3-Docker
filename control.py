import os
import stat
import json
from datetime import datetime

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

def save_properties_to_json(file_path, output_json):
    file_properties = get_file_properties(file_path)
    
    if file_properties:
        with open(output_json, 'w', encoding='utf-8') as json_file:
            json.dump(file_properties, json_file, indent=4, ensure_ascii=False)
        print(f"Les propriétés du fichier ont été sauvegardées dans '{output_json}'.")

file_path = '/etc/ssh/sshd_config' 
output_json = 'proprietes_shadow.json'

save_properties_to_json(file_path, output_json)
