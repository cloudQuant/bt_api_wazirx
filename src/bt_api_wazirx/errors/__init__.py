from bt_api_base.error import ErrorTranslator, UnifiedErrorCode


class WazirxErrorTranslator(ErrorTranslator):
    _ERROR_MAP = {
        "invalid_api_key": UnifiedErrorCode(1001, "invalid_api_key", "Invalid API key"),
        "invalid_signature": UnifiedErrorCode(1002, "invalid_signature", "Invalid signature"),
        "insufficient_balance": UnifiedErrorCode(
            1003,
            "insufficient_balance",
            "Insufficient balance",
        ),
        "invalid_order": UnifiedErrorCode(1004, "invalid_order", "Invalid order"),
        "order_not_found": UnifiedErrorCode(1005, "order_not_found", "Order not found"),
        "rate_limit": UnifiedErrorCode(1006, "rate_limit", "Rate limit exceeded"),
        "market_closed": UnifiedErrorCode(1007, "market_closed", "Market closed"),
        "withdraw_disabled": UnifiedErrorCode(1008, "withdraw_disabled", "Withdrawal disabled"),
    }

    def translate(self, error_data: dict) -> UnifiedErrorCode:
        if not error_data:
            return UnifiedErrorCode(0, "unknown", "Unknown error")
        error_msg = error_data.get("error") or error_data.get("message") or "Unknown error"
        for key, code in self._ERROR_MAP.items():
            if key in str(error_msg).lower():
                return code
        return UnifiedErrorCode(0, "unknown", error_msg)

    @staticmethod
    def is_error(response: dict) -> bool:
        if not isinstance(response, dict):
            return False
        return response.get("error") is not None or response.get("success", 1) == 0
