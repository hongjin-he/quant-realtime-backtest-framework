from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict
from ..core.orderbook import OrderBook, Side, Fill

@dataclass
class StrategyMetrics:
    pnl: float = 0.0
    num_trades: int = 0
    inventory: float = 0.0
    fills: list = field(default_factory=list)

class BaseStrategy(ABC):
    def __init__(self, name: str):
        self.name = name
        self.metrics = StrategyMetrics()
        self.active_orders: Dict[int, Dict] = {}

    @abstractmethod
    def on_orderbook_update(self, ob: OrderBook, timestamp: float) -> List[Dict]:
        """Return actions like [{'action': 'submit_limit', 'side': 'bid', 'price': 99.5, 'qty': 1}]"""
        pass

    def on_fill(self, fill: Fill):
        self.metrics.num_trades += 1
        self.metrics.fills.append(fill)
        if fill.side == Side.BID:
            self.metrics.inventory += fill.quantity
        else:
            self.metrics.inventory -= fill.quantity

    def on_end(self, final_price: float):
        self.metrics.pnl = self.metrics.inventory * final_price

# Dummy for testing
class DummyStrategy(BaseStrategy):
    def on_orderbook_update(self, ob: OrderBook, timestamp: float) -> List[Dict]:
        return []