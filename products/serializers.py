from rest_framework import serializers
from .models import Category, Subcategory, Product, Catalog

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    hero_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'hero_image_url', 'product_count', 'subcategories']

    def get_hero_image_url(self, obj):
        request = self.context.get('request')
        if obj.hero_image and request:
            return request.build_absolute_uri(obj.hero_image.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'description', 'grade', 'grade_display',
                  'status', 'status_display', 'image_url', 'category_name',
                  'category_slug', 'subcategory_name', 'is_featured']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class CatalogSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Catalog
        fields = ['id', 'name', 'category_name', 'cover_image_url', 'pdf_url', 'page_count', 'product_count']

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_pdf_url(self, obj):
        if obj.pdf_file:
            if str(obj.pdf_file).startswith('http'):
                return str(obj.pdf_file)
            return f'https://res.cloudinary.com/dsn7lwzh0/raw/upload/{obj.pdf_file}'
        return None