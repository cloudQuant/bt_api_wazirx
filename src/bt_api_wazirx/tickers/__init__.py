from bt_api_base.containers.tickers.ticker import Ticker


class WazirxRequestTickerData(Ticker):
    @staticmethod
    def from_json(data: dict) -> "WazirxRequestTickerData":
        if data is None:
            return WazirxRequestTickerData()
        return WazirxRequestTickerData(
            last_price=data.get("last", 0.0),
            best_bid_price=data.get("bid", 0.0),
            best_ask_price=data.get("ask", 0.0),
            best_bid_volume=data.get("bidVolume", 0.0),
            best_ask_volume=data.get("askVolume", 0.0),
            volume_24h=data.get("volume", 0.0),
            timestamp=int(data.get("at", 0) / 1000),
        )
