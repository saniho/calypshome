import requests
import json
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    HOST = "192.168.1.69"
    LOGIN = "aaa@aaa.aa"
    PASSWORD = "aaaa"

    cookies = {
        "_server": f"http://{HOST}",
        "_login": LOGIN,
        "_password": PASSWORD
    }

    session = requests.Session()
    session.cookies.update(cookies)

    url = f"http://{HOST}/m?a=getObjects"
    response = session.post(url, headers={"Accept": "application/json"}, verify=False, timeout=10)
    print(f"Status code: {response.status_code}")

    data = response.json()

    shutters = [obj for obj in data.get("objects", []) if obj.get("type") == "Rolling_Shutter"]

    print(f"Nombre de volets: {len(shutters)}\n")

    # Afficher le premier volet en détail
    if shutters:
        print("=== STRUCTURE COMPLETE DU PREMIER VOLET ===")
        print(json.dumps(shutters[0], indent=2))
        print("\n" + "="*50 + "\n")

        # Afficher tous les volets avec leur info
        for shutter in shutters:
            print(f"=== {shutter.get('name')} ===")
            print(f"ID: {shutter.get('id')}")
            print(f"Type: {shutter.get('type')}")

            # Vérifier si level/status sont directs ou dans une sous-structure
            if 'level' in shutter:
                print(f"Level (direct): {shutter.get('level')}")
            if 'status' in shutter:
                status = shutter.get('status')
                print(f"Status (type): {type(status)}")
                if isinstance(status, list):
                    print(f"Status (list): {len(status)} items")
                    for item in status:
                        if isinstance(item, dict):
                            name = item.get('name', '')
                            value = item.get('value', '')
                            if name in ['status', 'level', '__user_name']:
                                print(f"  - {name}: {value}")
                else:
                    print(f"Status (value): {status}")

            print()

except Exception as e:
    print(f"ERREUR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()

