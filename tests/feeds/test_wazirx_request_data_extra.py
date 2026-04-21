from __future__ import annotations

from unittest.mock import MagicMock

from bt_api_wazirx.feeds.live_wazirx.request_base import WazirxRequestData


def test_wazirx_disconnect_closes_http_client() -> None:
    request_data = WazirxRequestData()
    request_data._http_client.close = MagicMock()

    request_data.disconnect()

    request_data._http_client.close.assert_called_once_with()


def test_wazirx_falls_back_to_api_credentials_when_aliases_are_empty() -> None:
    request_data = WazirxRequestData(
        public_key="",
        api_key="public-key",
        secret_key="",
        api_secret="secret-key",
    )

    assert request_data.api_key == "public-key"
    assert request_data.api_secret == "secret-key"
