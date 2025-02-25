from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product
from django.urls import reverse

class ProductListViewTestCase(APITestCase):
  def setUp(self):
    """Create test products"""
    self.product1 = Product.objects.create(name="Product 1", price=10.0)
    self.product2 = Product.objects.create(name="Product 2", price=20.0)

    self.url = reverse("product-list") # /products/
    self.url_detail = lambda pk: reverse("product-detail", kwargs={"pk": pk}) # /products/{id}/

  def test_list_products(self):
    """Test GET /products/"""
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

  def test_create_products(self):
    """Test POST /products/"""
    data = {"name": "Product 3", "price": 300, "description": "automated test product"}
    response = self.client.post(self.url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Product.objects.count(), 3)
    self.assertEqual(Product.objects.last().name, "Product 3")

  def test_get_product_detail(self):
    """Test GET /products/{id}/"""
    response = self.client.get(self.url_detail(self.product1.id))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["name"], self.product1.name)

  def test_update_product(self):
    """Test PUT /products/{id}/"""
    data = {"name": "Updated Product", "price": 50.0}
    response = self.client.put(self.url_detail(self.product1.id), data, format="json")
    self.assertEqual(response.status_code, 200)
    self.product1.refresh_from_db()
    self.assertEqual(self.product1.name, "Updated Product")

  def test_delete_product(self):
    """Test DELETE /products/{id}/"""
    response = self.client.delete(self.url_detail(self.product1.id))
    self.assertEqual(response.status_code, 204)
    self.assertFalse(Product.objects.filter(id=self.product1.id).exists())

    

