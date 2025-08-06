# Customer Module Tests

This folder contains **11 tests** for the customer module, covering the most important functionality.

## Test Structure

### UI Tests (7 tests) - `routes/test_routes.py`
1. **test_1_view_restaurants_needs_auth** - Ensures authentication is required
2. **test_2_view_restaurants_success** - Tests successful restaurant viewing  
3. **test_3_add_to_cart** - Tests adding items to cart via UI
4. **test_4_place_order** - Tests order placement via UI
5. **test_5_view_restaurant_detail** - Tests viewing individual restaurant details and menu
6. **test_6_view_order_history** - Tests viewing order history page
7. **test_7_cancel_order** - Tests cancelling pending orders

### Service Tests (4 tests) - `services/test_services.py`
8. **test_8_get_customer_id** - Tests customer ID retrieval
9. **test_9_get_restaurant_list** - Tests restaurant listing service
10. **test_10_add_to_cart_service** - Tests cart service business logic
11. **test_11_place_order_service** - Tests order placement business logic

## Running Tests

### Run All 11 Tests
```bash
python tests/run_tests.py
```

### Run Individual Test Files
```bash
# UI tests only
python -m unittest tests.routes.test_routes

# Service tests only  
python -m unittest tests.services.test_services
```

### Run Single Test
```bash
python -m unittest tests.routes.test_routes.TestRoutes.test_1_view_restaurants_needs_auth
```

## Test Coverage

These 11 tests cover:
- ✅ Authentication and authorization
- ✅ Restaurant browsing and filtering
- ✅ Restaurant detail viewing
- ✅ Shopping cart functionality
- ✅ Order placement and management
- ✅ Order history and cancellation
- ✅ Core business logic and services

## Folder Structure

```
tests/
├── README.md              # This documentation
├── run_tests.py          # Main test runner for all 11 tests
├── __init__.py           # Test package initialization
├── routes/
│   ├── test_routes.py    # 7 UI/route tests
│   └── __init__.py
└── services/
    ├── test_services.py  # 4 service/business logic tests
    └── __init__.py
```

## Notes

- Tests use in-memory SQLite for speed and isolation
- Each test is independent with proper setup/teardown
- Tests focus on the most critical customer workflows
- Simple, maintainable test structure for long-term use  

