import pytest
from budgets.models import Budget, BudgetItem

@pytest.mark.django_db
def test_create_budget(user):
  budget = Budget.objects.create(user=user)
  assert budget.user == user  
  assert budget.items.count() == 0 

@pytest.mark.django_db
def test_create_budget_item(user, product):
  budget = Budget.objects.create(user=user)
  item = BudgetItem.objects.create(budget=budget, product=product, quantity=15)

  assert item.budget == budget
  assert item.product == product
  assert item.quantity == 15
  assert budget.items.count() == 1