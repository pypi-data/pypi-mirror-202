import typing as t

from orderbookzpy.direction import Direction
from orderbookzpy.tif import TimeInForce

if t.TYPE_CHECKING:
    from orderbookzpy.client import OrderbookzClient


class MarketClient:
    def __init__(
        self, orderbookz_client: "OrderbookzClient", venue_name: str, symbol: str
    ) -> None:
        self.orderbookz = orderbookz_client
        self.venue = venue_name
        self.symbol = symbol

    def get_orderbook(self) -> t.Dict:
        return self.orderbookz.request(path=f"/api/{self.venue}/{self.symbol}/book")

    def submit_order(
        self,
        price: int,
        quantity: int,
        direction: Direction,
        time_in_force: TimeInForce = TimeInForce.GTC,
    ) -> t.Dict:
        return self.orderbookz.request(
            path=f"/api/{self.venue}/{self.symbol}/submit",
            method="POST",
            data={
                "price": price,
                "quantity": quantity,
                "direction": Direction(direction).value,
                "tif": TimeInForce(time_in_force).value,
            },
        )

    def cancel_order(self, order_id: str) -> t.Dict:
        return self.orderbookz.request(
            path=f"/api/{self.venue}/{self.symbol}/cancel",
            method="PATCH",
            data={"id": order_id},
        )
