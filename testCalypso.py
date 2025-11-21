import requests
import json
import time
import urllib3

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CalypsHomeAPI:
    def __init__(self, host, login, password):
        """
        Initialise la connexion à la box Calyps'HOME

        Args:
            host: IP ou nom d'hôte (ex: "192.168.1.69")
            login: Email de connexion (ex: "aaa@aaa.aa")
            password: Mot de passe
        """
        self.host = host
        self.base_url = f"http://{host}"
        self.login = login
        self.password = password

        # Cookies d'authentification
        self.cookies = {
            "_server": f"http://{host}",
            "_login": login,
            "_password": password
        }

        self.session = requests.Session()
        self.session.cookies.update(self.cookies)

    def get_objects(self):
        """Récupère la liste de tous les objets (stores, etc.)"""
        url = f"{self.base_url}/m?a=getObjects"

        try:
            response = self.session.post(
                url,
                headers={"Accept": "application/json"},
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des objets: {e}")
            return None

    def send_action(self, device_id, action, args=None):
        """
        Envoie une action à un appareil

        Args:
            device_id: ID complet du device (avec le préfixe atm_io_ezsp::)
            action: Action à exécuter (OPEN, CLOSE, STOP, LEVEL, TILT)
            args: Dict optionnel avec les arguments (ex: {"level": "50"} pour LEVEL)

        Returns:
            True si succès, False sinon
        """
        url = f"{self.base_url}/m?a=command"

        # Construction du body selon le format attendu
        data = {
            "id": device_id,
            "action": action,
            "args": json.dumps(args) if args else ""
        }

        try:
            response = self.session.post(
                url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                verify=False,
                timeout=10
            )

            print(f"Status Code: {response.status_code}")
            print(f"Réponse: {response.text[:200]}")

            if response.status_code == 200:
                print(f"✓ Action {action} envoyée avec succès")
                return True
            else:
                print(f"✗ Erreur: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'envoi de l'action: {e}")
            return False

    def open_shutter(self, device_id):
        """Ouvre un store"""
        return self.send_action(device_id, "OPEN")

    def close_shutter(self, device_id):
        """Ferme un store"""
        return self.send_action(device_id, "CLOSE")

    def stop_shutter(self, device_id):
        """Arrête un store"""
        return self.send_action(device_id, "STOP")

    def set_level(self, device_id, level):
        """Règle le niveau d'ouverture d'un store (0-100)"""
        return self.send_action(device_id, "LEVEL", {"level": str(level)})

    def set_tilt(self, device_id, angle):
        """Règle l'angle d'inclinaison (si BSO)"""
        return self.send_action(device_id, "TILT", {"angle": str(angle)})


# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration
    HOST = "192.168.1.69"
    LOGIN = "aaa@aaa.aa"
    PASSWORD = "aaaa"

    # IDs complets des stores
    STORES = {
        "Ch Romane": "atm_io_ezsp::dev-0/IEEEAddr-20-91-8A-00-00-1F-FA-D6:cluster-closure:endpoint-in_1",
        "Ch Parental": "atm_io_ezsp::dev-0/IEEEAddr-20-91-8A-00-00-1F-FA-D4:cluster-closure:endpoint-in_1",
        "Fenetre salon": "atm_io_ezsp::dev-0/IEEEAddr-20-91-8A-00-00-1F-FA-D2:cluster-closure:endpoint-in_1",
        "Cuisine": "atm_io_ezsp::dev-0/IEEEAddr-20-91-8A-00-00-1F-FA-D0:cluster-closure:endpoint-in_1",
        "Baie vitrée": "atm_io_ezsp::dev-0/IEEEAddr-20-91-8A-00-00-1F-FA-CE:cluster-closure:endpoint-in_1",
        "Ch Marine": "atm_io_ezsp::dev-0/IEEEAddr-20-91-8A-00-00-1F-FA-D8:cluster-closure:endpoint-in_1",
    }

    # Initialiser l'API
    api = CalypsHomeAPI(HOST, LOGIN, PASSWORD)

    # Récupérer tous les objets
    print("=== Récupération des objets ===\n")
    objects = api.get_objects()
    print(objects)
    if objects:
        shutters = [obj for obj in objects.get("objects", []) if obj.get("type") == "Rolling_Shutter"]
        print(f"Stores trouvés: {len(shutters)}")
        for obj in shutters:
            print(f"  - {obj.get('name')}")

    print("\n=== Envoi de commandes ===\n")

    # Exemples de commandes
    #rint("1. Ouverture de Ch Romane")
    #api.open_shutter(STORES["Ch Romane"])
    #time.sleep(1)

    #print("\n2. Réglage Cuisine à 50%")
    #api.set_level(STORES["Cuisine"], 50)
    #time.sleep(1)

    #print("\n3. Fermeture Baie vitrée")
    #api.close_shutter(STORES["Cuisine"])
    #time.sleep(1)

    # Décommentez pour tester d'autres commandes :
    # print("\n4. Arrêt Ch Marine")
    # api.stop_shutter(STORES["Ch Marine"])