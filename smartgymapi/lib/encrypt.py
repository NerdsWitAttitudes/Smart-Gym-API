import base64
import binascii
import logging

import bcrypt
from Crypto import Random
from Crypto.Cipher import AES

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
        return False

    return True


def decrypt_AES(message, key, iv):
    decrypt_client = AES.new(key, AES.MODE_CBC, iv)
    test = decrypt_client.decrypt(message)
    return test


def decrypt_secret(secret, key, iv):
    decoded_secret = base64.b64decode(secret.encode('utf-8'))
    return decrypt_AES(decoded_secret, key, iv).decode('utf-8')


def get_secure_token():
    return binascii.b2a_hex(Random.get_random_bytes(32)).decode('utf-8')
