from typing import Dict, Optional
from domain.order import Order
from application.interfaces import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """
    Реализация репозитория заказов в памяти.
    Используется для тестирования без реальной базы данных
    """
    
    def __init__(self):
        self._storage: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Получает заказ по идентификатору"""
        return self._storage.get(order_id)
    
    def save(self, order: Order) -> None:
        """Сохраняет заказ в хранилище"""
        self._storage[order.order_id] = order
    
    def clear(self) -> None:
        """Очищает хранилище (для тестов)"""
        self._storage.clear()
