from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import Budget
from .serializer import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
  queryset = Budget.objects.all()
  serializer_class = BudgetSerializer

  @action(detail=True, methods=['get'])
  def generate_budget_pdf(self, request, pk=None):
    budget = get_object_or_404(Budget, pk=pk)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Orçamento #{budget.id}")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Cliente: {budget.customer}")
    p.drawString(50, height - 100, f"Total: R$ {budget.total_price}")

    y = height - 140
    for item in budget.items.all():
        p.drawString(50, y, f"Produto: {item.product.name} | Quantidade: {item.quantity} | Preço Unitário: R$ {item.product.price}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="budget_{budget.id}.pdf"'
    return response
