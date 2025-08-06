"""
Simple unit tests for customer routes (UI layer)
"""

import unittest
from app import create_app, db
from app.models import User, Customer, Restaurant, Food, Cart, OrderList, Address, Cuisine
from datetime import time


class TestRoutes(unittest.TestCase):
    """Test customer routes - 4 essential UI tests"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.setup_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setup_test_data(self):
        # Customer user
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

    def login(self):
        return self.client.post('/auth/login', data={
            'email': 'test@test.com', 'password': 'test'
        })

    def test_1_view_restaurants_needs_auth(self):
        """Test 1: Restaurants page requires authentication"""
        response = self.client.get('/customer/view_restaurants')
        self.assertEqual(response.status_code, 302)

    def test_2_view_restaurants_success(self):
        """Test 2: Can view restaurants when logged in"""
        self.login()
        response = self.client.get('/customer/view_restaurants')
        self.assertEqual(response.status_code, 200)

    def test_3_add_to_cart(self):
        """Test 3: Can add items to cart"""
        self.login()
        response = self.client.get(f'/customer/update_cart?food_id={self.food.id}&action=add')
        self.assertEqual(response.status_code, 302)
        
        cart_item = Cart.query.filter_by(customer_id=self.customer.id, food_id=self.food.id).first()
        self.assertIsNotNone(cart_item)

    def test_4_place_order(self):
        """Test 4: Can place orders"""
        self.login()
        cart = Cart(customer_id=self.customer.id, food_id=self.food.id, quantity=1)
        db.session.add(cart)
        db.session.commit()
        
        response = self.client.post('/customer/order')
        self.assertEqual(response.status_code, 302)
        
        order = OrderList.query.filter_by(customer_id=self.customer.id).first()
        self.assertIsNotNone(order)

    def test_5_view_restaurant_detail(self):
        """Test 5: Can view restaurant details and menu"""
        self.login()
        response = self.client.get(f'/customer/view_restaurant?restaurant_id={self.restaurant.id}')
        self.assertEqual(response.status_code, 200)

    def test_6_view_order_history(self):
        """Test 6: Can view order history"""
        self.login()
        # Create an order first
        order = OrderList(customer_id=self.customer.id, restaurant_id=self.restaurant.id, 
                         total_price=10.0, status='d')
        db.session.add(order)
        db.session.commit()
        
        response = self.client.get('/customer/view_order_history')
        self.assertEqual(response.status_code, 200)

    def test_7_cancel_order(self):
        """Test 7: Can cancel pending orders"""
        self.login()
        # Create a pending order
        order = OrderList(customer_id=self.customer.id, restaurant_id=self.restaurant.id,
                         total_price=10.0, status='p')
        db.session.add(order)
        db.session.commit()
        
        response = self.client.get(f'/customer/order/cancel?order_id={order.id}')
        self.assertEqual(response.status_code, 302)
        
        # Check order was cancelled
        cancelled_order = OrderList.query.get(order.id)
        self.assertEqual(cancelled_order.status, 'c')
