"""Support for control of ElkM1 lighting (X10, UPB, etc)."""
from homeassistant.components.light import ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light

from . import DOMAIN as ELK_DOMAIN, ElkEntity, create_elk_entities


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Elk light platform."""
    if discovery_info is None:
        return
    elk_datas = hass.data[ELK_DOMAIN]
    entities = []
    for elk_data in elk_datas.values():
        elk = elk_data["elk"]
        create_elk_entities(elk_data, elk.lights, "plc", ElkLight, entities)
    async_add_entities(entities, True)


class ElkLight(ElkEntity, Light):
    """Representation of an Elk lighting device."""

    def __init__(self, element, elk, elk_data):
        """Initialize the Elk light."""
        super().__init__(element, elk, elk_data)
        self._brightness = self._element.status

    @property
    def brightness(self):
        """Get the brightness."""
        return self._brightness

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def is_on(self) -> bool:
        """Get the current brightness."""
        return self._brightness != 0

    def _element_changed(self, element, changeset):
        status = self._element.status if self._element.status != 1 else 100
        self._brightness = round(status * 2.55)

    async def async_turn_on(self, **kwargs):
        """Turn on the light."""
        self._element.level(round(kwargs.get(ATTR_BRIGHTNESS, 255) / 2.55))

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        self._element.level(0)
