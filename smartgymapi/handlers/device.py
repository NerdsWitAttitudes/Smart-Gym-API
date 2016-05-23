import datetime
import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.exceptions.validation import NotUniqueException
from smartgymapi.lib.validation.device import DeviceSchema
from smartgymapi.models import commit, persist, rollback, delete
from smartgymapi.models.device import Device
from smartgymapi.models.gym import get_gym_by_MAC_address
from smartgymapi.models.user_activity import UserActivity

log = logging.getLogger(__name__)


@view_defaults(containment='smartgymapi.lib.factories.device.DeviceFactory',
               context='smartgymapi.lib.factories.device.DeviceFactory',
               permission='device',
               renderer='json')
class DeviceHandler(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='POST', permission='checkin', name='checkin')
    def checkin(self):
        schema = DeviceSchema(strict=True)
        try:
            result, errors = schema.load(self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        device = self.request.context.get_checkin_device(
            result['device_address'])
        device.last_used = datetime.datetime.now()

        activity = device.user.active_activity
        self.request.response.json_body = {
            "user": "{} {}".format(
                device.user.first_name, device.user.last_name)
        }

        # if there's an active activy for the user the user needs to be checked
        # out
        if activity:
            activity.end_date = datetime.datetime.now()
            self.request.response.json_body["status"] = "checked out"

        else:
            activity = UserActivity()
            activity.start_date = datetime.datetime.now()
            activity.user = device.user
            activity.gym = get_gym_by_MAC_address(result['client_address'])
            self.request.response.json_body["status"] = "checked in"

        try:
            persist(device)
            persist(activity)
        except:
            log.critical("Something went wrong checking in",
                         exc_info=True)
            rollback()
        finally:
            commit()

    @view_config(request_method='GET')
    def list(self):
        return DeviceSchema(
            many=True,
            only=('name', 'device_address', 'device_class')
        ).dump(self.request.context.get_devices())

    @view_config(request_method='POST', permission='public')
    def post(self):
        schema = DeviceSchema(strict=True, only=('name', 'device_address',
                                                 'device_class'))
        try:
            result, errors = schema.load(self.request.json_body)
        except (ValidationError, NotUniqueException) as e:
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
