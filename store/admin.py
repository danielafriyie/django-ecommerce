from django.contrib import admin
from .models import Category, Product, Cart, CartItem, OrderItem, Order, Review


@admin.register(Category)
class CatetoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product', {'fields': ['product']}),
        ('Quantity', {'fields': ['quantity']}),
        ('Price', {'fields': ['price']})
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billing_name', 'email_address', 'created']
    list_display_links = ['id', 'billing_name']
    search_fields = ['id', 'billing_name', 'email_address']
    readonly_fields = [
        'id', 'token', 'total', 'email_address', 'created', 'billing_name', 'billing_address1', 'billing_city',
        'billing_postcode', 'billing_country', 'shipping_name', 'shipping_address1', 'shipping_city',
        'shipping_postcode', 'shipping_country',
    ]
    fieldsets = [
        ('ORDER INFORMATION', {'fields': ['id', 'token', 'total', 'created']}),
        ('BILLING INFORMATION', {'fields': [
            'billing_name', 'billing_address1', 'billing_city', 'billing_postcode', 'billing_country', 'email_address'
        ]}),
        ('SHIPPING INFORMATION', {'fields': [
            'shipping_name', 'shipping_address1', 'shipping_city', 'shipping_postcode', 'shipping_country'
        ]})
    ]
    inlines = [OrderItemAdmin]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
