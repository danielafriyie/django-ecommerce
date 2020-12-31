from django.urls import path
from .views import (
    home, product_page, add_cart, cart_detail, cart_remove, cart_remove_product, thanks_page,
    signup_view, signin_view, signout_view, order_history, view_order, search
)

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('category/<slug:category_slug>', home, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', product_page, name='product_detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('cart/remove-product/<int:product_id>', cart_remove_product, name='cart_remove_product'),
    path('thank-you/<int:order_id>', thanks_page, name='thanks_page'),
    path('account/create/', signup_view, name='signup'),
    path('account/signin/', signin_view, name='signin'),
    path('acount/signout/', signout_view, name='signout'),
    path('order-history/', order_history, name='order_history'),
    path('order/<int:order_id>/', view_order, name='order_detail'),
    path('search/', search, name='search')
]
