from enum import Enum


class OrderStatus(Enum):
    """Перечисление статусов заказа"""
    
    DRAFT = "draft"
    PAID = "paid"
    CANCELLED = "cancelled"
