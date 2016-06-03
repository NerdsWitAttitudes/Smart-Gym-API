import base64
import logging

log = logging.getLogger(__name__)


def extract_client_authorization(request):
    authorization_header = request.authorization
    if not authorization_header.startswith('Basic '):
        raise ValueError
    authorization_header = authorization_header[6:]
    decoded_header = base64.b64decode(request.authorization)
    client_id, client_secret = decoded_header.split(':')
    return {
        "client_id": client_id,
        "client_secret": client_secret
    }
