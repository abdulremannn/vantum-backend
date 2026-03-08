from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views as dv

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom dashboard
    path('panel/', dv.dashboard, name='dashboard'),
    path('panel/login/', dv.login_view, name='login'),
    path('panel/logout/', dv.logout_view, name='logout'),

    path('panel/categories/', dv.categories, name='categories'),
    path('panel/categories/add/', dv.category_add, name='category_add'),
    path('panel/categories/<int:pk>/edit/', dv.category_edit, name='category_edit'),
    path('panel/categories/<int:pk>/delete/', dv.category_delete, name='category_delete'),

    path('panel/products/', dv.products, name='products'),
    path('panel/products/add/', dv.product_add, name='product_add'),
    path('panel/products/<int:pk>/edit/', dv.product_edit, name='product_edit'),
    path('panel/products/<int:pk>/delete/', dv.product_delete, name='product_delete'),

    path('panel/quotes/', dv.quotes, name='quotes'),
    path('panel/quotes/export/', dv.quotes_export, name='quotes_export'),
    path('panel/quotes/<int:pk>/', dv.quote_detail, name='quote_detail'),
    path('panel/quotes/<int:pk>/status/', dv.quote_status, name='quote_status'),

    path('panel/catalogs/', dv.catalogs, name='catalogs'),
    path('panel/catalogs/add/', dv.catalog_add, name='catalog_add'),
    path('panel/catalogs/<int:pk>/edit/', dv.catalog_edit, name='catalog_edit'),
    path('panel/catalogs/<int:pk>/delete/', dv.catalog_delete, name='catalog_delete'),

    path('panel/subs/<int:category_id>/', dv.get_subcategories),

    # API
    path('api/', include('products.urls')),
    path('api/', include('quotes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
