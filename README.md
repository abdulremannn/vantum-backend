# Vantum Surgical — Django Backend

## Local Setup (PyCharm)

1. Open this folder in PyCharm
2. PyCharm will detect requirements.txt — click "Install requirements"
3. Open terminal in PyCharm and run:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. Go to http://localhost:8000/admin — log in with your superuser

## API Endpoints

- GET  /api/categories/           — all categories
- GET  /api/categories/<slug>/    — single category with subcategories
- GET  /api/products/             — all products (filter: ?category=surgical&subcategory=1)
- GET  /api/catalogs/             — all catalogs
- POST /api/quotes/               — submit quote request

## Deploy to Railway

See deployment guide below.
