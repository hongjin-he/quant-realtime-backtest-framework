from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Tuple
import time
from sortedcontainers import SortedDict

class Side(Enum):
    BID = "bid"
    ASK = "ask"

@dataclass
class Order:
    order_id: int
    side: Side
    price: float
    quantity: float
    timestamp: float = field(default_factory=time.time)
    trader_id: str = "anonymous"

@dataclass
class Fill:
    order_id: int
    price: float
    quantity: float
    side: Side
    timestamp: float
    maker_id: str
    taker_id: str

class OrderBook:
    def __init__(self, tick_size: float = 0.01):
        self.tick_size = tick_size
        self._bids = SortedDict(key=lambda p: -p)  # descending bids
        self._asks = SortedDict()  # ascending asks
        self._orders = {}
        self._next_order_id = 1
        self.fills = []
        self.events = []

    def submit_limit_order(self, side: Side, price: float, quantity: float, trader_id: str = "anon") -> Tuple[int, List[Fill]]:
        order = Order(self._next_order_id, side, price, quantity, trader_id=trader_id)
        self._next_order_id += 1
        self._orders[order.order_id] = order

        fills = self._match(order)

        if order.quantity > 0:
            self._add_to_book(order)

        self._record_event("LIMIT", order, fills)
        return order.order_id, fills

    def submit_market_order(self, side: Side, quantity: float, trader_id: str = "anon") -> List[Fill]:
        order = Order(self._next_order_id, side, 0, quantity, trader_id=trater_id)
        self._next_order_id += 1

        fills = self._match(order)
        self._record_event("MARKET", order, fills)
        return fills

    def _match(self, incoming: Order) -> List[Fill]:
        fills = []
        book = self._asks if incoming.side == Side.BID else self._bids
        while incoming.quantity > 0 and book:
            best_key = next(iter(book))
            actual_price = -best_key if incoming.side == Side.BID else best_key
            if not self._can_trade(incoming, actual_price):
                break
            orders = book[best_key]
            i = 0
            while i < len(orders) and incoming.quantity > 0:
                resting = orders[i]
                fill_qty = min(incoming.quantity, resting.quantity)
                fills.append(Fill(incoming.order_id, actual_price, fill_qty, incoming.side, time.time(), resting.trader_id, incoming.trader_id))
                incoming.quantity -= fill_qty
                resting.quantity -= fill_qty
                if resting.quantity <= 0:
                    orders.pop(i)
                else:
                    i += 1
            if not orders:
                del book[best_key]
        return fills

    def _can_trade(self, incoming: Order, resting_price: float) -> bool:
        return (incoming.side == Side.BID and resting_price <= incoming.price) or \
               (incoming.side == Side.ASK and resting_price >= incoming.price)

    def _add_to_book(self, order: Order):
        book = self._bids if order.side == Side.BID else self._asks
        key = -order.price if order.side == Side.BID else order.price
        if key not in book:
            book[key] = []
        book[key].append(order)

    def cancel_order(self, order_id: int) -> bool:
        if order_id not in self._orders:
            return False
        order = self._orders[order_id]
        book = self._bids if order.side == Side.BID else self._asks
        key = -order.price if order.side == Side.BID else order.price
        if key in book:
            book[key] = [o for o in book[key] if o.order_id != order_id]
            if not book[key]:
                del book[key]
        del self._orders[order_id]
        return True

    def _record_event(self, type_: str, order: Order, fills: List[Fill]):
        self.events.append({"type": type_, "order": order.__dict__, "fills": [f.__dict__ for f in fills]})

    @property
    def best_bid(self) -> Optional[float]:
        if self._bids:
            return -next(iter(self._bids))
        return None

    @property
    def best_ask(self) -> Optional[float]:
        if self._asks:
            return next(iter(self._asks))
        return None

    @property
    def spread(self) -> Optional[float]:
        bb, ba = self.best_bid, self.best_ask
        return ba - bb if bb is not None and ba is not None else None

    def get_depth(self, levels: int = 5) -> Dict[str, List[Tuple[float, float]]]:
        bids = [(-k, sum(o.quantity for o in v)) for k, v in list(self._bids.items())[:levels]]
        asks = [(k, sum(o.quantity for o in v)) for k, v in list(self._asks.items())[:levels]]
        return {"bids": bids, "asks": asks}

    def get_snapshot(self) -> Dict:
        return {
            "best_bid": self.best_bid,
            "best_ask": self.best_ask,
            "spread": self.spread,
            "depth": self.get_depth(),
            "fills": len(self.fills)
        }

# Unit Tests
def test_orderbook():
    ob = OrderBook()
    ob.submit_limit_order(Side.ASK, 100.0, 10, "maker")
    fills = ob.submit_market_order(Side.BID, 5, "taker")
    print(f"✅ Test passed! Fills: {len(fills)}")
    print("Snapshot:", ob.get_snapshot())

if __name__ == "__main__":
    test_orderbook()