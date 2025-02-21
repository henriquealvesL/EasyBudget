from rest_framework import serializers
from .models import Budget, BudgetItem

class BudgetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Budget
    fields = '__all__'

class BudgetItemSerializer(serializers.ModelSerializer):
  class Meta:
    model: BudgetItem
    fields = '__all__'