from marshmallow import Schema, fields
from sqlalchemy.orm.exc import NoResultFound

from smartgymapi.lib.exceptions.validation import NotUniqueException
from smartgymapi.models.device import get_device_by_device_address


class DeviceSchema(Schema):
    name = fields.Str(required='Name is required')
    device_address = fields.Str(required='Device address is required')
    device_class = fields.Integer(required='Device class is required')
    client_address = fields.Str(required='Client address is required')

    def validate_device_address(self, data):
        try:
            get_device_by_device_address(data['device_address'])
        except KeyError:
            # This means there's no device address in the data. This will be
            # handled in the user validation.
            return
        except NoResultFound:
            # Meaning no device was found for this device address.
            # We can proceed to create the new device.
            return
        raise NotUniqueException(
            "A device was found that already contains the given device address"
        )
