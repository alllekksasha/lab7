from dataclasses import dataclass
from domain.money import Money


@dataclass(frozen=True)
class OrderLine:
    """Строка заказа — часть агрегата Order"""
    
    product_name: str
    quantity: int
    unit_price: Money
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
    
    @property
    def total(self) -> Money:
        """Вычисляет стоимость строки заказа"""
        return Money(
            amount=self.unit_price.amount * self.quantity,
            currency=self.unit_price.currency
        )
