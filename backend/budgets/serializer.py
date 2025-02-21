from rest_framework import serializers
from .models import Budget, BudgetItem

class BudgetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Budget
    field = '__all__'

class BudgetItemSerializer(serializers.ModelSerializer):
  class Meta:
    model: BudgetItem
    field = '__all__'