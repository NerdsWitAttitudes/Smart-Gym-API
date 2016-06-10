from pyramid.security import Allow, Authenticated
from sqlalchemy.orm.exc import NoResultFound

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.device import (get_device, get_devices,
                                       get_device_by_device_address)


class DeviceFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if key == 'checkin':
            raise KeyError

        try:
            device = get_device(self.request.user, key)
        except NoResultFound:
            raise KeyError

        device.set_lineage(self, 'device')
        return device

    def get_checkin_device(self, device_address):
        return get_device_by_device_address(device_address)

    def get_devices(self):
        return get_devices(self.request.user)

    def __acl__(self):
        return (
            (Allow, Authenticated, 'device'),
            (Allow, 'client:confidential', 'checkin')
        )
