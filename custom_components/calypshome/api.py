"""API client for Calyps'HOME."""
import logging
import requests
import json
import urllib3

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_LOGGER = logging.getLogger(__name__)


class CalypsHomeAPI:
    """API client for Calyps'HOME."""

    def __init__(self, host, login, password):
        """Initialize the Calyps'HOME API client.

        Args:
            host: IP or hostname (ex: "192.168.1.69")
            login: Email login (ex: "aaa@aaa.aa")
            password: Password
        """
        self.host = host
        self.base_url = f"http://{host}"
        self.login = login
        self.password = password

        # Authentication cookies
        self.cookies = {
            "_server": f"http://{host}",
            "_login": login,
            "_password": password
        }

        self.session = requests.Session()
        self.session.cookies.update(self.cookies)

    def get_objects(self):
        """Get list of all objects (shutters, etc.)."""
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
            _LOGGER.error("Error getting objects: %s", e)
            return None

    def send_action(self, device_id, action, args=None):
        """Send an action to a device.

        Args:
            device_id: Full device ID (with atm_io_ezsp:: prefix)
            action: Action to execute (OPEN, CLOSE, STOP, LEVEL, TILT)
            args: Optional dict with arguments (ex: {"level": "50"} for LEVEL)

        Returns:
            True if success, False otherwise
        """
        url = f"{self.base_url}/m?a=command"

        # Build body according to expected format
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

            if response.status_code == 200:
                _LOGGER.debug("Action %s sent successfully to %s", action, device_id)
                return True
            else:
                _LOGGER.error("Error sending action: %s", response.status_code)
                return False

        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error sending action: %s", e)
            return False

    def open_shutter(self, device_id):
        """Open a shutter."""
        return self.send_action(device_id, "OPEN")

    def close_shutter(self, device_id):
        """Close a shutter."""
        return self.send_action(device_id, "CLOSE")

    def stop_shutter(self, device_id):
        """Stop a shutter."""
        return self.send_action(device_id, "STOP")

    def set_level(self, device_id, level):
        """Set shutter opening level (0-100)."""
        return self.send_action(device_id, "LEVEL", {"level": str(level)})

    def set_tilt(self, device_id, angle):
        """Set tilt angle (for BSO shutters)."""
        return self.send_action(device_id, "TILT", {"angle": str(angle)})

