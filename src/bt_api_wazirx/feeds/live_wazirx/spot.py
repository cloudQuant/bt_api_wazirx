import time
import urllib.parse
from typing import Any

from bt_api_base.feeds.capability import Capability

from bt_api_wazirx.feeds.live_wazirx.request_base import WazirxRequestData
from bt_api_wazirx.tickers import WazirxRequestTickerData


class WazirxRequestDataSpot(WazirxRequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "WAZIRX___SPOT")

    def _get_tick(
        self, symbol: str, extra_data: Any = None, **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        market = self._format_market(symbol)
        path = f"/api/v2/tickers/{market}"
        return self._request_prepare(
            path, extra_data=extra_data, request_type="get_tick", symbol=symbol,
        )

    @staticmethod
    def _get_tick_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data or WazirxRequestData._is_error(input_data):
            return [], False
        return [WazirxRequestTickerData.from_json(input_data)], True

    def get_tick(self, symbol: str, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.http_request(path, params=params, extra_data=extra_data)

    def async_get_tick(self, symbol: str, extra_data: Any = None, **kwargs: Any) -> None:
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_http_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_depth(
        self, symbol: str, count: int = 20, extra_data: Any = None, **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        market = self._format_market(symbol)
        path = f"/api/v2/depth/{market}?limit={count}"
        return self._request_prepare(
            path, extra_data=extra_data, request_type="get_depth", symbol=symbol,
        )

    @staticmethod
    def _get_depth_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data or WazirxRequestData._is_error(input_data):
            return [], False
        return [input_data], True

    def get_depth(self, symbol: str, count: int = 20, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.http_request(path, params=params, extra_data=extra_data)

    def async_get_depth(
        self, symbol: str, count: int = 20, extra_data: Any = None, **kwargs: Any,
    ) -> None:
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_http_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        market = self._format_market(symbol)
        interval = self._exchange_data.get_kline_periods().get(period, 60)
        since = int(time.time()) - interval * 100
        path = f"/api/v2/klines/{market}?interval={interval}&startTime={since}"
        return self._request_prepare(
            path, extra_data=extra_data, request_type="get_kline", symbol=symbol,
        )

    @staticmethod
    def _get_kline_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data or WazirxRequestData._is_error(input_data):
            return [], False
        klines = input_data if isinstance(input_data, list) else []
        return [klines], True

    def get_kline(
        self, symbol: str, period: str, count: int = 20, extra_data: Any = None, **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.http_request(path, params=params, extra_data=extra_data)

    def async_get_kline(
        self, symbol: str, period: str, count: int = 20, extra_data: Any = None, **kwargs: Any,
    ) -> None:
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_http_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_exchange_info(
        self, extra_data: Any = None, **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "/api/v2/markets"
        return self._request_prepare(
            path, extra_data=extra_data, request_type="get_exchange_info", symbol="",
        )

    @staticmethod
    def _get_exchange_info_normalize_function(
        input_data: Any, extra_data: Any,
    ) -> tuple[list[Any], bool]:
        if not input_data or WazirxRequestData._is_error(input_data):
            return [], False
        markets = input_data if isinstance(input_data, list) else []
        return [markets], True

    def get_exchange_info(self, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        return self.http_request(path, params=params, extra_data=extra_data)

    def _get_balance(
        self, symbol: str | None = None, extra_data: Any = None, **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        path = "/api/v2/account/balance"
        timestamp = str(int(time.time() * 1000))
        query = f"timestamp={timestamp}"
        signature = self._get_signature(query)
        params = {"timestamp": timestamp, "signature": signature}
        return self._request_prepare_with_auth(
            path,
            params=params,
            extra_data=extra_data,
            request_type="get_balance",
            symbol=symbol or "",
        )

    @staticmethod
    def _get_balance_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data or WazirxRequestData._is_error(input_data):
            return [], False
        return [input_data], True

    def get_balance(self, symbol: str | None = None, extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_balance(symbol, extra_data, **kwargs)
        return self.http_request(path, params=params, extra_data=extra_data)

    def _get_account(
        self, extra_data: Any = None, **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        return self._get_balance(extra_data=extra_data, **kwargs)

    @staticmethod
    def _get_account_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data or WazirxRequestData._is_error(input_data):
            return [], False
        return [input_data], True

    def get_account(self, symbol: str = "ALL", extra_data: Any = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_account(extra_data, **kwargs)
        return self.http_request(path, params=params, extra_data=extra_data)

    def _make_order(
        self,
        symbol: str,
        volume: float,
        price: float,
        order_type: str,
        offset: str = "open",
        extra_data: Any = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, str], Any]:
        path = "/api/v2/orders"
        side = "buy" if "buy" in order_type.lower() else "sell"
        market = self._format_market(symbol)
        timestamp = str(int(time.time() * 1000))
        params = {
            "symbol": market,
            "side": side,
            "type": "limit",
            "price": str(price),
            "quantity": str(volume),
            "timestamp": timestamp,
        }
        query = urllib.parse.urlencode(sorted(params.items()))
        params["signature"] = self._get_signature(query)
        return self._request_prepare(
            path, params=params, extra_data=extra_data, request_type="make_order", symbol=symbol,
        )

    @staticmethod
    def _make_order_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data or WazirxRequestData._is_error(input_data):
            return [], False
        return [input_data], True

    def make_order(
        self,
        symbol: str,
        volume: float,
        price: float,
        order_type: str,
        offset: str = "open",
        extra_data: Any = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._make_order(
            symbol, volume, price, order_type, offset, extra_data, **kwargs,
        )
        return self.http_request(path, params=params, extra_data=extra_data)

    def _cancel_order(
        self, symbol: str, order_id: str, extra_data: Any = None, **kwargs: Any,
    ) -> tuple[str, dict[str, str], Any]:
        path = "/api/v2/orders"
        timestamp = str(int(time.time() * 1000))
        params = {
            "id": order_id,
            "timestamp": timestamp,
            "signature": self._get_signature(timestamp),
        }
        return self._request_prepare(
            path,
            params=params,
            extra_data=extra_data,
            request_type="cancel_order",
            symbol=symbol,
            order_id=order_id,
        )

    def cancel_order(
        self, symbol: str, order_id: str, extra_data: Any = None, **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.http_request(path, params=params, extra_data=extra_data)

    def _request_prepare(
        self,
        path: str,
        params: dict | None = None,
        extra_data: Any = None,
        request_type: str = "",
        symbol: str = "",
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        from bt_api_base.functions.utils import update_extra_data

        extra_data = update_extra_data(
            extra_data,
            request_type=request_type, symbol_name=symbol, asset_type=self.asset_type, exchange_name=self.exchange_name, normalize_function=getattr(self, f"_{request_type}_normalize_function"),
        )
        return path, params or {}, extra_data

    def _request_prepare_with_auth(
        self,
        path: str,
        params: dict | None = None,
        extra_data: Any = None,
        request_type: str = "",
        symbol: str = "",
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], Any]:
        from bt_api_base.functions.utils import update_extra_data

        extra_data = update_extra_data(
            extra_data,
            request_type=request_type, symbol_name=symbol, asset_type=self.asset_type, exchange_name=self.exchange_name, normalize_function=getattr(self, f"_{request_type}_normalize_function"),
        )
        return path, params or {}, extra_data
