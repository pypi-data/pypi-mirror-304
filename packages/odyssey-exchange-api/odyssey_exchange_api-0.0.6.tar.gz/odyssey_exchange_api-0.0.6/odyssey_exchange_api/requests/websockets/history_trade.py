from odyssey_exchange_api.requests.base import WebsocketRequest


class WebsocketHistoryTradeRequest(WebsocketRequest):
    symbol: str

    def build_request_data(self) -> dict:
        data = {
            "event": "req",
            "params": {
                "channel": f"market_{self.symbol}_trade_ticker",
            }
        }
        return data
