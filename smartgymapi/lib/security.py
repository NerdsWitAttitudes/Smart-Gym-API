import base64
import logging

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import Authenticated, Everyone

from smartgymapi.models.oauth import get_token_by_token


log = logging.getLogger(__name__)


def extract_client_authorization(request):
    auth_method, encoded_string = request.authorization
    if not auth_method == 'Basic':
        raise ValueError
    decoded_header = base64.b64decode(encoded_string).decode('utf-8')
    client_id, client_secret = decoded_header.split(':')
    return {
        "client_id": client_id,
        "client_secret": client_secret
    }


class SmartGymAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_access_token(self, request):
        try:
            auth_method, token_string = request.authorization
        except (ValueError, TypeError):
            # Meaning the token is invalid or no token was found
            return

        if auth_method != 'Bearer':
            return
        access_token = get_token_by_token(token_string)

        if access_token.expires_in == 0:
            return

        return access_token

    def effective_principals(self, request):
        principals = [Everyone]

        if request.user is not None:
            principals.append(Authenticated)

        access_token = self.authenticated_access_token(request)
        if access_token:
            principals.append('client:{}'.format(
                access_token.client.client_type))
        return principals
