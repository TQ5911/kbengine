from Lib.jwt.api_jwk import PyJWK, PyJWKSet
from .api_jws import (
    PyJWS,
    get_algorithm_by_name,
    get_unverified_header,
    register_algorithm,
    unregister_algorithm,
)
from Lib.jwt.api_jwt import PyJWT, decode, encode
from Lib.jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
    PyJWKClientError,
    PyJWKError,
    PyJWKSetError,
    PyJWTError,
)
from Lib.jwt.jwks_client import PyJWKClient

__version__ = "2.6.0"

__title__ = "PyJWT"
__description__ = "JSON Web Token implementation in Python"
__url__ = "https://pyjwt.readthedocs.io"
__uri__ = __url__
__doc__ = f"{__description__} <{__uri__}>"

__author__ = "José Padilla"
__email__ = "hello@jpadilla.com"

__license__ = "MIT"
__copyright__ = "Copyright 2015-2022 José Padilla"


__all__ = [
    "PyJWS",
    "PyJWT",
    "PyJWKClient",
    "PyJWK",
    "PyJWKSet",
    "decode",
    "encode",
    "get_unverified_header",
    "register_algorithm",
    "unregister_algorithm",
    "get_algorithm_by_name",
    # Exceptions
    "DecodeError",
    "ExpiredSignatureError",
    "ImmatureSignatureError",
    "InvalidAlgorithmError",
    "InvalidAudienceError",
    "InvalidIssuedAtError",
    "InvalidIssuerError",
    "InvalidKeyError",
    "InvalidSignatureError",
    "InvalidTokenError",
    "MissingRequiredClaimError",
    "PyJWKClientError",
    "PyJWKError",
    "PyJWKSetError",
    "PyJWTError",
]
