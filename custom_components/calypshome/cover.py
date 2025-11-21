"""Support for Calyps'HOME covers."""
import logging
from typing import Any

from homeassistant.components.cover import (
    ATTR_POSITION,
    ATTR_TILT_POSITION,
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Calyps'HOME covers from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]

    # Get all objects from API
    objects = await hass.async_add_executor_job(api.get_objects)

    if objects is None:
        _LOGGER.error("Unable to get objects from Calyps'HOME")
        return

    # Filter shutters
    shutters = [
        obj for obj in objects.get("objects", [])
        if obj.get("type") == "Rolling_Shutter"
    ]

    # Create entities
    entities = []
    for shutter in shutters:
        device_id = shutter.get("id")
        name = shutter.get("name")
        if device_id and name:
            entities.append(CalypsHomeCover(api, device_id, name, shutter))

    if entities:
        async_add_entities(entities, True)
        _LOGGER.info("Added %d Calyps'HOME covers", len(entities))


class CalypsHomeCover(CoverEntity):
    """Representation of a Calyps'HOME cover."""

    def __init__(self, api, device_id, name, device_data):
        """Initialize the cover."""
        self._api = api
        self._device_id = device_id
        self._attr_name = name
        self._attr_unique_id = device_id
        self._device_data = device_data
        self._attr_device_class = CoverDeviceClass.SHUTTER

        # Features supported
        self._attr_supported_features = (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.STOP
            | CoverEntityFeature.SET_POSITION
        )

        # Check if tilt is supported (BSO)
        if device_data.get("hasTilt", False):
            self._attr_supported_features |= CoverEntityFeature.SET_TILT_POSITION

        self._attr_is_closed = None
        self._attr_current_cover_position = None
        self._attr_current_cover_tilt_position = None
        self._attr_is_opening = False
        self._attr_is_closing = False

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._attr_name,
            "manufacturer": "Calyps'HOME",
            "model": "Rolling Shutter",
        }

    @property
    def current_cover_position(self):
        """Return current position of cover (0-100)."""
        return self._attr_current_cover_position

    @property
    def current_cover_tilt_position(self):
        """Return current tilt position of cover (0-100)."""
        return self._attr_current_cover_tilt_position

    @property
    def is_opening(self):
        """Return if the cover is opening."""
        return self._attr_is_opening

    @property
    def is_closing(self):
        """Return if the cover is closing."""
        return self._attr_is_closing

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        if self._attr_current_cover_position is not None:
            return self._attr_current_cover_position == 0
        return self._attr_is_closed

    async def async_update(self):
        """Fetch new state data for this cover."""
        try:
            objects = await self.hass.async_add_executor_job(self._api.get_objects)
            if objects:
                shutters = [
                    obj for obj in objects.get("objects", [])
                    if obj.get("id") == self._device_id
                ]
                if shutters:
                    shutter = shutters[0]
                    self._device_data = shutter

                    # L'API retourne les données dans une liste status
                    # Structure: [{"name": "level", "value": "36"}, {"name": "status", "value": "middle"}, ...]
                    status_list = shutter.get("status", [])
                    level_value = None
                    status_value = None

                    if isinstance(status_list, list):
                        for item in status_list:
                            if isinstance(item, dict):
                                name = item.get("name")
                                value = item.get("value")
                                if name == "level":
                                    level_value = value
                                elif name == "status":
                                    status_value = value

                    # Update position (0 = closed, 100 = open)
                    if level_value is not None:
                        new_position = int(level_value)
                        old_position = self._attr_current_cover_position
                        self._attr_current_cover_position = new_position
                        self._attr_is_closed = new_position == 0

                        # Détection automatique de la fin du mouvement
                        if old_position is None:
                            # Premier chargement : pas de mouvement en cours
                            self._attr_is_opening = False
                            self._attr_is_closing = False
                        elif new_position == old_position:
                            # Position stable : le mouvement est terminé
                            self._attr_is_opening = False
                            self._attr_is_closing = False

        except Exception as err:
            _LOGGER.error("Error updating cover %s: %s", self._attr_name, err)

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        self._attr_is_opening = True
        self._attr_is_closing = False
        self.async_write_ha_state()
        await self.hass.async_add_executor_job(self._api.open_shutter, self._device_id)
        # L'état sera mis à jour lors du prochain refresh

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        self._attr_is_closing = True
        self._attr_is_opening = False
        self.async_write_ha_state()
        await self.hass.async_add_executor_job(self._api.close_shutter, self._device_id)
        # L'état sera mis à jour lors du prochain refresh

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover."""
        await self.hass.async_add_executor_job(self._api.stop_shutter, self._device_id)
        self._attr_is_opening = False
        self._attr_is_closing = False
        self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Move the cover to a specific position."""
        position = kwargs.get(ATTR_POSITION)
        if position is not None:
            current_pos = self._attr_current_cover_position or 0
            # Déterminer si on ouvre ou ferme
            if position > current_pos:
                self._attr_is_opening = True
                self._attr_is_closing = False
            elif position < current_pos:
                self._attr_is_closing = True
                self._attr_is_opening = False
            self.async_write_ha_state()

            await self.hass.async_add_executor_job(
                self._api.set_level, self._device_id, position
            )
            # L'état sera mis à jour lors du prochain refresh

    async def async_set_cover_tilt_position(self, **kwargs: Any) -> None:
        """Move the cover tilt to a specific position."""
        tilt_position = kwargs.get(ATTR_TILT_POSITION)
        if tilt_position is not None:
            await self.hass.async_add_executor_job(
                self._api.set_tilt, self._device_id, tilt_position
            )

