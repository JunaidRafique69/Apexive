# serializers.py

from rest_framework import serializers
from .models import Product, Manufacturer, Category

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    categories = CategorySerializer(many=True)
    
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        

    def create(self, validated_data):
        manufacturer_data = validated_data.pop('manufacturer')
        manufacturer = Manufacturer.objects.create(**manufacturer_data)

        categories_data = validated_data.pop('categories')
        categories = [Category.objects.create(**category_data) for category_data in categories_data]

        product = Product.objects.create(manufacturer=manufacturer, **validated_data)
        product.categories.set(categories)

        return product

    def update(self, instance, validated_data):
        manufacturer_data = validated_data.pop('manufacturer', {})
        instance.manufacturer.name = manufacturer_data.get('name', instance.manufacturer.name)
        instance.manufacturer.location = manufacturer_data.get('location', instance.manufacturer.location)
        instance.manufacturer.save()

        categories_data = validated_data.pop('categories', [])
        for i, category_data in enumerate(categories_data):
            category_instance = instance.categories.all()[i]
            category_instance.name = category_data.get('name', category_instance.name)
            category_instance.save()

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        return instance

    def get_discounted_price(self, obj):
        return obj.price * 0.9

class DynamicFieldProductSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.SerializerMethodField()
    is_expensive = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_manufacturer_name(self, obj):
        return obj.manufacturer.name if obj.manufacturer else None

    def get_is_expensive(self, obj):
        return obj.price > 100
