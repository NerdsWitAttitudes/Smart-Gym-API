from pyramid.security import Allow, Authenticated, Everyone

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.device import get_device, get_device_by_device_address


class DeviceFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        device = get_device(key)

        if device:
            device.set_lineage(self, 'device')
            return device

        raise KeyError

    def get_checkin_device(self, device_address):
        return get_device_by_device_address(device_address)

    def __acl__(self):
        return (
            (Allow, Authenticated, 'device'),
            (Allow, Everyone, 'checkin')
        )
