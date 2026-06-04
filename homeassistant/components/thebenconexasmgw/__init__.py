"""The Theben Conexa Smartmeter gateway integration."""

from dataclasses import dataclass
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

_LOGGER = logging.getLogger(__name__)
# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type ThebenConfData = ConfigEntry[Config]


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: ThebenConfData) -> bool:
    """Set up Theben Conexa Smartmeter gateway from a config entry."""

    _LOGGER.debug("Logging is fun")
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)

    entry.runtime_data = Config(
        conf1=4,
        host=entry.data[CONF_HOST],
        usr=entry.data[CONF_USERNAME],
        pw=entry.data[CONF_PASSWORD],
    )

    # if elD.conf1 == 5:
    #     raise ConfigEntryNotReady("Device is offline")

    # raise ConfigEntryNotReady("Device is effline")

    # if entry.conf1 == 6:
    #     raise ex.ConfigEntryError("haaaa")

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ThebenConfData) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)


@dataclass
class Config:
    """Data for the Blueprint integration."""

    conf1: int
    host: str
    usr: str
    pw: str
