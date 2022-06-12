import random
import string

from fastapi import Request
from app.utils import verify_password, encrypt_password, get_authorization_from_headers

special_characters = r" !\"  # $%&'()*+,-./:;<=>?@[\]^_`{|}~"
allow_characters = string.ascii_letters + string.digits + special_characters


def test_verify_password():
    plain_password = "".join([random.choice(allow_characters) for _ in range(16)])
    encrypted_password = encrypt_password(plain_password)
    assert verify_password(plain_password=plain_password, encrypted_password=encrypted_password)


def test_get_authorization_from_headers():
    pass
