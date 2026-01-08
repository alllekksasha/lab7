from abc import ABC, abstractmethod
from typing import Optional
from domain.order import Order
from domain.money import Money


class OrderRepository(ABC):
    """Интерфейс репозитория заказов"""
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Получает заказ по идентификатору"""
        pass
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Сохраняет заказ"""
        pass


class PaymentGateway(ABC):
    """Интерфейс платёжного шлюза"""
    
    @abstractmethod
    def charge(self, order_id: str, money: Money) -> bool:
        """
        Выполняет списание средств.
        Возвращает True при успешной оплате, False при ошибке
        """
        pass
