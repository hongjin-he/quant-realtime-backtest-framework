from typing import List, Dict
from .core.orderbook import OrderBook, Side
from .strategies.base import BaseStrategy

class Arena:
    """
    Strategy Arena: Multiple strategies compete in one OrderBook
    """
    def __init__(self, strategies: List[BaseStrategy]):
        self.strategies = {s.name: s for s in strategies}
        self.ob = OrderBook()
        self.timestamp = 0.0
        self.history = []

    def run_synthetic(self, steps: int = 1000):
        """
        Run synthetic simulation with noise orders
        """
        for step in range(steps):
            self.timestamp += 0.001  # tick time
            
            # External noise (market making)
            noise_price = 100.0 + step * 0.0001
            self.ob.submit_limit_order(Side.ASK, noise_price + 0.01, 1.0, "noise")
            self.ob.submit_limit_order(Side.BID, noise_price - 0.01, 1.0, "noise")
            
            # Strategies make decisions
            for name, strategy in self.strategies.items():
                actions = strategy.on_orderbook_update(self.ob, self.timestamp)
                self._execute_actions(strategy, actions)
            
            # Snapshot
            self.history.append(self.ob.get_snapshot())

        # Final settlement
        final_price = self.ob.mid_price or 100.0
        for strategy in self.strategies.values():
            strategy.on_end(final_price)

        return self.get_results()

    def _execute_actions(self, strategy: BaseStrategy, actions: List[Dict]):
        for action in actions:
            act_type = action["action"]
            if act_type == "submit_limit":
                side = Side.BID if action["side"] == "bid" else Side.ASK
                oid, fills = self.ob.submit_limit_order(
                    side, action["price"], action["qty"], strategy.name
                )
                strategy.active_orders[oid] = action
                for fill in fills:
                    strategy.on_fill(fill)
            elif act_type == "submit_market":
                side = Side.BID if action["side"] == "bid" else Side.ASK
                fills = self.ob.submit_market_order(side, action["qty"], strategy.name)
                for fill in fills:
                    strategy.on_fill(fill)
            elif act_type == "cancel":
                self.ob.cancel_order(action["order_id"])
                strategy.active_orders.pop(action["order_id"], None)

    def get_results(self) -> Dict[str, Dict]:
        return {
            name: {
                "pnl": s.metrics.pnl,
                "num_trades": s.metrics.num_trades,
                "inventory": s.metrics.inventory,
                "sharpe": s.metrics.sharpe if s.metrics.sharpe else 0
            }
            for name, s in self.strategies.items()
        }

    def print_leaderboard(self):
        results = self.get_results()
        sorted_results = sorted(results.items(), key=lambda x: x[1]["pnl"], reverse=True)
        print("\n" + "="*60)
        print("🏆 STRATEGY ARENA LEADERBOARD 🏆")
        print("="*60)
        for rank, (name, r) in enumerate(sorted_results, 1):
            emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "⚪"
            print(f"{emoji} #{rank} {name:<15} | PnL: ${r['pnl']:>8.2f} | Trades: {r['num_trades']:>4} | Inv: {r['inventory']:>6.1f}")
        print("="*60)