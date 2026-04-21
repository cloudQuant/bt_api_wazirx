from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class WazirxExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "WAZIRX___SPOT"


class WazirxExchangeDataSpot(WazirxExchangeData):
    _REST_URL = "https://api.wazirx.com"
    _WSS_URL = "wss://stream.wazirx.com/stream"

    _KLINE_PERIODS = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "1d": 1440,
    }

    @staticmethod
    def get_rest_url() -> str:
        return WazirxExchangeDataSpot._REST_URL

    @staticmethod
    def get_wss_url() -> str:
        return WazirxExchangeDataSpot._WSS_URL

    @staticmethod
    def get_kline_periods() -> dict:
        return WazirxExchangeDataSpot._KLINE_PERIODS

    @staticmethod
    def get_symbol(symbol: str) -> str:
        return symbol.lower()

    @staticmethod
    def get_rest_path(action: str) -> str:
        paths = {
            "ticker": "/api/v2/tickers/{symbol}",
            "depth": "/api/v2/depth/{symbol}",
            "trades": "/api/v2/trades/{symbol}",
            "kline": "/api/v2/klines/{symbol}",
            "markets": "/api/v2/markets",
            "balance": "/api/v2/account/balance",
        }
        return paths.get(action, "")

    @staticmethod
    def get_wss_path(action: str) -> str:
        return ""

    @staticmethod
    def get_local_symbol(symbol: str) -> str:
        return symbol.upper()

    @staticmethod
    def is_trading_enabled() -> bool:
        return True
