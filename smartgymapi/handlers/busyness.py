import logging
import requests

from datetime import date, datetime, time, timedelta
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

        todays_predicted_busyness = (
            self.request.context.get_predicted_busyness(
                date=datetime.now().date()))

        todays_predicted_busyness = filter_on_weather(
            todays_predicted_busyness, create_weather_prediction_list(r))

        self.fill_hour_count(todays_busyness)

        self.fill_hour_count(todays_predicted_busyness,
                             True, True)
        return replace_keys_with_datetimes(datetime.now().date(),
                                           self.hour_count)

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

        predicted_busyness = (
            self.request.context.get_predicted_busyness(
                date=result['date']
            ))

        predicted_busyness = filter_on_weather(
            predicted_busyness, create_weather_prediction_list(r))

        self.fill_hour_count(predicted_busyness, False, True)
        return self.hour_count

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
        self.hour_count[
            str(item.start_date.hour)] = self.hour_count.setdefault(
            str(item.start_date.hour), 0) + 1


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
    first_iteration = True
    # todo fix van 2 uur vooruit.
    for prediction in weather_prediction['list']:
        rain = False
        if prediction.get('rain'):
            rain = True
        temp = prediction['main']['temp']
        weather = {"temperature": temp, "rain": rain}
        predictions[datetime.fromtimestamp(prediction['dt'])] = weather
        if first_iteration:
            predictions[
                datetime.fromtimestamp(
                    prediction['dt']) + timedelta(hours=-1)] = weather
            predictions[
                datetime.fromtimestamp(
                    prediction['dt']) + timedelta(hours=-2)] = weather
            first_iteration = False
        predictions[
            datetime.fromtimestamp(
                prediction['dt']) + timedelta(hours=1)] = weather
        predictions[
            datetime.fromtimestamp(
                prediction['dt']) + timedelta(hours=2)] = weather
    return predictions


def filter_on_weather(activities, weather):
    """
    This function removes all activities where the weather does not match the
    weather of the day we predict
    """
    # create an object with hours as keys and datetimes as value for every
    # hour of the day
    date_list = {x: datetime.combine(
        date.today(), time()) + timedelta(hours=x) for x in range(0, 24)}

    new_activities = []
    for activity in activities:
        if activity.weather.rain == weather[
            date_list[activity.start_date.hour]]['rain'] and (
                activity.weather.temperature >= weather[
                    date_list[activity.start_date.hour]][
                    'temperature'] - 5 or
            activity.weather.temperature <= weather[
                    date_list[activity.start_date.hour]][
                    'temperature'] + 5):
            new_activities.append(activity)

    return new_activities


def replace_keys_with_datetimes(date, hour_count):
    new_hour_count = {}
    for key in hour_count.keys():
        new_key = datetime.combine(date, time(int(key), 00))
        if new_key != key:
            new_hour_count[new_key.isoformat()] = hour_count[key]
    log.info(new_hour_count)
    return new_hour_count
