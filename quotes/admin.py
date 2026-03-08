from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import QuoteRequest

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company', 'email', 'country', 'product_lines_display', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'company', 'email']
    list_editable = ['status']
    readonly_fields = ['full_name', 'company', 'email', 'phone', 'country', 'product_lines', 'message', 'created_at']
    actions = ['export_csv']

    fieldsets = (
        ('Customer', {
            'fields': ('full_name', 'company', 'email', 'phone', 'country')
        }),
        ('Request', {
            'fields': ('product_lines', 'message', 'created_at')
        }),
        ('Internal', {
            'fields': ('status', 'notes')
        }),
    )

    def product_lines_display(self, obj):
        return ', '.join(obj.product_lines) if obj.product_lines else '—'
    product_lines_display.short_description = 'Products'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="quotes_{timezone.now().strftime("%Y%m%d")}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date', 'Name', 'Company', 'Email', 'Phone', 'Country', 'Products', 'Message', 'Status'])
        for q in queryset:
            writer.writerow([
                q.created_at.strftime('%Y-%m-%d %H:%M'),
                q.full_name, q.company, q.email, q.phone, q.country,
                ', '.join(q.product_lines), q.message, q.get_status_display()
            ])
        return response
    export_csv.short_description = 'Export selected to CSV'
