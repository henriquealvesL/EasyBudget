from rest_framework import viewsets
from .models import Budget
from .serializer import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
  queryset = Budget.objects.all()
  serializer_class = BudgetSerializer
    