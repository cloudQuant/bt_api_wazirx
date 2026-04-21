from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry


def register_wazirx() -> None:
    from bt_api_wazirx.feeds.live_wazirx.spot import WazirxRequestDataSpot
    from bt_api_wazirx.exchange_data import WazirxExchangeDataSpot
    from bt_api_wazirx.errors import WazirxErrorTranslator
    from bt_api_wazirx.tickers import WazirxRequestTickerData
    from bt_api_base.balance_utils import simple_balance_handler

    ExchangeRegistry.register(
        "WAZIRX___SPOT",
        WazirxExchangeDataSpot(),
        WazirxRequestDataSpot,
        WazirxErrorTranslator(),
        simple_balance_handler,
        ticker_container=WazirxRequestTickerData,
    )


def plugin_info() -> PluginInfo:
    from bt_api_wazirx import __version__

    return PluginInfo(
        name="WazirX",
        version=__version__,
        description="WazirX exchange adapter",
    )
