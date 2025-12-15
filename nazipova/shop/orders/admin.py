from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'full_name', 'phone', 'status',
        'created_at', 'get_total_cost'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone', 'address']
    inlines = [OrderItemInline]
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_cancelled']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(status='PAID')
    mark_as_paid.short_description = "Пометить как оплаченные"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')
    mark_as_shipped.short_description = "Пометить как отправленные"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
    mark_as_cancelled.short_description = "Пометить как отмененные"