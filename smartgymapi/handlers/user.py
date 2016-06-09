import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import (HTTPBadRequest, HTTPInternalServerError,
                                    HTTPNoContent, HTTPCreated)
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.encrypt import hash_password
from smartgymapi.lib.exceptions.validation import NotUniqueException
from smartgymapi.lib.factories.user import BuddyFactory, UserFactory
from smartgymapi.lib.redis import RedisSession
from smartgymapi.lib.similarity import get_ordered_list_similarity
from smartgymapi.lib.validation.auth import SignupSchema
from smartgymapi.lib.validation.user import (BuddySchema, UserSchema,
                                             GETUserSchema)
from smartgymapi.models import commit, persist, rollback, delete
from smartgymapi.models.user import User, get_user, list_users
from smartgymapi.models.user_activity import get_favorite_weekdays_for_user

log = logging.getLogger(__name__)


@view_defaults(containment=UserFactory,
               permission='user',
               renderer='json')
class RESTUser(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=UserFactory, request_method="GET")
    def list(self):
        try:
            result, errors = GETUserSchema().load(
                self.request.GET)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        return UserSchema(many=True).dump(
            self.request.context.get_users(**result)).data

    @view_config(context=User, request_method="GET")
    def get(self):
        return UserSchema().dump(self.request.context).data

    @view_config(context=UserFactory, request_method="GET", name="me")
    def get_current_user(self):
        return UserSchema().dump(self.request.user).data

    @view_config(context=UserFactory, permission='signup',
                 request_method="POST")
    def post(self):
        try:
            result, errors = SignupSchema(strict=True).load(
                self.request.json_body)
        except (ValidationError, NotUniqueException) as e:
            raise HTTPBadRequest(json={'message': str(e)})

        user = User()
        user.password_hash, user.password_salt = hash_password(
            result['password'])

        self.save(user)

        raise HTTPCreated

    @view_config(context=User, request_method="PUT")
    def put(self):
        self.save(self.request.context)

    def save(self, user):
        try:
            result, errors = UserSchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        user.set_fields(result)

        try:
            persist(user)
        except:
            log.critical("Something went wrong saving the user",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

    @view_config(context=User, request_method="DELETE")
    def delete(self):
        try:
            delete(self.request.context)
        except:
            log.critical("Something went wrong deleting the user",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

        raise HTTPNoContent

    @view_config(context=User, request_method="GET", name="buddies")
    def list_buddies(self):
        return UserSchema(many=True).dump(self.request.context.friends)


@view_defaults(containment=BuddyFactory,
               permission='buddy',
               renderer='json')
class RESTBuddy(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=BuddyFactory, request_method="GET")
    def list(self):
        return UserSchema(many=True).dump(self.request.user.buddies).data

    @view_config(context=BuddyFactory, request_method="GET",
                 name="recommended")
    def list_recommended(self):
        """Returns 5 users we recommend for the user to befriend

        To improve performace the output is cached and will be retrieved
        from cache if possible.
        """

        current_user = self.request.user
        recommended_buddies = RedisSession().session.get(
            "{}_recommended_buddies".format(current_user.id))

        if recommended_buddies:
            # return recommended_buddies
            pass

        recommended_buddies = {}
        favorite_weekdays = get_favorite_weekdays_for_user(current_user).all()
        users = list_users()
        for user in users:
            if user is current_user or user in user.buddies:
                # Don't recommend the user to befriend him or herself
                # or users that are already buddies.
                continue

            favorite_weekday_similarity = get_ordered_list_similarity(
                favorite_weekdays,
                get_favorite_weekdays_for_user(user).all())

            if len(recommended_buddies) < 5:
                # List not full, we can continue early
                recommended_buddies[user] = favorite_weekday_similarity
                continue

            # Get the lowest similarity currently in the list
            lowest_user = min(recommended_buddies,
                              key=recommended_buddies.get)
            lowest_similarity = recommended_buddies[lowest_user]

            # Replace the lowest user if this user fits the current user
            # better.
            if favorite_weekday_similarity > lowest_similarity:
                recommended_buddies.pop(lowest_user, None)
                recommended_buddies[user] = favorite_weekday_similarity

        recommended_buddies_data = UserSchema(many=True).dump(
            recommended_buddies).data
        RedisSession().session.set(
            "{}_recommended_buddies".format(current_user.id),
            recommended_buddies_data)

        return recommended_buddies_data

    @view_config(context=BuddyFactory, request_method="PUT")
    def put(self):
        schema = BuddySchema(strict=True)
        try:
            result, errors = schema.load(self.request.json_body)
            schema.validate_user_id(result, self.request.user.id)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        new_buddy = get_user(result['user_id'])

        # add the new buddy to the user's existing buddies
        self.request.user.buddies.append(new_buddy)

        try:
            persist(self.request.user)
            response_body = UserSchema().dump(new_buddy).data
        except:
            log.critical("Something went wrong adding a new buddy",
                         exc_info=True)
            rollback()
        finally:
            commit()

        return response_body

    @view_config(context=User, request_method="DELETE")
    def delete(self):
        self.request.user.buddies.remove(self.request.context)
        try:
            persist(self.request.user)
        except:
            log.critical("Something went wrong deleting a buddy",
                         exc_info=True)
            rollback()
        finally:
            commit()

        raise HTTPNoContent
