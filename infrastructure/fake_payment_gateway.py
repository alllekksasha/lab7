from typing import List, Tuple
from domain.money import Money
from application.interfaces import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """
    Фейковая реализация платёжного шлюза.
    Используется для тестирования без реальных платежей
    """
    
    def __init__(self, should_succeed: bool = True):
        self._should_succeed = should_succeed
        self._charges: List[Tuple[str, Money]] = []
    
    def charge(self, order_id: str, money: Money) -> bool:
        """Имитирует списание средств"""
        self._charges.append((order_id, money))
        return self._should_succeed
    
    def set_should_succeed(self, value: bool) -> None:
        """Устанавливает, должны ли платежи проходить успешно"""
        self._should_succeed = value
    
    @property
    def charges(self) -> List[Tuple[str, Money]]:
        """Возвращает список выполненных списаний"""
        return self._charges.copy()
    
    def clear(self) -> None:
        """Очищает историю списаний (для тестов)"""
        self._charges.clear()
