from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

import stripe

from .models import Category, Product, Cart, CartItem, Order, OrderItem


def home(request, category_slug=None):
    category_page = None
    # products = None

    if category_slug is not None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)

    return render(request, 'store/home.html', {'category': category_page, 'products': products})


def product_page(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'store/product.html', {'product': product})


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product, cart=cart, quantity=1
        )
        cart_item.save()
    return redirect('store:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'G-Store - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billing_name = request.POST['stripeBillingName']
            billing_address1 = request.POST['stripeBillingAddressLine1']
            billing_city = request.POST['stripeBillingAddressCity']
            billing_postcode = request.POST['stripeBillingAddressZip']
            billing_country = request.POST['stripeBillingAddressCountryCode']
            shipping_name = request.POST['stripeShippingName']
            shipping_address1 = request.POST['stripeShippingAddressLine1']
            shipping_city = request.POST['stripeShippingAddressCity']
            shipping_postcode = request.POST['stripeShippingAddressZip']
            shipping_country = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )
            order_details = Order.objects.create(
                token=token,
                total=total,
                email_address=email,
                billing_name=billing_name,
                billing_address1=billing_address1,
                billing_city=billing_city,
                billing_postcode=billing_postcode,
                billing_country=billing_country,
                shipping_name=shipping_name,
                shipping_address1=shipping_address1,
                shipping_city=shipping_city,
                shipping_postcode=shipping_postcode,
                shipping_country=shipping_country
            )
            order_details.save()

            for order_item in cart_items:
                OrderItem.objects.create(
                    product=order_item.product.name,
                    quantity=order_item.quantity,
                    price=order_item.product.price,
                    order=order_details
                )
                products = Product.objects.get(pk=order_item.product.pk)
                products.stock = int(order_item.product.stock - order_item.quantity)
                products.save()
                order_item.delete()

                print('the order has been created')
            return redirect('store:thanks_page', order_details.pk)

        except Exception as e:
            return False, e

    context = {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'data_key': data_key,
        'stripe_total': stripe_total,
        'description': description
    }
    return render(request, 'store/cart.html', context)


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('store:cart_detail')


def cart_remove_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('store:cart_detail')


def thanks_page(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, pk=order_id)
    return render(request, 'store/thank_you.html', {'customer_order': customer_order})
