from rest_framework import generics, filters
from rest_framework.response import Response
from .models import Category, Product, Catalog
from .serializers import CategorySerializer, ProductSerializer, CatalogSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {'request': self.request}

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'sku', 'description']

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category', 'subcategory')
        category_slug = self.request.query_params.get('category')
        subcategory_id = self.request.query_params.get('subcategory')
        status = self.request.query_params.get('status')
        featured = self.request.query_params.get('featured')

        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if subcategory_id:
            qs = qs.filter(subcategory_id=subcategory_id)
        if status:
            qs = qs.filter(status=status)
        if featured == 'true':
            qs = qs.filter(is_featured=True)
        return qs

class CatalogListView(generics.ListAPIView):
    queryset = Catalog.objects.filter(is_active=True)
    serializer_class = CatalogSerializer

    def get_serializer_context(self):
        return {'request': self.request}