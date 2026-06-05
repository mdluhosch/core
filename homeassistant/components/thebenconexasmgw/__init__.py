"""The Theben Conexa Smartmeter gateway integration."""

from dataclasses import dataclass
import logging

import aiohttp
from .smgw import ConexaSMGW, ConexaSmgwErr, buildCompleteUrl

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)
# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type ThebenConfData = ConfigEntry[Data]


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: ThebenConfData) -> bool:
    """Set up Theben Conexa Smartmeter gateway from a config entry."""

    _LOGGER.debug("Logging is fun")
    try:
        m2mUrl = await buildCompleteUrl(
            async_get_clientsession(hass),
            entry.data[CONF_HOST],
            entry.data[CONF_USERNAME],
            entry.data[CONF_PASSWORD],
        )
        entry.runtime_data = Data(
            ConexaSMGW(
                async_get_clientsession(hass),
                m2mUrl,
                entry.data[CONF_USERNAME],
                entry.data[CONF_PASSWORD],
            )
        )
        _LOGGER.debug(f"SMGW returned valid query URL {m2mUrl}")
    except ConexaSmgwErr as e:
        ConfigEntryError(f"Something went wrong {e}")
    except aiohttp.ClientError as e:
        raise ConfigEntryNotReady(f"Device is not reachable {e}")

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)

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
class Data:
    """Data for the Blueprint integration."""

    api: ConexaSMGW
    # conf1: int
    # host: str
    # usr: str
    # pw: str
