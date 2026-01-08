import pytest
from domain.money import Money
from domain.order import Order
from domain.order_line import OrderLine
from domain.order_status import OrderStatus
from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


class TestPayOrderUseCase:
    """Тесты use-case оплаты заказа"""
    
    def setup_method(self):
        """Подготовка перед каждым тестом"""
        self.repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway(should_succeed=True)
        self.use_case = PayOrderUseCase(self.repository, self.payment_gateway)
    
    def _create_order_with_items(self, order_id: str = "order-1") -> Order:
        """Создаёт заказ с товарами для тестов"""
        order = Order(order_id=order_id, customer_id="customer-1")
        order.add_line(OrderLine(
            product_name="Product A",
            quantity=2,
            unit_price=Money(amount=100)
        ))
        order.add_line(OrderLine(
            product_name="Product B",
            quantity=1,
            unit_price=Money(amount=50)
        ))
        return order
    
    def test_successful_payment(self):
        """Тест успешной оплаты корректного заказа"""
        # Arrange
        order = self._create_order_with_items()
        self.repository.save(order)
        
        # Act
        result = self.use_case.execute("order-1")
        
        # Assert
        assert result.success is True
        assert result.message == "Payment successful"
        
        saved_order = self.repository.get_by_id("order-1")
        assert saved_order.is_paid() is True
        
        assert len(self.payment_gateway.charges) == 1
        assert self.payment_gateway.charges[0][1].amount == 250
    
    def test_empty_order_payment_fails(self):
        """Тест ошибки при оплате пустого заказа"""
        # Arrange
        order = Order(order_id="order-empty", customer_id="customer-1")
        self.repository.save(order)
        
        # Act
        result = self.use_case.execute("order-empty")
        
        # Assert
        assert result.success is False
        assert result.message == "Cannot pay empty order"
    
    def test_double_payment_fails(self):
        """Тест ошибки при повторной оплате"""
        # Arrange
        order = self._create_order_with_items()
        self.repository.save(order)
        
        # Первая оплата
        self.use_case.execute("order-1")
        
        # Act - попытка повторной оплаты
        result = self.use_case.execute("order-1")
        
        # Assert
        assert result.success is False
        assert result.message == "Order already paid"
    
    def test_cannot_modify_paid_order(self):
        """Тест невозможности изменения заказа после оплаты"""
        # Arrange
        order = self._create_order_with_items()
        self.repository.save(order)
        self.use_case.execute("order-1")
        
        # Act & Assert
        paid_order = self.repository.get_by_id("order-1")
        
        with pytest.raises(ValueError, match="Cannot modify paid order"):
            paid_order.add_line(OrderLine(
                product_name="Product C",
                quantity=1,
                unit_price=Money(amount=30)
            ))
        
        with pytest.raises(ValueError, match="Cannot modify paid order"):
            paid_order.remove_line("Product A")
    
    def test_correct_total_calculation(self):
        """Тест корректного расчёта итоговой суммы"""
        # Arrange
        order = Order(order_id="order-calc", customer_id="customer-1")
        order.add_line(OrderLine(
            product_name="Item 1",
            quantity=3,
            unit_price=Money(amount=100)
        ))
        order.add_line(OrderLine(
            product_name="Item 2",
            quantity=2,
            unit_price=Money(amount=75)
        ))
        
        # Act
        total = order.total
        
        # Assert
        # 3 * 100 + 2 * 75 = 300 + 150 = 450
        assert total.amount == 450
        assert total.currency == "USD"
    
    def test_order_not_found(self):
        """Тест ошибки при оплате несуществующего заказа"""
        # Act
        result = self.use_case.execute("non-existent-order")
        
        # Assert
        assert result.success is False
        assert result.message == "Order not found"
    
    def test_payment_gateway_failure(self):
        """Тест обработки ошибки платёжного шлюза"""
        # Arrange
        order = self._create_order_with_items()
        self.repository.save(order)
        self.payment_gateway.set_should_succeed(False)
        
        # Act
        result = self.use_case.execute("order-1")
        
        # Assert
        assert result.success is False
        assert result.message == "Payment failed"
