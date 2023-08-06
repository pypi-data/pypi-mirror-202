import typing as t
import requests

from orderbookzpy.marketclient import MarketClient
from orderbookzpy.direction import Direction
from orderbookzpy.tif import TimeInForce


class OrderbookzClient:
    def __init__(
        self, api_key: str, game_name: str, host: str = "https://orderbookz.com"
    ) -> None:
        self.host = host
        self.headers = {"X-api-key": api_key}
        self.game_name = game_name
        self.session: t.Optional[requests.Session] = None

    def start_session(self) -> requests.Session:
        self.close_session()
        self.session = requests.Session()
        self.session.headers = self.headers
        return self.session

    def close_session(self) -> None:
        if self.session is not None:
            self.session.close()
            self.session = None

    def __enter__(self) -> "OrderbookzClient":
        if self.session is not None:
            return self
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def request(
        self,
        path: str,
        method: str = "GET",
        query: t.Optional[t.Dict] = None,
        data: t.Optional[t.Dict] = None,
    ) -> t.Dict:
        with self:
            return self.session.request(
                method=method, url=f"{self.host}{path}", json=data, params=query
            ).json()

    def market(self, venue_name: str, symbol: str) -> MarketClient:
        return MarketClient(
            orderbookz_client=self, venue_name=venue_name, symbol=symbol
        )

    def get_orderbook(self, venue_name: str, symbol: str) -> t.Dict:
        return self.request(path=f"/api/{venue_name}/{symbol}/book")

    def submit_order(
        self,
        venue_name: str,
        symbol: str,
        price: int,
        quantity: int,
        direction: str,
        time_in_force: str = "GTC",
    ) -> t.Dict:
        return self.request(
            path=f"/api/{venue_name}/{symbol}/submit",
            method="POST",
            data={
                "price": price,
                "quantity": quantity,
                "direction": Direction(direction).value,
                "tif": TimeInForce(time_in_force).value,
            },
        )

    def cancel_order(self, venue_name: str, symbol: str, order_id: str) -> t.Dict:
        return self.request(
            path=f"/api/{venue_name}/{symbol}/cancel",
            method="PATCH",
            data={"id": order_id},
        )
