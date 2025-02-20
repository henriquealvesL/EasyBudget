from django.contrib import admin

from .models import Budget, BudgetItem

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('get_budget_id', 'get_product_name', 'quantity')
    search_fields = ('budget__id', 'product__name')

    def get_budget_id(self, obj):
        return obj.budget.id  

    def get_product_name(self, obj):
        return obj.product.name  

    get_budget_id.short_description = "Budget ID"
    get_product_name.short_description = "Product Name"
