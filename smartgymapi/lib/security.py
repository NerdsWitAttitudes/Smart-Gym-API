import base64
import logging

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import Authenticated, Everyone

from smartgymapi.models.oauth import get_token_by_token


log = logging.getLogger(__name__)


def extract_authorization_header(request):
    authorization_header = request.authorization
    return authorization_header.split(' ')


def extract_client_authorization(request):
    auth_method, encoded_string = extract_authorization_header(request)
    if not auth_method == 'Basic':
        raise ValueError
    decoded_header = base64.b64decode(encoded_string)
    client_id, client_secret = decoded_header.split(':')
    return {
        "client_id": client_id,
        "client_secret": client_secret
    }


class SmartGymAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_access_token(self, request):
        auth_method, token_string = extract_authorization_header(request)
        if auth_method != 'Bearer':
            return
        access_token = get_token_by_token(token_string)

        if access_token.expires_in == 0:
            return

        return access_token

    def effictive_principals(self, request):
        principals = (Everyone,)

        if request.user is not None:
            principals.append(Authenticated)

        access_token = self.authenticated_access_token(request)
        if access_token:
            principals.append('client:{}'.format(
                access_token.client.client_type))
        return principals
