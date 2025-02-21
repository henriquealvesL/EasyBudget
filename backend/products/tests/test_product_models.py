import pytest
from products.models import Product

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(name="Test Product", description="Description",price=100)
    assert product.name == "Test Product"
    assert product.price == 100