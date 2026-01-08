from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    """Value Object для представления денежной суммы"""
    
    amount: int
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
    
    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency
    
    @classmethod
    def zero(cls, currency: str = "USD") -> "Money":
        return cls(amount=0, currency=currency)
