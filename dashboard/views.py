from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.utils import timezone
import csv
import cloudinary.uploader
from products.models import Category, Product, Subcategory, Catalog
from quotes.models import QuoteRequest

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/panel/login/')
def dashboard(request):
    stats = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_quotes': QuoteRequest.objects.count(),
        'new_quotes': QuoteRequest.objects.filter(status='new').count(),
        'recent_quotes': QuoteRequest.objects.order_by('-created_at')[:5],
        'products_by_category': Category.objects.annotate(count=Count('products')).filter(is_active=True),
    }
    return render(request, 'dashboard/dashboard.html', stats)

# ── CATEGORIES ──
@login_required(login_url='/panel/login/')
def categories(request):
    cats = Category.objects.all().order_by('order')
    return render(request, 'dashboard/categories.html', {'categories': cats})

@login_required(login_url='/panel/login/')
def category_add(request):
    if request.method == 'POST':
        cat = Category(
            name=request.POST['name'],
            slug=request.POST['slug'],
            description=request.POST['description'],
            product_count=request.POST.get('product_count', 0),
            order=request.POST.get('order', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        if 'hero_image' in request.FILES:
            cat.hero_image = request.FILES['hero_image']
        cat.save()
        subs = request.POST.getlist('subcategories')
        for sub in subs:
            if sub.strip():
                Subcategory.objects.create(category=cat, name=sub.strip())
        messages.success(request, f'Category "{cat.name}" created.')
        return redirect('categories')
    return render(request, 'dashboard/category_form.html', {'action': 'Add'})

@login_required(login_url='/panel/login/')
def category_edit(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.name = request.POST['name']
        cat.slug = request.POST['slug']
        cat.description = request.POST['description']
        cat.product_count = request.POST.get('product_count', 0)
        cat.order = request.POST.get('order', 0)
        cat.is_active = request.POST.get('is_active') == 'on'
        if 'hero_image' in request.FILES:
            cat.hero_image = request.FILES['hero_image']
        cat.save()
        messages.success(request, f'Category "{cat.name}" updated.')
        return redirect('categories')
    return render(request, 'dashboard/category_form.html', {'action': 'Edit', 'category': cat})

@login_required(login_url='/panel/login/')
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    cat.delete()
    messages.success(request, 'Category deleted.')
    return redirect('categories')

# ── PRODUCTS ──
@login_required(login_url='/panel/login/')
def products(request):
    qs = Product.objects.select_related('category', 'subcategory').order_by('category', 'name')
    cat_filter = request.GET.get('category')
    search = request.GET.get('q')
    if cat_filter:
        qs = qs.filter(category__slug=cat_filter)
    if search:
        qs = qs.filter(name__icontains=search)
    return render(request, 'dashboard/products.html', {
        'products': qs,
        'categories': Category.objects.filter(is_active=True),
        'cat_filter': cat_filter,
        'search': search,
    })

@login_required(login_url='/panel/login/')
def product_add(request):
    if request.method == 'POST':
        p = Product(
            name=request.POST['name'],
            sku=request.POST.get('sku', ''),
            category_id=request.POST['category'],
            subcategory_id=request.POST.get('subcategory') or None,
            description=request.POST.get('description', ''),
            grade=request.POST.get('grade', '316L'),
            status=request.POST.get('status', 'in_stock'),
            is_featured=request.POST.get('is_featured') == 'on',
            is_active=request.POST.get('is_active') == 'on',
        )
        if 'image' in request.FILES:
            p.image = request.FILES['image']
        p.save()
        messages.success(request, f'Product "{p.name}" added.')
        return redirect('products')
    return render(request, 'dashboard/product_form.html', {
        'action': 'Add',
        'categories': Category.objects.filter(is_active=True),
    })

@login_required(login_url='/panel/login/')
def product_edit(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        p.name = request.POST['name']
        p.sku = request.POST.get('sku', '')
        p.category_id = request.POST['category']
        p.subcategory_id = request.POST.get('subcategory') or None
        p.description = request.POST.get('description', '')
        p.grade = request.POST.get('grade', '316L')
        p.status = request.POST.get('status', 'in_stock')
        p.is_featured = request.POST.get('is_featured') == 'on'
        p.is_active = request.POST.get('is_active') == 'on'
        if 'image' in request.FILES:
            p.image = request.FILES['image']
        p.save()
        messages.success(request, f'Product "{p.name}" updated.')
        return redirect('products')
    subcategories = Subcategory.objects.filter(category=p.category)
    return render(request, 'dashboard/product_form.html', {
        'action': 'Edit', 'product': p,
        'categories': Category.objects.filter(is_active=True),
        'subcategories': subcategories,
    })

@login_required(login_url='/panel/login/')
def product_delete(request, pk):
    p = get_object_or_404(Product, pk=pk)
    p.delete()
    messages.success(request, 'Product deleted.')
    return redirect('products')

# ── QUOTES ──
@login_required(login_url='/panel/login/')
def quotes(request):
    qs = QuoteRequest.objects.order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'dashboard/quotes.html', {
        'quotes': qs,
        'status_filter': status_filter,
        'counts': {s[0]: QuoteRequest.objects.filter(status=s[0]).count() for s in QuoteRequest.STATUS_CHOICES},
    })

@login_required(login_url='/panel/login/')
def quote_detail(request, pk):
    quote = get_object_or_404(QuoteRequest, pk=pk)
    return render(request, 'dashboard/quote_detail.html', {'quote': quote})

@login_required(login_url='/panel/login/')
def quote_status(request, pk):
    if request.method == 'POST':
        quote = get_object_or_404(QuoteRequest, pk=pk)
        quote.status = request.POST.get('status')
        quote.notes = request.POST.get('notes', '')
        quote.save()
        messages.success(request, 'Quote updated.')
        return redirect('quote_detail', pk=pk)
    return redirect('quotes')

@login_required(login_url='/panel/login/')
def quotes_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="quotes_{timezone.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Name', 'Company', 'Email', 'Phone', 'Country', 'Products', 'Message', 'Status'])
    for q in QuoteRequest.objects.all().order_by('-created_at'):
        writer.writerow([q.created_at.strftime('%Y-%m-%d'), q.full_name, q.company, q.email, q.phone, q.country, ', '.join(q.product_lines), q.message, q.get_status_display()])
    return response

# ── CATALOGS ──
@login_required(login_url='/panel/login/')
def catalogs(request):
    return render(request, 'dashboard/catalogs.html', {'catalogs': Catalog.objects.all()})

@login_required(login_url='/panel/login/')
def catalog_add(request):
    if request.method == 'POST':
        c = Catalog(
            name=request.POST['name'],
            category_id=request.POST.get('category') or None,
            page_count=request.POST.get('page_count', 0),
            product_count=request.POST.get('product_count', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        if 'cover_image' in request.FILES:
            c.cover_image = request.FILES['cover_image']
        if 'pdf_file' in request.FILES:
            result = cloudinary.uploader.upload(
                request.FILES['pdf_file'],
                resource_type='raw',
                folder='catalogs/pdfs',
            )
            c.pdf_file = result['secure_url']
        c.save()
        messages.success(request, f'Catalog "{c.name}" added.')
        return redirect('catalogs')
    return render(request, 'dashboard/catalog_form.html', {
        'action': 'Add',
        'categories': Category.objects.filter(is_active=True),
    })

@login_required(login_url='/panel/login/')
def catalog_edit(request, pk):
    c = get_object_or_404(Catalog, pk=pk)
    if request.method == 'POST':
        c.name = request.POST['name']
        c.category_id = request.POST.get('category') or None
        c.page_count = request.POST.get('page_count', 0)
        c.product_count = request.POST.get('product_count', 0)
        c.is_active = request.POST.get('is_active') == 'on'
        if 'cover_image' in request.FILES:
            c.cover_image = request.FILES['cover_image']
        if 'pdf_file' in request.FILES:
            result = cloudinary.uploader.upload(
                request.FILES['pdf_file'],
                resource_type='raw',
                folder='catalogs/pdfs',
            )
            c.pdf_file = result['secure_url']
        c.save()
        messages.success(request, f'Catalog "{c.name}" updated.')
        return redirect('catalogs')
    return render(request, 'dashboard/catalog_form.html', {'action': 'Edit', 'catalog': c, 'categories': Category.objects.filter(is_active=True)})

@login_required(login_url='/panel/login/')
def catalog_delete(request, pk):
    c = get_object_or_404(Catalog, pk=pk)
    c.delete()
    messages.success(request, 'Catalog deleted.')
    return redirect('catalogs')

# AJAX - get subcategories for a category
def get_subcategories(request, category_id):
    subs = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subs), safe=False)

