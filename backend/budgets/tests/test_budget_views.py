from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from budgets.models import Budget, BudgetItem
from products.models import Product

class BudgetListViewTestCase(APITestCase):
  def setUp(self):
      """Create test user, products, and budgets"""
      self.user = User.objects.create_user(username="testuser", password="password123")
      self.product1 = Product.objects.create(name="Product 1", price=100.0)
      self.product2 = Product.objects.create(name="Product 2", price=50.0)
      
      self.budget = Budget.objects.create(user=self.user, customer="Customer 1", total_price=0)
      BudgetItem.objects.create(budget=self.budget, product=self.product1, quantity=2)
      BudgetItem.objects.create(budget=self.budget, product=self.product2, quantity=1)

      self.budget.total_price = sum(item.product.price * item.quantity for item in self.budget.items.all())
      self.budget.save()

      self.url = reverse("budget-list")  # /budgets/
      self.url_detail = lambda pk: reverse("budget-detail", kwargs={"pk": pk})  # /budgets/{id}/

  def test_list_budgets(self):
      """Test GET /budgets/"""
      response = self.client.get(self.url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 1)
      self.assertEqual(response.data[0]["customer"], "Customer 1")

  def test_create_budget(self):
      """Test POST /budgets/"""
      self.client.force_login(self.user)
      data = {
          "customer": "New Customer",
          "items": [
              {"product": self.product1.id, "quantity": 1},
              {"product": self.product2.id, "quantity": 2}
          ]
      }
      response = self.client.post(self.url, data, format="json")
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Budget.objects.count(), 2)
      self.assertEqual(BudgetItem.objects.count(), 4)
      self.assertEqual(Budget.objects.last().customer, "New Customer")

  def test_get_budget_detail(self):
      """Test GET /budgets/{id}/"""
      response = self.client.get(self.url_detail(self.budget.id))
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data["customer"], self.budget.customer)

  def test_update_budget(self):
      """Test PUT /budgets/{id}/"""
      budget_item = self.budget.items.first()
      data = {
          "customer": "Updated Customer",
          "items": [
              { "id": budget_item.id,"product": self.product1.id, "quantity": 3}
          ]
      }
      response = self.client.put(self.url_detail(self.budget.id), data, format="json")
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.budget.refresh_from_db()
      self.assertEqual(self.budget.customer, "Updated Customer")
      self.assertEqual(self.budget.items.count(), 1) 
      self.assertEqual(self.budget.items.first().quantity, 3)

  def test_delete_budget(self):
      """Test DELETE /budgets/{id}/"""
      response = self.client.delete(self.url_detail(self.budget.id))
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.assertFalse(Budget.objects.filter(id=self.budget.id).exists()) 
