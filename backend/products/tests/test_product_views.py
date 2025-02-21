from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product
from django.urls import reverse

class ProductListViewTestCase(APITestCase):
  def setUp(self):
    """Create test products"""
    self.product1 = Product.objects.create(name="Product 1", price=10.0)
    self.product2 = Product.objects.create(name="Product 2", price=20.0)
    self.url_list = reverse("product-list")
    self.url_create = reverse("product-create")

  def test_list_products(self):
    response = self.client.get(self.url_list)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

  def test_create_products(self):
    data = {"name": "Product-test", "price": 300, "description": "automated test product"}
    response = self.client.post(self.url_create, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Product.objects.count(), 3)
    self.assertEqual(Product.objects.last().name, "Product-test")

