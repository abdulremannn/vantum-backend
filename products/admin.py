from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Subcategory, Product, Catalog

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 3
    fields = ['name', 'order']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'order', 'is_active', 'image_preview']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubcategoryInline]

    def image_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px"/>', obj.hero_image.url)
        return '—'
    image_preview.short_description = 'Photo'

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'subcategory', 'grade', 'status', 'is_featured', 'is_active', 'image_preview']
    list_filter = ['category', 'grade', 'status', 'is_featured', 'is_active']
    list_editable = ['status', 'is_featured', 'is_active']
    search_fields = ['name', 'sku', 'description']
    autocomplete_fields = ['category', 'subcategory']
    readonly_fields = ['image_preview_large']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'sku', 'category', 'subcategory', 'description')
        }),
        ('Specifications', {
            'fields': ('grade', 'status')
        }),
        ('Photo', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px"/>', obj.image.url)
        return '—'
    image_preview.short_description = 'Photo'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px"/>', obj.image.url)
        return 'No photo yet'
    image_preview_large.short_description = 'Preview'

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'page_count', 'product_count', 'is_active', 'updated_at']
    list_editable = ['is_active']