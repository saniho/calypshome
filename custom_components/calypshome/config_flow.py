"""Config flow for Calyps'HOME integration."""
import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import DOMAIN, CONF_HOST, CONF_LOGIN, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_LOGIN): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, str]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Import ici pour éviter le blocage au chargement du module
    from .api import CalypsHomeAPI

    api = CalypsHomeAPI(data[CONF_HOST], data[CONF_LOGIN], data[CONF_PASSWORD])

    # Test connection
    try:
        objects = await hass.async_add_executor_job(api.get_objects)
        if objects is None:
            raise Exception("Unable to connect")
    except Exception as err:
        _LOGGER.error("Error connecting to Calyps'HOME: %s", err)
        raise

    # Return info that you want to store in the config entry.
    return {"title": f"Calyps'HOME ({data[CONF_HOST]})"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Calyps'HOME."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

