from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view()),
    path('products/', views.ProductListView.as_view()),
    path('catalogs/', views.CatalogListView.as_view()),
]
