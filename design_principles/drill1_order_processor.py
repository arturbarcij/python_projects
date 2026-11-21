"""Drill 1: OrderProcessor split by responsibility.

Payment is a Strategy passed per order. Repository and notifier are
long-lived collaborators injected once.
"""

from abc import ABC, abstractmethod
import sqlite3


class PaymentMethod(ABC):
    @abstractmethod
    def charge(self, amount: float) -> None:
        """Collect payment for the computed total."""


class CardPayment(PaymentMethod):
    def charge(self, amount: float) -> None:
        print(f"Charging card: {amount}")


class PayPalPayment(PaymentMethod):
    def charge(self, amount: float) -> None:
        print(f"Charging PayPal: {amount}")


class CryptoPayment(PaymentMethod):
    """New payment type: a new class, no edit to OrderProcessor."""

    def charge(self, amount: float) -> None:
        print(f"Charging crypto: {amount}")


class OrderRepository(ABC):
    @abstractmethod
    def save(self, total: float) -> None:
        """Persist an order total."""


class SqliteOrderRepository(OrderRepository):
    def __init__(self, db_path: str = "orders.db") -> None:
        self._db_path = db_path

    def save(self, total: float) -> None:
        with sqlite3.connect(self._db_path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS orders (total REAL)"
            )
            db.execute("INSERT INTO orders VALUES (?)", (total,))


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        """Deliver a message to the user."""


class ConsoleNotifier(Notifier):
    def send(self, message: str) -> None:
        print(message)


class OrderProcessor:
    def __init__(self, repository: OrderRepository, notifier: Notifier) -> None:
        self._repository = repository
        self._notifier = notifier

    def process(self, order: dict, payment: PaymentMethod) -> float:
        items = order.get("items") or []
        if not items:
            raise ValueError("empty order")
        total = sum(item["price"] * item["qty"] for item in items)
        payment.charge(total)
        self._repository.save(total)
        self._notifier.send(f"Email sent: order total {total}")
        return total


if __name__ == "__main__":
    processor = OrderProcessor(
        SqliteOrderRepository(":memory:"),
        ConsoleNotifier(),
    )
    order = {"items": [{"price": 10.0, "qty": 2}, {"price": 5.0, "qty": 1}]}
    processor.process(order, CardPayment())
    processor.process(order, PayPalPayment())
