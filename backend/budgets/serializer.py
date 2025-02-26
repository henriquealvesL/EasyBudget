from rest_framework import serializers
from django.db.models import F, Sum
from .models import Budget, BudgetItem
from products.models import Product

class BudgetItemSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(required=False)
  product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

  class Meta:
    model = BudgetItem
    fields = ['id', 'product', 'quantity']

class BudgetSerializer(serializers.ModelSerializer):
  items = BudgetItemSerializer(many=True)

  class Meta:
    model = Budget
    fields = '__all__'

  def create(self, validated_data):
    items_data = validated_data.pop('items', [])
    items_to_create = []
    request = self.context.get('request')

    budget = Budget.objects.create(user=request.user, user_name=request.user.username ,**validated_data)
    
    for item in items_data:
      items_to_create.append(BudgetItem(budget=budget, **item))
    
    BudgetItem.objects.bulk_create(items_to_create)

    total_price = budget.items.annotate(
      item_price=F('product__price') * F('quantity')
    ).aggregate(total=Sum('item_price'))['total'] or 0

    budget.total_price = total_price
    budget.save(update_fields=['total_price'])
    return budget
  
  def update(self, instance, validated_data):
    items_data = validated_data.pop('items', None)
    for attr, value in validated_data.items():
            setattr(instance, attr, value)

    if items_data is not None:
      existing_items = {item.id: item for item in instance.items.all()}
      sent_items_id = set()
      items_to_update = []
      items_to_create = []

      for item_data in items_data:
          item_id = item_data.get("id")
          if item_id and item_id in existing_items:
              item = existing_items[item_id]
              setattr(item, 'quantity', item_data['quantity'])
              items_to_update.append(item)
              sent_items_id.add(item_id)
          else:
              items_to_create.append(BudgetItem(budget=instance, **item_data))

      if items_to_create:
        new_items = BudgetItem.objects.bulk_create(items_to_create)
        sent_items_id.update([item.product.id for item in new_items])
      
      if items_to_update:
        BudgetItem.objects.bulk_update(items_to_update, ['quantity', 'product'])

      items_to_delete = [item_id for item_id in existing_items.keys() if item_id not in sent_items_id]
      if items_to_delete:
         BudgetItem.objects.filter(budget=instance, id__in=items_to_delete).delete()
      

      total_price = instance.items.annotate(
        item_price=F('product__price') * F('quantity')
      ).aggregate(total=Sum('item_price'))['total'] or 0
      
      instance.total_price = total_price
      instance.save()
      
    return instance
