import datetime

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest

from smartgymapi.lib.validation.device import CheckinSchema


class Device(object):
    def checkin(request):
        schema = CheckinSchema(strict=True)
        try:
            result, errors = schema.load(request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        device = request.context
        device.last_used = datetime.datetime.now()

        # launch activity code
