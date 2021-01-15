from django.db import models
from django.shortcuts import reverse
from django.conf import settings 

# Create your models here.
CATEGORY_CHOICES = [
    ('AM', 'Amazon'),
    ('FK', 'Flipkart'),
    ('AB', 'AliBaba')
]
COUNTRY_CHOICES = [
    ('india','India'),
]

STATE_CHOICES = [
    ('ncr', 'N.C.R'),
]

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True, default=0.00)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=300)
    slug = models.SlugField()
    description = models.TextField()
    image = models.CharField(max_length=6000, default="https://pbs.twimg.com/profile_images/1023140866255249409/1CJ1vGU4_400x400.jpg")
    

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def get_name(self):
        return f"{self.quantity} of {self.item.title}"
    def get_price(self):
        return f"Rs. {self.item.price}"
    def get_dis(self):
        return f"You Saved {self.item.discount_price}"
    def get_total_price(self):
        return self.quantity * ( self.item.price - self.item.discount_price )


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billingaddress = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank = True, null = True)

    def __str__(self):
        return self.user.username
    def get_final_price(self):
        total = 0 
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total

    

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=300)
    appartment_address = models.CharField(max_length=300)
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=300)
    state = models.CharField(choices=STATE_CHOICES, max_length=300)
    zip_code = models.CharField(max_length=300)
    name_on_card = models.CharField(max_length=300)
    pp_card = models.CharField(max_length=300)
    expiry_date = models.CharField(max_length=300)
    cvv = models.CharField(max_length=300)

    def __str__(self):
        return self.street_address