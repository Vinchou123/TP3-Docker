import os
import psutil
import subprocess
from time import sleep

def check_tool_installed(tool):
    return subprocess.run(["which", tool], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    return 

def monitor_disk_usage():
    print("\n--- Utilisation des partitions ---")
    for part in psutil.disk_partitions():
        usage = psutil.disk_usage(part.mountpoint)
        print(f"{part.device}: {usage.percent}% utilisé, Libre: {usage.free / (1024**3):.2f} GB")
    print("-" * 40)
    return

def monitor_memory():
    print("\n--- Utilisation de la mémoire vive (RAM) ---")
    while True:
        mem = psutil.virtual_memory()
        print(f"RAM utilisé: {mem.percent}% (Libre: {mem.available / (1024**3):.2f} GB)", end="\r")
        sleep(1)
        return

def monitor_temperature():
    print("\n--- Température et santé du matériel ---")
    if check_tool_installed("sensors"):
        try:
            sensors_output = subprocess.check_output(["sensors"], text=True)
            print(sensors_output)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de lm_sensors : {e}")
    else:
        print("lm_sensors n'est pas installé. Installez-le avec 'sudo dnf install lm_sensors'.")
    print("-" * 40)
    return

def scan_open_ports():
    print("\n--- Ports ouverts sur la machine ---")
    if check_tool_installed("nmap"):
        try:
            nmap_output = subprocess.check_output(["sudo", "nmap", "-sS", "localhost"], text=True)
            print(nmap_output)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de nmap : {e}")
    else:
        print("nmap n'est pas installé. Installez-le avec 'sudo dnf install nmap'.")
        return


def monitor_connected_users():
    print("\n--- Utilisateurs connectés ---")
    users_output = subprocess.check_output(["w"], text=True)
    print(users_output)
    print("-" * 40)
    return

def show_login_history():
    print("\n--- Historique des connexions ---")
    login_output = subprocess.check_output(["last"], text=True)
    print(login_output)
    print("-" * 40)
    return

def monitor_docker_containers():
    print("\n--- État des containers Docker ---")
    if check_tool_installed("docker"):
        try:
            docker_output = subprocess.check_output(["docker", "ps"], text=True)
            print(docker_output)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de Docker : {e}")
    else:
        print("Docker n'est pas installé ou configuré. Installez-le avec 'sudo dnf install docker'.")
    print("-" * 40)
    return

def monitor_listening_ports():
    print("\n--- Ports en écoute ---")
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN:
            print(f"Port {conn.laddr.port} - Écoute sur {conn.laddr.ip}")
    print("-" * 40)
    return

def monitor_active_connections():
    print("\n--- Connexions réseau actives ---")
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_ESTABLISHED:
            print(f"Connexion établie : {conn.laddr.ip}:{conn.laddr.port} → {conn.raddr.ip}:{conn.raddr.port}")
    print("-" * 40)
    return

def monitor_active_processes():
    print("\n--- Processus actifs ---")
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
        try:
            print(f"PID: {proc.info['pid']}, Nom: {proc.info['name']}, "
                  f"Utilisateur: {proc.info['username']}, Statut: {proc.info['status']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    print("-" * 40)
    return

def main():
    print("Options disponibles :")
    print("1. Afficher l'utilisation des partitions")
    print("2. Afficher la consommation de mémoire vive (RAM)")
    print("3. Afficher la température et la santé du matériel")
    print("4. Scanner les ports ouverts sur la machine")
    print("5. Afficher les utilisateurs connectés")
    print("6. Afficher l'historique des connexions")
    print("7. Surveiller l'état des containers Docker")
    print("8. Surveiller les ports en écoute")
    print("9. Surveiller les connexions réseau actives")
    print("10. Surveiller les processus actifs")
    print("11. Quitter")

    while True:
        choice = input("\nEntrez votre choix (1-11) : ")
        if choice == "1":
            monitor_disk_usage()
        elif choice == "2":
            monitor_memory()
        elif choice == "3":
            monitor_temperature()
        elif choice == "4":
            scan_open_ports()
        elif choice == "5":
            monitor_connected_users()
        elif choice == "6":
            show_login_history()
        elif choice == "7":
            monitor_docker_containers()
        elif choice == "8":
            monitor_listening_ports()
        elif choice == "9":
            monitor_active_connections()
        elif choice == "10":
            monitor_active_processes()
        elif choice == "11":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
