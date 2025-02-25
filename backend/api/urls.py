from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from budgets.views import BudgetViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'budgets', BudgetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
