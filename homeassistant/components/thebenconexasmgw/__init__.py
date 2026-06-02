"""The Theben Conexa Smartmeter gateway integration."""

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type New_NameConfigEntry = ConfigEntry[Data]


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Set up Theben Conexa Smartmeter gateway from a config entry."""

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)
    elD = Data
    elD.conf1 = 3

    entry.runtime_data = elD

    if elD.conf1 == 5:
        raise ConfigEntryNotReady("Device is offline")

    # if entry.conf1 == 6:
    #     raise ex.ConfigEntryError("haaaa")

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)


@dataclass
class Data:
    """Data for the Blueprint integration."""

    conf1: int
