from rest_framework import serializers
from .models import Category, Item, ItemImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('id', 'image', 'is_primary')

class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'category', 'category_name', 
                 'condition', 'location', 'latitude', 'longitude', 
                 'is_available', 'created_at', 'images') 