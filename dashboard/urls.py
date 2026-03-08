from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Products
    path('products/', views.products, name='products'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Quotes
    path('quotes/', views.quotes, name='quotes'),
    path('quotes/<int:pk>/', views.quote_detail, name='quote_detail'),
    path('quotes/<int:pk>/status/', views.quote_status, name='quote_status'),
    path('quotes/export/', views.quotes_export, name='quotes_export'),

    # Catalogs
    path('catalogs/', views.catalogs, name='catalogs'),
    path('catalogs/add/', views.catalog_add, name='catalog_add'),
    path('catalogs/<int:pk>/edit/', views.catalog_edit, name='catalog_edit'),
    path('catalogs/<int:pk>/delete/', views.catalog_delete, name='catalog_delete'),
]
