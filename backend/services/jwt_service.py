import datetime
import typing

from jose import exceptions, jwe, jwt


def _get_jwt_secret() -> str:
    # import secrets
    # jwt_pwd = secrets.token_urlsafe(32)
    return "QM9QqB9j3YqpboR6Jj2PBljxceejTzKXTXMsOjIx5w4"


def _get_jwe_secret() -> str:
    # import secrets
    # jwe_pwd = secrets.token_hex(8)
    return "05326e2fbb86e47c"


def encode_dict(data: dict, expiration_in_secs: int = None) -> str:
    if not isinstance(data, dict):
        raise ValueError("data must be a dict")

    to_encode = {"data": data}
    if expiration_in_secs:
        to_encode["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=expiration_in_secs
        )

    # generate signed token
    token = jwt.encode(
        to_encode,
        _get_jwt_secret(),
        algorithm="HS256",
    )
    # encrypt the token
    encrypted: str = jwe.encrypt(
        token,
        _get_jwe_secret(),
        algorithm="dir",
        encryption="A128GCM",
    ).decode("utf8")
    return encrypted


def decode_dict(encrypted_data: str) -> typing.Optional[dict]:
    decoded_data = None
    try:
        # get original jwt
        token = jwe.decrypt(
            encrypted_data,
            _get_jwe_secret(),
        )
        # get original data
        data = jwt.decode(
            token,
            _get_jwt_secret(),
            algorithms=["HS256"],
        )
        decoded_data = data["data"]
    except (exceptions.JWEError, exceptions.JWTError):
        pass

    return decoded_data
