import pytest
from django.contrib.auth.models import User
from products.models import Product

@pytest.fixture
def user(db):
    return User.objects.create(username="test_user", password="password123")

@pytest.fixture
def product(db):
    return Product.objects.create(name="Test Product", price=50.0)
