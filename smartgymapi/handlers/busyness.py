import logging
from datetime import datetime
from itertools import groupby

from marshmallow import ValidationError

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.factories.busyness import BusynessFactory
from smartgymapi.lib.validation.busyness import BusynessSchema
from smartgymapi.lib.validation.user_activity import UserActivitySchema

log = logging.getLogger(__name__)


@view_defaults(containment=BusynessFactory,
               permission='public',
               renderer='json')
class RESTBusyness(object):

    def __init__(self, request):
        self.request = request
        self.hour_count = {}

    @view_config(name='past', context=BusynessFactory,
                 request_method="GET")
    def get_past_busyness(self):
        try:
            result, errors = BusynessSchema(strict=True).load(
                self.request.GET)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        past = self.request.context.get_busyness(date=result['date'])

        self.fill_hour_count(past)
        return self.hour_count

    @view_config(name='today', context=BusynessFactory,
                 request_method="GET")
    def get_todays_busyness(self):
        todays_busyness = self.request.context.get_busyness(
            datetime.now().date())
        todays_predicted_busyness = (
            self.request.context.get_predicted_busyness(
                date=datetime.now().date()))
        self.fill_hour_count(todays_busyness)

        self.fill_hour_count(todays_predicted_busyness, True, True)
        return self.hour_count

    @view_config(name='predict', context=BusynessFactory,
                 request_method="GET")
    def get_predicted_busyness(self):
        try:
            result, errors = BusynessSchema(strict=True).load(
                self.request.GET)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        predicted_busyness = (
            self.request.context.get_predicted_busyness(result['date']))

        self.fill_hour_count(predicted_busyness, False, True)
        return self.hour_count

    def fill_hour_count(self, activities, predict_for_today=False,
                        predict=False):
        if predict:
            amount_of_days = 0
            for (year, items) in groupby(activities, grouper):
                amount_of_days += 1
                for item in items:
                    if (predict_for_today and
                            item.start_date.hour <= datetime.now().hour):
                        continue
                    self.add_item_to_hour_count(item)
            for hour in self.hour_count:
                if (predict_for_today and
                        int(hour) <= datetime.now().hour):
                    continue
                self.hour_count[hour] = round(
                    self.hour_count[hour] / amount_of_days)
        else:
            for item in activities:
                self.add_item_to_hour_count(item)

    def add_item_to_hour_count(self, item):
        self.hour_count[str(item.start_date.hour)] = \
            self.hour_count.setdefault(
            str(item.start_date.hour), 0) + 1


def grouper(item):
    return item.start_date.year
