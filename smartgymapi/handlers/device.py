import datetime
import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.validation.device import DeviceSchema
from smartgymapi.model import commit, persist, rollback, delete
from smartgymapi.models.device import Device

log = logging.getLogger(__name__)


@view_defaults(containment='smartgymapi.lib.factories.device.DeviceFactory',
               permission='device',
               renderer='json')
class DeviceHandler(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=Device, request_method='POST', permission='checkin',
                 name='checkin')
    def checkin(self):
        schema = DeviceSchema(strict=True)
        try:
            result, errors = schema.load(self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        device = self.request.context
        device.last_used = datetime.datetime.now()

        # launch activity code

    @view_config(context='smartgymapi.lib.factories.device.DeviceFactory',
                 request_method='GET')
    def list(self):
        return DeviceSchema(
            many=True,
            only=('name', 'device_address', 'device_class')
        ).dump(self.request.context.get_devices())

    @view_config(context='smartgymapi.lib.factories.device.DeviceFactory',
                 request_method='POST')
    def post(self):
        schema = DeviceSchema(strict=True, only=('name', 'device_address',
                                                 'device_Class'))
        try:
            result, errors = schema.load(self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        device = Device()
        device.set_fields(result)

        try:
            persist(device)
        except:
            log.critical("Something went wrong saving the device",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

    @view_config(context=Device, request_method='DELETE')
    def delete(self):
        try:
            delete(self.request.context)
        except:
            log.critical("Something went wrong deleting the device",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
