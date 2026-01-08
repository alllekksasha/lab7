from dataclasses import dataclass
from application.interfaces import OrderRepository, PaymentGateway


@dataclass
class PayOrderResult:
    """Результат выполнения use-case оплаты заказа"""
    
    success: bool
    order_id: str
    message: str


class PayOrderUseCase:
    """
    Use-case оплаты заказа
    
    Шаги:
    1. Загружает заказ через OrderRepository
    2. Выполняет доменную операцию оплаты
    3. Вызывает платёж через PaymentGateway
    4. Сохраняет заказ
    5. Возвращает результат оплаты
    """
    
    def __init__(self, order_repository: OrderRepository, payment_gateway: PaymentGateway):
        self._order_repository = order_repository
        self._payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> PayOrderResult:
        """Выполняет оплату заказа"""
        
        # 1. Загружаем заказ
        order = self._order_repository.get_by_id(order_id)
        
        if order is None:
            return PayOrderResult(
                success=False,
                order_id=order_id,
                message="Order not found"
            )
        
        # 2. Выполняем доменную операцию оплаты
        try:
            order.pay()
        except ValueError as e:
            return PayOrderResult(
                success=False,
                order_id=order_id,
                message=str(e)
            )
        
        # 3. Вызываем платёжный шлюз
        payment_success = self._payment_gateway.charge(order_id, order.total)
        
        if not payment_success:
            return PayOrderResult(
                success=False,
                order_id=order_id,
                message="Payment failed"
            )
        
        # 4. Сохраняем заказ
        self._order_repository.save(order)
        
        # 5. Возвращаем результат
        return PayOrderResult(
            success=True,
            order_id=order_id,
            message="Payment successful"
        )
