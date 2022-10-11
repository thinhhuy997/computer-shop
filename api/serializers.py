from rest_framework import serializers
from .models import Category, Product, ImageURL

class CategorySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Category
		fields = ["id", "name", "product_list"]
		depth = 1

class ImageURLSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
	image_urls = serializers.SlugRelatedField(many=True,
        read_only=True,
        slug_field='url')

	class Meta:
		model = Product
		fields = ['id', 'slug', 'categories', 'image_urls', 'name', 'price', 'description_from_crawler', 'created_at', 'updated_at']
		depth = 1
