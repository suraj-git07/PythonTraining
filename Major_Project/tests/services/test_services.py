"""
Simple unit tests for services (Business logic)
"""

import unittest
from app import create_app, db
from app.models import User, Customer, Restaurant, Food, Cart, OrderList, Address, Cuisine
from app.customer.services import (
    get_customer_id_from_user_id, add_to_cart, place_order, get_restaurant_list
)
from datetime import time


class TestServices(unittest.TestCase):
    """Test customer services - 4 essential business logic tests"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.setup_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setup_test_data(self):
        # Customer
        self.user = User(email='test@test.com', code='1', phone='1234567890')
        self.user.set_password('test')
        db.session.add(self.user)
        db.session.flush()
        
        self.customer = Customer(user_id=self.user.id, name='Test Customer')
        db.session.add(self.customer)
        
        # Restaurant
        self.rest_user = User(email='rest@test.com', code='2', phone='0987654321')
        self.rest_user.set_password('test')
        db.session.add(self.rest_user)
        db.session.flush()
        
        self.restaurant = Restaurant(
            user_id=self.rest_user.id, name='Test Restaurant',
            opening_time=time(9, 0), closing_time=time(22, 0), rating=4.5
        )
        db.session.add(self.restaurant)
        
        self.address = Address(
            user_id=self.rest_user.id, full_address='123 Test St',
            city='Test City', location='Downtown'
        )
        db.session.add(self.address)
        
        self.cuisine = Cuisine(name='Italian')
        db.session.add(self.cuisine)
        db.session.flush()
        
        self.food = Food(
            restaurant_id=self.restaurant.id, name='Pizza', price=10.0,
            cuisine_id=self.cuisine.id, category='Main'
        )
        db.session.add(self.food)
        db.session.commit()

    def test_8_get_customer_id(self):
        """Test 8: Get customer ID from user ID"""
        customer_id = get_customer_id_from_user_id(self.user.id)
        self.assertEqual(customer_id, self.customer.id)

    def test_9_get_restaurant_list(self):
        """Test 9: Get list of restaurants"""
        restaurants = get_restaurant_list(self.customer.id)
        self.assertEqual(len(restaurants), 1)
        self.assertEqual(restaurants[0].name, 'Test Restaurant')

    def test_10_add_to_cart_service(self):
        """Test 10: Add item to cart service"""
        success, message = add_to_cart(self.food.id, self.customer.id)
        self.assertTrue(success)
        
        cart_item = Cart.query.filter_by(
            customer_id=self.customer.id, food_id=self.food.id
        ).first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 1)

    def test_11_place_order_service(self):
        """Test 11: Place order service"""
        # Add item to cart first
        cart = Cart(customer_id=self.customer.id, food_id=self.food.id, quantity=1)
        db.session.add(cart)
        db.session.commit()
        
        success, message = place_order(self.customer.id)
        self.assertTrue(success)
        
        order = OrderList.query.filter_by(customer_id=self.customer.id).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 10.0)
