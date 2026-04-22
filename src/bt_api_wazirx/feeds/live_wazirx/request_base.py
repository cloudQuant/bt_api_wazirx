from __future__ import annotations

import hashlib
import hmac
from typing import Any

from bt_api_base.feeds.http_client import HttpClient

from bt_api_wazirx.exchange_data import WazirxExchangeDataSpot


class WazirxRequestData:
    _exchange_data = WazirxExchangeDataSpot()

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "WAZIRX___SPOT")
        self.api_key = kwargs.get("public_key") or kwargs.get("api_key") or ""
        self.secret = (
            kwargs.get("private_key") or kwargs.get("api_secret") or kwargs.get("secret_key") or ""
        )
        self.api_secret = self.secret
        self._http_client = HttpClient(self._exchange_data.get_rest_url())

    def _get_signature(self, query_string: str) -> str:
        return hmac.new(
            self.secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256,
        ).hexdigest()

    def _get_headers(self) -> dict:
        return {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _format_market(self, symbol: str) -> str:
        return symbol.lower()

    def disconnect(self) -> None:
        self._http_client.close()

    @staticmethod
    def _is_error(response: dict) -> bool:
        if not isinstance(response, dict):
            return False
        return response.get("error") is not None or response.get("success", 1) == 0
