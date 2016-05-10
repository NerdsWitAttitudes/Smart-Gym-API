import base64
import bcrypt
import logging
from Crypto.Cipher import AES

log = logging.getLogger(__name__)


def hash_password(password):
    salt = bcrypt.gensalt()
    return (bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8'),
            salt.decode('utf-8'))


def decrypt_AES(message, key, iv):
    decrypt_client = AES.new(key, AES.MODE_CBC, iv)
    test = decrypt_client.decrypt(message)
    return test


def decrypt_secret(secret, key, iv):
    decoded_secret = base64.b64decode(secret.encode('utf-8'))
    return decrypt_AES(decoded_secret, key, iv).decode('utf-8')
