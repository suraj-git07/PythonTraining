# JustEat - Food Delivery Application

A full-stack Flask web application that connects customers with restaurants for seamless food ordering and delivery.

## 🚀 Features Implementation

### **Authentication & User Management** 
-  **User Login/Logout**: Secure authentication for both customers and restaurant owners
-  **Password Reset**: Both customers and restaurant owners can reset their passwords
-  **User Roles**: Differentiated access (Customer: code=1, Restaurant Owner: code=2)
-  **Database Migrations**: Flask-Migrate implementation for schema management

###  **Customer Features** 
-  **Restaurant Discovery**: Browse and search restaurants by location, cuisine, or name
-  **Advanced Filtering**: Filter by cuisine type, restaurant name, location, price range, and rating
-  **Menu Browsing**: View detailed menus with prices, categories, and cuisine information
-  **Cart Management**: Add items with custom quantities, update cart, and place orders
-  **Order Tracking**: Track order status (pending/delivered/cancelled) and view comprehensive order history with search
-  **Profile Management**: Update personal information, phone, email
-  **Favorites System**: 
  - Save favorite restaurants (manual and auto-detection based on order frequency)
  - Save favorite food items (manual and auto-detection)
  - View "My Favourite" page with preferred items
-  **Order History Search**: Search through past orders with detailed order information

###  **Smart Recommendations** 
-  **Automatic Favorites**: System auto-detects frequently ordered restaurants and dishes


###  **Restaurant Owner Features**
-  **Restaurant Registration**: Register and manage restaurant profiles
-  **Menu Management**: Add, edit, and delete menu items with pricing and categories
-  **Order Processing**: View, manage and process orders received from customers
-  **Special Items**: Mark items as "Today's Special" and "Deal of the Day"
-  **Analytics**: Automatic "Mostly Ordered" tags for items ordered 10+ times per day
-  **Multiple Restaurant Support**: Restaurant owners can manage multiple restaurants

###  **BONUS Features** 
-  **Rating & Review System**: 
  - Customers can rate and review both restaurants and individual dishes
  - Reviews visible to all customers with corresponding restaurants and cuisines
  - Review system integrated with order completion
-  **Customer Feedback**: Comprehensive review system allows customers to provide detailed feedback
-  **Review Management**: Restaurant owners can view customer reviews and ratings

## 🚀 Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login with bcrypt password hashing
- **Frontend**: HTML5, CSS3, JavaScript
- **Forms**: Flask-WTF with CSRF protection
- **Database Migrations**: Flask-Migrate

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd Major_Project
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create `.env` file based on `demo_env`:
```bash
cp demo_env .env
```

### 5. Initialize Database
```bash
# Seed sample data
python seed.py
```

### 6. Run Application
```bash
python run.py
```

Access the application at: **http://127.0.0.1:5000**

## 🗄️ Database Schema

### Core Models

| Model | Description | Key Fields |
|-------|-------------|------------|
| **User** | Authentication and user management | `id`, `email`, `code` (1=Customer, 2=Restaurant), `password`, `phone` |
| **Customer** | Customer profiles | `id`, `user_id`, `name` |
| **Restaurant** | Restaurant information | `id`, `user_id`, `name`, `description`, `image_url`, `opening_time`, `closing_time`, `rating` |
| **Food** | Menu items | `id`, `restaurant_id`, `name`, `price`, `cuisine_id`, `category`, `is_special`, `is_deal_of_day` |
| **OrderList** | Order management | `id`, `customer_id`, `restaurant_id`, `total_price`, `status`, `order_time`, `delivery_time` |
| **OrderDetail** | Order line items | `id`, `order_id`, `food_id`, `quantity` |
| **Cart** | Shopping cart | `id`, `customer_id`, `food_id`, `quantity` |

### Supporting Models

| Model | Description | Key Fields |
|-------|-------------|------------|
| **Address** | Location management | `id`, `user_id`, `full_address`, `city`, `location` |
| **Cuisine** | Food categories | `id`, `name` |
| **FavouriteRestaurant** | User restaurant preferences | `id`, `customer_id`, `restaurant_id`, `mode` (a=auto, m=manual) |
| **FavouriteFood** | User food preferences | `id`, `customer_id`, `food_id`, `mode` (a=auto, m=manual) |
| **DishReview** | Dish ratings and reviews | `id`, `customer_id`, `food_id`, `order_id`, `rating`, `review`, `review_time` |
| **RestaurantReview** | Restaurant ratings and reviews | `id`, `customer_id`, `restaurant_id`, `order_id`, `rating`, `review`, `review_time` |

## 🔐 Demo Credentials

