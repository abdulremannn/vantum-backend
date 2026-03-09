from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    hero_image = models.ImageField(upload_to='categories/', blank=True, null=True, storage=MediaCloudinaryStorage())
    product_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f'{self.category.name} → {self.name}'


class Product(models.Model):
    GRADE_CHOICES = [
        ('316L', 'Grade 316L SS'),
        ('304', 'Grade 304 SS'),
        ('titanium', 'Titanium'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('made_to_order', 'Made to Order'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default='316L')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    image = models.ImageField(upload_to='products/', blank=True, null=True, storage=MediaCloudinaryStorage())
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.sku})'


class Catalog(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    cover_image = models.ImageField(upload_to='catalogs/covers/', storage=MediaCloudinaryStorage())
    pdf_file = models.URLField(max_length=500, blank=True, null=True)
    page_count = models.PositiveIntegerField(default=0)
    product_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
