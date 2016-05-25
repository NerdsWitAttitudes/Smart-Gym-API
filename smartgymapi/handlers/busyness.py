import logging
import requests

from datetime import datetime
from itertools import groupby

from marshmallow import ValidationError

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config, view_defaults

from smartgymapi.models.gym import get_gym

from smartgymapi.lib.factories.busyness import BusynessFactory
from smartgymapi.lib.validation.busyness import BusynessSchema

log = logging.getLogger(__name__)


@view_defaults(containment=BusynessFactory,
               permission='busyness',
               renderer='json')
class RESTBusyness(object):

    def __init__(self, request):
        self.request = request
        self.hour_count = {}
        self.settings = request.registry.settings

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

        gym = get_gym(result['gym_id'])
        r_params = {"q": gym.city,
                    "appid": self.settings['open_weather_api_key'],
                    "units": "metric"}
        r = requests.get(
            self.settings['open_weather_url_forecast'],
            params=r_params).json()

        weather_prediction = create_weather_prediction_list(r)
        log.info(weather_prediction)
        return
        # if r.get('rain'):
        #     weather.raining_outside = True
        # try:
        #     weather.temperature = r['main']['temp']
        # except KeyError:
        #     log.WARN('Temparature not found')

        #     activity.weather = weather

        predicted_busyness = (
            self.request.context.get_predicted_busyness(result['date']))

        self.fill_hour_count(predicted_busyness, False, True)
        return self.hour_count

    def fill_hour_count(self, activities, predict_for_today=False,
                        predict=False):
        """ Set the correct amount of activities for every hour """
        if predict:
            amount_of_days = 0
            # group the activities.
            for (year, items) in groupby(activities, grouper):
                amount_of_days += 1
                for item in items:
                    # For today we only need to predict the hours still to come
                    if (predict_for_today and
                            item.start_date.hour <= datetime.now().hour):
                        continue
                    self.add_item_to_hour_count(item)
            for hour in self.hour_count:
                if (predict_for_today and
                        int(hour) <= datetime.now().hour):
                    continue
                # take the average.
                self.hour_count[hour] = round(
                    self.hour_count[hour] / amount_of_days)
        else:
            for item in activities:
                self.add_item_to_hour_count(item)

    def add_item_to_hour_count(self, item):
        """
        Add activity to the correct hour if exists. If not create and set
        value to 1
        """
        self.hour_count[str(item.start_date.hour)] = \
            self.hour_count.setdefault(
            str(item.start_date.hour), 0) + 1


def grouper(item):
    """
    This function return the year of the activity. This is for grouping the
    activities.
    """
    return item.start_date.year


def create_weather_prediction_list(weather_prediction):
    """
    This function creates a json object with epoch as key and temperature
    as value.
    """
    predictions = {}
    for prediction in weather_prediction['list']:
        predictions[prediction['dt']] = prediction['main']['temp']
        log.info(predictions[prediction['dt']])
    return predictions
