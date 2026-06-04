"""Platform for sensor integration."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import Config, ThebenConfData
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ThebenConfData,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([ExampleSensor(entry.runtime_data)])


class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 15

    def __init__(self, data: Config):
        """Initialize metadata."""
        self._attr_unique_id = f"RoflDieKaty{data.conf1}"
        data.conf1 += 1
        self._attr_device_info = DeviceInfo(
            name="isNichWahr", identifiers={(DOMAIN, data.host)}
        )

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value += 1
        if self._attr_native_value > 50:
            self._attr_native_value = 15
