from rest_framework import serializers
from .models import MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

# use serializers.HyperlinkedModelSerializer for hyperlinks cleaner code
class MenuItemSerializer(serializers.ModelSerializer):
    #category = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    #path('category/<int:pk>',views.category_detail, name='category-detail')
    #category = serializers.HyperlinkedRelatedField(
    #    queryset = Category.objects.all(),
    #    view_name='category-detail'
    #)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory', 'category', 'category_id']

        #extra_kwargs = {"price": {"min_value": 2},
        #   "inventory": {"min_value": 0}
        #}

    #def create(self, validated_data):
    #    category_data = validated_data.pop('category')
    #    category, created = Category.objects.get_or_create(**category_data)
    #    menu_item = MenuItem.objects.create(category=category, **validated_data)
    #    return menu_item