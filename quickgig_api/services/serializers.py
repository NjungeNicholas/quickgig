from rest_framework import serializers
from .models import Service, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() # to show category name instead of id
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'category']