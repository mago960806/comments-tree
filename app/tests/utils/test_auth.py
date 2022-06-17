import random
import string
from datetime import datetime, timedelta

from jose import jwt

from app.config import settings
from app.utils import verify_password, encrypt_password, create_access_token

special_characters = r" !\"  # $%&'()*+,-./:;<=>?@[\]^_`{|}~"
allow_characters = string.ascii_letters + string.digits + special_characters


def test_verify_password():
    plain_password = "".join([random.choice(allow_characters) for _ in range(16)])
    encrypted_password = encrypt_password(plain_password)
    assert verify_password(plain_password=plain_password, encrypted_password=encrypted_password)


def test_create_access_token():
    now = datetime.now()
    subject = "test"
    expires_delta = timedelta(minutes=10)
    access_token = create_access_token(subject=subject, expires_delta=expires_delta)
    payload = jwt.decode(access_token, settings.SECRET_KEY)
    assert payload == {"exp": int((now + timedelta(minutes=10)).timestamp()), "sub": subject}
