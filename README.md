# bt_api_wazirx

WazirX exchange adapter for bt_api.

## Installation

```bash
pip install bt_api_wazirx
```

## Usage

```python
from bt_api_wazirx import register_wazirx
register_wazirx()

from bt_api_py import BtApi
api = BtApi(exchange_kwargs={"WAZIRX___SPOT": {"api_key": "...", "secret": "..."}})
ticker = api.get_tick("WAZIRX___SPOT", "btcinr")
```
