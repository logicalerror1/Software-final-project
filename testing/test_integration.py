"""
INTEGRATION TESTING - Brew-Time Coffee System
Tests interaction between Customer and Barista modules
Author: [Your Name]
Date: April 2026
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import Product


class TestCustomerBaristaIntegration(unittest.TestCase):
    """
    Integration tests between Customer UI and Barista Dashboard
    Verifies data flows correctly between components
    """
    
    def setUp(self):
        """Setup test database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test-key'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Add test products
            products = [
                Product(name="Latte", price=4.50),
                Product(name="Cappuccino", price=4.00),
                Product(name="Mocha", price=5.00),
                Product(name="Croissant", price=3.00)
            ]
            for p in products:
                db.session.add(p)
            db.session.commit()
        
        print(f"\n  Setup complete for: {self._testMethodName}")
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    # ========== INTEGRATION TEST CASES ==========
    
    def test_int_01_customer_order_reaches_barista(self):
        """
        TC-INT-01: Verify customer order appears on barista dashboard
        Integration point: Customer UI → Database → Barista UI
        """
        print("\n TC-INT-01: Customer order reaches barista")
        
        # Step 1: Customer places order
        order_data = {'items': [{'product_id': 1, 'quantity': 1}]}
        customer_response = self.client.post('/place_order',
                                            data=json.dumps(order_data),
                                            content_type='application/json')
        self.assertEqual(customer_response.status_code, 200)
        order_id = json.loads(customer_response.data)['order_id']
        print(f"  Customer placed order #{order_id}")
        
        # Step 2: Barista logs in
        self.client.post('/barista/login', data={'code': '1234'})
        
        # Step 3: Barista fetches orders
        barista_response = self.client.get('/orders')
        orders = json.loads(barista_response.data)
        
        # Step 4: Verify order appears
        found = any(o['id'] == order_id for o in orders)
        self.assertTrue(found, "Order should appear on barista dashboard")
        print(f" Order #{order_id} appears on barista dashboard")
        print(" TC-INT-01 PASSED: Customer → Barista data flow verified")
    
    def test_int_02_barista_status_update_reaches_customer(self):
        """
        TC-INT-02: Verify barista status update shows for customer
        Integration point: Barista UI → Database → Customer UI
        """
        print("\n TC-INT-02: Barista status update reaches customer")
        
        # Step 1: Customer places order
        order_data = {'items': [{'product_id': 1, 'quantity': 1}]}
        post_response = self.client.post('/place_order',
                                        data=json.dumps(order_data),
                                        content_type='application/json')
        order_id = json.loads(post_response.data)['order_id']
        
        # Step 2: Barista updates status
        self.client.post('/barista/login', data={'code': '1234'})
        update_response = self.client.post(f'/update_status/{order_id}',
                                          data=json.dumps({'status': 'Preparing'}),
                                          content_type='application/json')
        self.assertEqual(update_response.status_code, 200)
        print(f"  Barista updated status to 'Preparing'")
        
        # Step 3: Customer checks status
        customer_check = self.client.get(f'/status/{order_id}')
        status_data = json.loads(customer_check.data)
        
        # Step 4: Verify customer sees update
        self.assertEqual(status_data['status'], 'Preparing')
        print(f"  Customer sees status: {status_data['status']}")
        print(" TC-INT-02 PASSED: Barista → Customer data flow verified")
    
    def test_int_03_simultaneous_orders_queue_management(self):
        """
        TC-INT-03: Verify multiple orders are queued correctly
        Integration point: Multiple customers → Order queue → Barista
        """
        print("\n TC-INT-03: Multiple order queue management")
        
        # Step 1: Multiple customers place orders
        order_ids = []
        for i in range(3):
            order_data = {'items': [{'product_id': 1, 'quantity': 1}]}
            response = self.client.post('/place_order',
                                       data=json.dumps(order_data),
                                       content_type='application/json')
            order_id = json.loads(response.data)['order_id']
            order_ids.append(order_id)
        print(f"  3 customers placed orders: {order_ids}")
        
        # Step 2: Barista logs in
        self.client.post('/barista/login', data={'code': '1234'})
        
        # Step 3: Barista sees all orders
        response = self.client.get('/orders')
        orders = json.loads(response.data)
        
        # Step 4: Verify all orders appear
        for order_id in order_ids:
            found = any(o['id'] == order_id for o in orders)
            self.assertTrue(found, f"Order {order_id} should be in queue")
        
        self.assertGreaterEqual(len(orders), 3)
        print(f"   Barista sees all {len(orders)} orders in queue")
        print(" TC-INT-03 PASSED: Multiple order queue verified")
    
    def test_int_04_complete_order_workflow(self):
        """
        TC-INT-04: Verify complete workflow: 
        Customer → Place → Barista sees → Updates → Customer sees
        """
        print("\n TC-INT-04: Complete order workflow")
        
        # Step 1: Customer places order
        order_data = {'items': [{'product_id': 1, 'quantity': 2}, {'product_id': 4, 'quantity': 1}]}
        response = self.client.post('/place_order',
                                   data=json.dumps(order_data),
                                   content_type='application/json')
        order_id = json.loads(response.data)['order_id']
        print(f"   Step 1: Order #{order_id} placed")
        
        # Step 2: Barista logs in
        self.client.post('/barista/login', data={'code': '1234'})
        
        # Step 3: Barista sees order
        response = self.client.get('/orders')
        orders = json.loads(response.data)
        self.assertTrue(any(o['id'] == order_id for o in orders))
        print(f"   Step 2: Barista sees order #{order_id}")
        
        # Step 4: Barista updates through full workflow
        workflow = ['Preparing', 'Ready', 'Completed']
        for status in workflow:
            self.client.post(f'/update_status/{order_id}',
                           data=json.dumps({'status': status}),
                           content_type='application/json')
            print(f"   Step: Status → {status}")
        
        # Step 5: Customer sees final status
        final_check = self.client.get(f'/status/{order_id}')
        final_status = json.loads(final_check.data)['status']
        self.assertEqual(final_status, 'Completed')
        print(f"   Step 3: Customer sees order is Completed")
        
        print(" TC-INT-04 PASSED: Complete workflow verified")
    
    def test_int_05_authentication_separation(self):
        """
        TC-INT-05: Verify customer cannot access barista functions
        Integration point: Authentication layer
        """
        print("\n TC-INT-05: Authentication separation")
        
        # Customer tries to access barista dashboard
        response = self.client.get('/barista')
        self.assertEqual(response.status_code, 302, "Should redirect to login")
        print("   Customer cannot access barista dashboard")
        
        # Customer tries to update status
        response = self.client.post('/update_status/1',
                                   data=json.dumps({'status': 'Ready'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 403, "Should be forbidden")
        print("  Customer cannot update order status")
        
        # Customer tries to get all orders
        response = self.client.get('/orders')
        # Should be redirect (302) because not logged in
        self.assertEqual(response.status_code, 302)
        print("    Customer cannot view all orders")
        
        print(" TC-INT-05 PASSED: Authentication separation verified")


def run_integration_tests():
    """Run all integration tests"""
    print("\n" + "="*70)
    print(" INTEGRATION TESTING PHASE - Brew-Time Coffee System")
    print("="*70)
    print("\n  Testing Strategy: Verify communication between components")
    print("   - Customer UI ↔ Database ↔ Barista UI")
    print("   - Real-time status updates")
    print("   - Queue management")
    print("   - Authentication separation")
    print("="*70 + "\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCustomerBaristaIntegration)
    
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print(" INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f" Tests Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" Tests Failed: {len(result.failures)}")
    print(f" Total Tests: {result.testsRun}")
    print("="*70)
    
    return result


if __name__ == '__main__':
    run_integration_tests()