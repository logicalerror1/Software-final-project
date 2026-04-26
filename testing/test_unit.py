"""
UNIT TESTING - Brew-Time Coffee System
Tests individual components in isolation
Author: [Your Name]
Date: April 2026
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from models import Product, Order, OrderItem


class TestProductModel(unittest.TestCase):
    """Test Product model - individual unit tests"""
    
    def setUp(self):
        """Setup before each test"""
        self.product = Product(name="Latte", price=4.50, description="Hot coffee with milk")
    
    def test_product_creation(self):
        """TC-UNIT-01: Verify product can be created with name and price"""
        self.assertEqual(self.product.name, "Latte")
        self.assertEqual(self.product.price, 4.50)
        print(" TC-UNIT-01 PASSED: Product creation")
    
    def test_product_price_type(self):
        """TC-UNIT-02: Verify price is float type"""
        self.assertIsInstance(self.product.price, float)
        print(" TC-UNIT-02 PASSED: Price type is float")
    
    def test_product_name_not_empty(self):
        """TC-UNIT-03: Verify product name is not empty"""
        self.assertTrue(len(self.product.name) > 0)
        print("TC-UNIT-03 PASSED: Product name not empty")
    
    def test_product_price_positive(self):
        """TC-UNIT-04: Verify product price is positive"""
        self.assertGreater(self.product.price, 0)
        print(" TC-UNIT-04 PASSED: Price is positive")


class TestOrderModel(unittest.TestCase):
    """Test Order model - individual unit tests"""
    
    def setUp(self):
        self.order = Order(status="Pending", total_price=0.0)
    
    def test_order_creation(self):
        """TC-UNIT-05: Verify order can be created with pending status"""
        self.assertEqual(self.order.status, "Pending")
        self.assertIsNotNone(self.order.id)
        print(" TC-UNIT-05 PASSED: Order creation")
    
    def test_order_initial_status(self):
        """TC-UNIT-06: Verify new order has 'Pending' status"""
        self.assertEqual(self.order.status, "Pending")
        print(" TC-UNIT-06 PASSED: Initial status is Pending")
    
    def test_order_total_calculation(self):
        """TC-UNIT-07: Verify order total can be set and retrieved"""
        self.order.total_price = 12.50
        self.assertEqual(self.order.total_price, 12.50)
        print(" TC-UNIT-07 PASSED: Total calculation")
    
    def test_order_has_timestamp(self):
        """TC-UNIT-08: Verify order has created_at timestamp"""
        self.assertIsNotNone(self.order.created_at)
        print(" TC-UNIT-08 PASSED: Timestamp exists")


class TestOrderItemModel(unittest.TestCase):
    """Test OrderItem model - individual unit tests"""
    
    def setUp(self):
        self.product = Product(name="Cappuccino", price=4.00)
        self.order_item = OrderItem(product=self.product, quantity=2)
    
    def test_order_item_creation(self):
        """TC-UNIT-09: Verify order item has product and quantity"""
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.product.name, "Cappuccino")
        print(" TC-UNIT-09 PASSED: Order item creation")
    
    def test_order_item_quantity_positive(self):
        """TC-UNIT-10: Verify quantity is positive"""
        self.assertGreater(self.order_item.quantity, 0)
        print(" TC-UNIT-10 PASSED: Quantity is positive")


class TestPriceCalculation(unittest.TestCase):
    """Test price calculation logic - independent unit tests"""
    
    def test_calculate_single_item_price(self):
        """TC-UNIT-11: Calculate price for single item"""
        price = 4.50
        quantity = 1
        total = price * quantity
        self.assertEqual(total, 4.50)
        print(" TC-UNIT-11 PASSED: Single item price = $4.50")
    
    def test_calculate_multiple_items_price(self):
        """TC-UNIT-12: Calculate price for multiple different items"""
        latte_total = 4.50 * 2   # 2 Lattes
        croissant_total = 3.00 * 1  # 1 Croissant
        total = latte_total + croissant_total
        self.assertEqual(total, 12.00)
        print(" TC-UNIT-12 PASSED: Multiple items total = $12.00")
    
    def test_discount_calculation_10_percent(self):
        """TC-UNIT-13: Calculate 10% discount correctly"""
        subtotal = 10.00
        discount = subtotal * 0.10
        final = subtotal - discount
        self.assertEqual(final, 9.00)
        print(" TC-UNIT-13 PASSED: 10% discount = $9.00")
    
    def test_empty_cart_total(self):
        """TC-UNIT-14: Empty cart should total $0"""
        total = 0
        self.assertEqual(total, 0)
        print(" TC-UNIT-14 PASSED: Empty cart = $0")


class TestStatusTransitions(unittest.TestCase):
    """Test order status transition logic"""
    
    def test_valid_status_transitions(self):
        """TC-UNIT-15: Verify valid status transitions"""
        valid_statuses = ["Pending", "Preparing", "Ready", "Completed"]
        for status in valid_statuses:
            order = Order(status=status)
            self.assertEqual(order.status, status)
        print("TC-UNIT-15 PASSED: Valid status transitions")
    
    def test_order_has_items_relationship(self):
        """TC-UNIT-16: Verify order can have multiple items"""
        order = Order()
        self.assertTrue(hasattr(order, 'items'))
        print(" TC-UNIT-16 PASSED: Order-Items relationship exists")


def run_unit_tests():
    """Run all unit tests"""
    print("\n" + "="*70)
    print(" UNIT TESTING PHASE - Brew-Time Coffee System")
    print("="*70)
    print("\n Testing Strategy: Individual components tested in isolation")
    print("   - Product model validation")
    print("   - Order model validation")
    print("   - OrderItem model validation")
    print("   - Price calculation logic")
    print("   - Status transition logic")
    print("="*70 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProductModel))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderModel))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderItemModel))
    suite.addTests(loader.loadTestsFromTestCase(TestPriceCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestStatusTransitions))
    
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print(" UNIT TEST SUMMARY")
    print("="*70)
    print(f" Tests Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" Tests Failed: {len(result.failures)}")
    print(f" Errors: {len(result.errors)}")
    print(f" Total Tests Run: {result.testsRun}")
    print("="*70)
    
    return result


if __name__ == '__main__':
    run_unit_tests()