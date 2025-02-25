from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Budget(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  user_name= models.CharField(max_length=255, blank=True)
  customer = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class BudgetItem(models.Model):
  budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="items")
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveBigIntegerField(default=1)