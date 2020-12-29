from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=350, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:products_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=350, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'
        ordering = ['date_added']
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cart_item'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


class Order(models.Model):
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')
    email_address = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billing_name = models.CharField(max_length=250, blank=True)
    billing_address1 = models.CharField(max_length=250, blank=True)
    billing_city = models.CharField(max_length=250, blank=True)
    billing_postcode = models.CharField(max_length=250, blank=True)
    billing_country = models.CharField(max_length=250, blank=True)
    shipping_name = models.CharField(max_length=250, blank=True)
    shipping_address1 = models.CharField(max_length=250, blank=True)
    shipping_city = models.CharField(max_length=250, blank=True)
    shipping_postcode = models.CharField(max_length=250, blank=True)
    shipping_country = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'order'
        ordering = ['-created']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product


