from rest_framework import generics
from .models import Product
from .serializer import ProductSerializer

class ProductListView(generics.ListAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

class ProductCreateView(generics.CreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer