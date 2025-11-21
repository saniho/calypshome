"""Support for Calyps'HOME shutters."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_HOST, CONF_LOGIN, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["cover"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Calyps'HOME from a config entry."""
    # Import ici pour éviter le blocage au chargement du module
    from .api import CalypsHomeAPI

    host = entry.data[CONF_HOST]
    login = entry.data[CONF_LOGIN]
    password = entry.data[CONF_PASSWORD]

    api = CalypsHomeAPI(host, login, password)

    # Test de connexion
    try:
        objects = await hass.async_add_executor_job(api.get_objects)
        if objects is None:
            raise ConfigEntryNotReady("Unable to connect to Calyps'HOME")
    except Exception as err:
        _LOGGER.error("Error connecting to Calyps'HOME: %s", err)
        raise ConfigEntryNotReady from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

