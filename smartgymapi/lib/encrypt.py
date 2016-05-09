import base64
import bcrypt
import logging
from Crypto.Cipher import AES
from pyramid.exceptions import HTTPBadRequest

log = logging.getLogger(__name__)


def hash_password(password):
    salt = bcrypt.gensalt()
    return (bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8'),
            salt.decode('utf-8'))


def check_password(password, hashed_password, salt):
    """Checks the password against the hashed bytes of the user"""

    new_hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                        salt.encode('utf-8'))

    if not new_hashed_password == hashed_password.encode('utf-8'):
        raise HTTPBadRequest(
            json={"message": "Username or password incorrect"})


def decrypt_AES(message, key, iv):
    decrypt_client = AES.new(key, AES.MODE_CBC, iv)
    test = decrypt_client.decrypt(message)
    return test


def decrypt_secret(secret, key, iv):
    log.info(secret)
    decoded_secret = base64.b64decode(secret.encode('utf-8'))
    return decrypt_AES(decoded_secret, key, iv).decode('utf-8')
