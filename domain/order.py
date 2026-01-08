from typing import List
from domain.money import Money
from domain.order_line import OrderLine
from domain.order_status import OrderStatus


class Order:
    """
    Сущность заказа — корень агрегата
    
    Инварианты:
    - Нельзя оплатить пустой заказ
    - Нельзя оплатить заказ повторно
    - После оплаты нельзя менять строки заказа
    - Итоговая сумма равна сумме строк
    """
    
    def __init__(self, order_id: str, customer_id: str):
        self._order_id = order_id
        self._customer_id = customer_id
        self._lines: List[OrderLine] = []
        self._status = OrderStatus.DRAFT
    
    @property
    def order_id(self) -> str:
        return self._order_id
    
    @property
    def customer_id(self) -> str:
        return self._customer_id
    
    @property
    def status(self) -> OrderStatus:
        return self._status
    
    @property
    def lines(self) -> List[OrderLine]:
        return self._lines.copy()
    
    @property
    def total(self) -> Money:
        """Вычисляет итоговую сумму заказа"""
        if not self._lines:
            return Money.zero()
        
        result = Money.zero(self._lines[0].unit_price.currency)
        for line in self._lines:
            result = result + line.total
        return result
    
    def add_line(self, line: OrderLine) -> None:
        """Добавляет строку в заказ"""
        if self._status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self._lines.append(line)
    
    def remove_line(self, product_name: str) -> None:
        """Удаляет строку из заказа по названию продукта"""
        if self._status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self._lines = [line for line in self._lines if line.product_name != product_name]
    
    def pay(self) -> None:
        """Переводит заказ в статус оплаченного"""
        if not self._lines:
            raise ValueError("Cannot pay empty order")
        if self._status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        self._status = OrderStatus.PAID
    
    def is_paid(self) -> bool:
        """Проверяет, оплачен ли заказ"""
        return self._status == OrderStatus.PAID
