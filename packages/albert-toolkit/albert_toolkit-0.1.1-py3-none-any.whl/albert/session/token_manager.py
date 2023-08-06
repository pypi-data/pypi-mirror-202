import base64
import datetime
import json
import sys
from typing import Any, Dict

import jose.jwt as jwt


class TokenManager(object):
    @property
    def token(self):
        return self.__get_token()

    @property
    def raw_token(self):
        return self.__token

    def __init__(self, token=None, **kwargs):
        self._set_token(token)

    def get_decoded_token(self, token: str) -> Dict[str, Any]:
        """
        We are in a client side library so we obviously cannot verify the token,
        but we can atleast inspect the payload
        """
        return jwt.decode(
            token, key="NONE", options={"verify_aud": False, "verify_signature": False}
        )

    def _get_token_exp(self, token):
        """
        Get the token expiration time. if not present assume forever
        """
        return self.get_decoded_token(token).get("exp", sys.maxsize)

    def _have_unexpired_token(self, token) -> bool:
        if token:
            exp = self._get_token_exp(token)
            if exp >= round(datetime.datetime.utcnow().timestamp()):
                return True
            else:
                return False
        else:
            return False

    def has_valid_token(self) -> bool:
        if self.__token is None:
            return False

        if self._have_unexpired_token(self.__token):
            return True

        return False

    def _set_token(self, token) -> None:
        if token:
            self.__token = token
            self.__token_expiration_sec = self._get_token_exp(token)
        else:
            self.__token = None
            self.__token_expiration_sec = 0

    def _get_token(self) -> str | None:
        if self.__token:
            if not self._have_unexpired_token(self.__token):
                self.refresh_token()
        return self.__token

    def _do_refresh_token(self, old_token, exp=None):
        pass

    def refresh_token(self):
        pass
