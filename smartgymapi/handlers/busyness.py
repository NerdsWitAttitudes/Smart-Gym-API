import logging
from datetime import date, datetime, time, timedelta

from itertools import groupby

from pytz import timezone

import requests

from marshmallow import ValidationError

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config, view_defaults

from smartgymapi.models.gym import get_gym

from smartgymapi.lib.factories.busyness import BusynessFactory
from smartgymapi.lib.validation.busyness import BusynessSchema

log = logging.getLogger(__name__)


@view_defaults(containment=BusynessFactory,
               permission='busyness',
               renderer='json',
               context=BusynessFactory,
               request_method="GET")
class RESTBusyness(object):

    def __init__(self, request):
        self.request = request
        self.hour_count = {}
        self.settings = request.registry.settings

    @view_config(name='past')
    def get_past_busyness(self):
        try:
            result, errors = BusynessSchema(strict=True).load(
                self.request.GET)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        gym = self.get_gym(result)

        if not gym:
            raise HTTPBadRequest(json={'message': 'no gym found'})

        past = self.request.context.get_busyness(gym=gym, date=result['date'])

        self.fill_hour_count(past)
        return replace_keys_with_datetimes(result['date'],
                                           self.hour_count)

    @view_config(name='today')
    def get_todays_busyness(self):
        try:
            result, errors = BusynessSchema(strict=True).load(
                self.request.GET)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        gym = self.get_gym(result)

        if not gym:
            raise HTTPBadRequest(json={'message': 'no gym found'})

        todays_busyness = self.request.context.get_busyness(
            date=datetime.now().date(), gym=gym)

        r = get_weather(self.settings, gym, predict=True)

        todays_predicted_busyness = (
            self.request.context.get_predicted_busyness(
                date=datetime.now().date(), gym=gym))

        todays_predicted_busyness = filter_on_weather(
            todays_predicted_busyness, create_weather_prediction_list(r),
            date.today())

        self.fill_hour_count(todays_busyness)

        self.fill_hour_count(todays_predicted_busyness,
                             True, True)
        return replace_keys_with_datetimes(datetime.now().date(),
                                           self.hour_count)

    @view_config(name='predict')
    def get_predicted_busyness(self):
        try:
            result, errors = BusynessSchema(strict=True).load(
                self.request.GET)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        gym = self.get_gym(result)

        if not gym:
            raise HTTPBadRequest(json={'message': 'no gym found'})

        r = get_weather(self.settings, gym, predict=True)

        predicted_busyness = (
            self.request.context.get_predicted_busyness(
                date=result['date']
            ))

        predicted_busyness = filter_on_weather(
            predicted_busyness, create_weather_prediction_list(r),
            result['date'])

        self.fill_hour_count(predicted_busyness, False, True)
        return replace_keys_with_datetimes(result['date'],
                                           self.hour_count)

    def get_gym(self, result):
        try:
            return get_gym(result['gym_id'])
        except KeyError:
            return self.request.user.gym

    def fill_hour_count(self, activities, predict_for_today=False,
                        predict=False):
        """ Set the correct amount of activities for every hour """
        if predict:
            amount_of_days = 0
            # group the activities.
            for (day, items) in groupby(activities, grouper):
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
                    # take the average not including today in the amount of
                    # days.
                    self.hour_count[hour] = round(
                        self.hour_count[hour] / amount_of_days - 1)
                else:
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
        self.hour_count[
            str(item.start_date.hour)] = self.hour_count.setdefault(
            str(item.start_date.hour), 0) + 1


def get_weather(settings, gym, predict=False):
    r_params = {"q": gym.city,
                "appid": settings['open_weather_api_key'],
                "units": "metric"}

    if predict:
        return requests.get(
            settings['open_weather_url_forecast'],
            params=r_params).json()
    else:
        return requests.get(
            settings['open_weather_url_current'],
            params=r_params).json()


def grouper(item):
    """
    This function return the day of the activity. This is for grouping the
    activities.
    """
    return item.start_date.day


def create_weather_prediction_list(weather_prediction):
    """
    This function creates a json object with datetime as key and temperature
    as value for every hour in the day.
    """
    predictions = {}
    for prediction in weather_prediction['list']:
        rain = False
        if prediction.get('rain'):
            rain = True
        temp = prediction['main']['temp']
        weather = {"temperature": temp, "rain": rain}
        predictions[datetime.fromtimestamp(prediction['dt'])] = weather
    return predictions


def filter_on_weather(activities, weather, date):
    """
    This function removes all activities where the weather does not match the
    weather of the day we predict
    """
    # create an object with hours as keys and datetimes as value for every
    # 3 hours of the day
    date_list = {x: datetime.combine(
        date, time()) + timedelta(hours=x) for x in range(0, 24)}
    new_activities = []
    # calculate offset
    offset = timezone('CET').utcoffset(datetime.now()).total_seconds() / 3600
    for activity in activities:
        # get the correct key because the weather is saved in steps of 3 hours.
        # we have to add our gmt offset to that number.
        correct_key = activity.start_date.hour + \
            (3 - (activity.start_date.hour % 3)) + offset
        if activity.weather.rain == weather[
            date_list[correct_key]]['rain'] and (
                activity.weather.temperature >= weather[
                    date_list[correct_key]][
                    'temperature'] - 5 or
            activity.weather.temperature <= weather[
                    date_list[correct_key]][
                    'temperature'] + 5):
            new_activities.append(activity)
    return new_activities


def replace_keys_with_datetimes(date, hour_count):
    """
    This function replaces the keys in hour_count with real datetimes
    """
    new_hour_count = {}
    for key in hour_count.keys():
        new_key = datetime.combine(date, time(int(key), 00))
        if new_key != key:
            new_hour_count[new_key.isoformat()] = hour_count[key]
    return new_hour_count
