__version__ = "0.1.0"

from bt_api_base.plugins.protocol import PluginInfo


def plugin_info() -> PluginInfo:
    return PluginInfo(
        name="WazirX",
        version=__version__,
        description="WazirX exchange adapter",
    )