### Restaurant Owners
```
Email: restaurant1@example.com | Password: rest123
Email: restaurant2@example.com | Password: rest123
Email: restaurant3@example.com | Password: rest123
Email: restaurant4@example.com | Password: rest123
```

### Customers
```
Email: customer1@example.com | Password: cust123
Email: customer2@example.com | Password: cust123
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run all tests
python tests/run_tests.py

# Run specific test modules
python -m unittest tests.routes.test_routes    # UI tests
python -m unittest tests.services.test_services # Service tests
```

## 📁 Project Structure

```
Major_Project/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models
│   ├── config.py                # Configuration settings
│   ├── auth/                    # Authentication routes
│   ├── customer/                # Customer functionality
│   ├── restaurant/              # Restaurant functionality
│   ├── static/                  # CSS, JS, images
│   └── templates/               # HTML templates
├── tests/                       # Test suite
├── migrations/                  # Database migrations
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
└── seed.py                     # Database seeding
```

## 📝 API Endpoints

### Authentication Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page - redirects to appropriate dashboard |
| `GET/POST` | `/auth/login` | User login |
| `GET` | `/auth/logout` | User logout |

### Customer Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/customer/` | Customer home - redirects to restaurants |
| `GET` | `/customer/view_restaurants` | Browse restaurants with filters |
| `GET` | `/customer/view_restaurant` | Restaurant details and menu |
| `GET/POST` | `/customer/update_cart` | Add/remove items from cart |
| `GET` | `/customer/view_cart` | View shopping cart |
| `GET` | `/customer/cart` | Alternative cart route |
| `GET/POST` | `/customer/cart/update` | Update cart from cart page |
| `GET` | `/customer/clear_cart` | Clear cart items |
| `GET/POST` | `/customer/order` | Place order from cart |
| `GET` | `/customer/view_order_history` | View order history |
| `GET/POST` | `/customer/order_detail/<order_id>` | Order details with review options |
| `GET` | `/customer/order/cancel` | Cancel pending order |
| `GET/POST` | `/customer/view_profile` | View and update customer profile |
| `GET/POST` | `/customer/apply_name_filter` | Filter restaurants by name |
| `GET` | `/customer/add_favourite_restaurant` | Add restaurant to favorites |
| `GET` | `/customer/remove_favourite_restaurant` | Remove restaurant from favorites |
| `GET` | `/customer/set_favourite_food` | Add food item to favorites |
| `GET` | `/customer/remove_favourite_food` | Remove food item from favorites |
| `GET/POST` | `/customer/reset_password` | Reset customer password |
| `GET` | `/customer/mostly_ordered` | View frequently ordered items |
| `GET` | `/customer/auto_set_fav_rest` | Auto-set favorite restaurants (development) |
| `POST` | `/customer/toggle_favorite_restaurant/<restaurant_id>` | Toggle restaurant favorite status (AJAX) |

### Restaurant Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/restaurant/` | Restaurant dashboard |
| `GET` | `/restaurant/view_orders` | View all incoming orders |
| `GET` | `/restaurant/order_detail/<order_id>` | View specific order details |
| `GET` | `/restaurant/view_menu` | View and manage menu |
| `GET/POST` | `/restaurant/add_dish` | Add new dish to menu |
| `GET` | `/restaurant/remove_dish` | Remove dish from menu |
| `POST` | `/restaurant/update_menu` | Update multiple menu items |
| `GET` | `/restaurant/mark_order_as_delivered` | Mark order as delivered |
| `GET` | `/restaurant/make_dish_of_the_day` | Mark dish as special (incomplete route) |
| `GET` | `/restaurant/view_profile` | View restaurant owner profile |
| `GET/POST` | `/restaurant/reset_password` | Reset restaurant password |
| `GET/POST` | `/restaurant/restaurant/add` | Add new restaurant |
| `GET/POST` | `/restaurant/restaurant/<restaurant_id>/edit` | Edit restaurant details |
| `GET` | `/restaurant/restaurant/<restaurant_id>` | View restaurant details |
| `GET` | `/restaurant/restaurant/<restaurant_id>/orders` | View orders for specific restaurant |
| `GET` | `/restaurant/restaurant/<restaurant_id>/menu` | View menu for specific restaurant |
| `GET/POST` | `/restaurant/restaurant/<restaurant_id>/menu/add` | Add menu item to specific restaurant |
| `GET/POST` | `/restaurant/restaurant/<restaurant_id>/menu/<food_id>/edit` | Edit specific menu item |
| `GET` | `/restaurant/restaurant/<restaurant_id>/menu/<food_id>/delete` | Delete specific menu item |

---

*Built by Suraj Mishra using Flask and modern web technologies*
