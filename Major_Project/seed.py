from app import db, create_app
from app.models import User, Customer, Restaurant, Food, Cuisine, OrderList, OrderDetail, Address, DishReview, RestaurantReview
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push() 

# Clear existing data
db.session.commit()
db.drop_all()
db.create_all()


users = [
    User(id=2, email="customer1@example.com", code="1",
         password=generate_password_hash("cust123"), phone="1234567891"),
    User(id=3, email="customer2@example.com", code="1",
         password=generate_password_hash("cust123"), phone="1234567892"),
    User(id=4, email="restaurant1@example.com", code="2",
         password=generate_password_hash("rest123"), phone="1234567893"),
    User(id=5, email="restaurant2@example.com", code="2",
         password=generate_password_hash("rest123"), phone="1234567894"),
    User(id=6, email="restaurant3@example.com", code="2",
         password=generate_password_hash("rest123"), phone="1234567895"),
    User(id=7, email="restaurant4@example.com", code="2",
         password=generate_password_hash("rest123"), phone="1234567896"),
]
db.session.add_all(users)
db.session.commit()

# Create Customers
customers = [
    Customer(user_id=2, name="Alice"),
    Customer(user_id=3, name="Bob"),
]
db.session.add_all(customers)
db.session.commit()

# Create Restaurants (multiple per owner)
restaurants = [
    # Owner 1 (user_id=4)
    Restaurant(
        user_id=4,
        name="Bikaner Wala",
        description="Authentic Indian snacks and sweets served in a modern setting.",
        image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        opening_time=datetime.strptime("10:00", "%H:%M").time(),
        closing_time=datetime.strptime("22:00", "%H:%M").time(),
        rating=4.5
    ),
    Restaurant(
        user_id=4,
        name="Spice Garden",
        description="Premium dining experience with a focus on North Indian cuisine.",
        image_url="https://images.unsplash.com/photo-1552566626-52f8b828add9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        opening_time=datetime.strptime("11:00", "%H:%M").time(),
        closing_time=datetime.strptime("23:00", "%H:%M").time(),
        rating=4.7
    ),
    # Owner 2 (user_id=5)
    Restaurant(
        user_id=5,
        name="The Pizza Place",
        description="Authentic Italian pizzas and pasta in a cozy atmosphere.",
        image_url="https://images.unsplash.com/photo-1579751626657-72bc17010498?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        opening_time=datetime.strptime("11:30", "%H:%M").time(),
        closing_time=datetime.strptime("23:30", "%H:%M").time(),
        rating=4.6
    ),
    # Owner 3 (user_id=6)
    Restaurant(
        user_id=6,
        name="Sushi Express",
        description="Fresh and authentic Japanese cuisine with modern fusion twists.",
        image_url="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        opening_time=datetime.strptime("12:00", "%H:%M").time(),
        closing_time=datetime.strptime("22:30", "%H:%M").time(),
        rating=4.8
    ),
]

db.session.add_all(restaurants)
db.session.commit()

# Create Cuisines
cuisines = [Cuisine(name="Italian"), Cuisine(name="Japanese"),
            Cuisine(name="American"), Cuisine(name="Mexican"),
            Cuisine(name="Indian"), Cuisine(name="Chinese"),
            ]
db.session.add_all(cuisines)
db.session.commit()

# Create Food Items
foods = [
    Food(restaurant_id=1, name="Tandoori Chaap",
         price=200, cuisine_id=5, category="Starters", is_special=True),
    Food(restaurant_id=1, name="Butter Naan", price=20,
         cuisine_id=5, category="Main Course", is_deal_of_day=True),
    Food(restaurant_id=2, name="Dosa", price=150,
         cuisine_id=5, category="Main Course", is_special=True),
    Food(restaurant_id=2, name="Fried Rice",
         price=130, cuisine_id=6, category="Chinese", is_deal_of_day=True),
    Food(restaurant_id=3, name="McVeggie Burger",
         price=80, cuisine_id=3, category="Burgers", is_special=True),
    Food(restaurant_id=3, name="McAloo Tikki Burger",
         price=50, cuisine_id=3, category="Burgers"),
    Food(restaurant_id=3, name="Fries", price=50,
         cuisine_id=3, category="Fries", is_deal_of_day=True),
    Food(restaurant_id=4, name="Margherita Pizza",
         price=200, cuisine_id=1, category="Classic", is_special=True),
    Food(restaurant_id=4, name="Veggie Paradise Pizza",
         price=349, cuisine_id=1, category="Special", is_deal_of_day=True),
    Food(
        name="Butter Chicken",
        price=350,
        restaurant_id=1,
        category="Main Course",
        cuisine_id=5,  # Indian cuisine
        is_special=True
    ),
    Food(
        name="Dal Makhani",
        price=250,
        restaurant_id=1,
        category="Main Course",
        cuisine_id=5  # Indian cuisine
    ),
    Food(
        name="Margherita Pizza",
        price=400,
        restaurant_id=2,
        category="Pizza",
        cuisine_id=1,  # Italian cuisine
        is_deal_of_day=True
    ),
]
db.session.add_all(foods)
db.session.commit()


# Create Addresses
addresses = [
    Address(user_id=2, full_address="123 Main St", city="Springfield", location="IL"),
    Address(user_id=3, full_address="456 Elm St", city="Springfield", location="IL"),
    Address(user_id=4, full_address="Iifco Chowk", city="Gurugram", location="Gurugram"),
    Address(user_id=5, full_address="A-2 Paschim Vihar", city="Delhi", location="Paschim Vihar"),
    Address(user_id=6, full_address="Sector 46 Noida", city="Noida", location="Noida"),
    Address(user_id=7, full_address="Near MGF Toyota", city="Delhi", location="Rajouri Garden"),
]
db.session.add_all(addresses)
db.session.commit()

print("Seeding completed successfully!")