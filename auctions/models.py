from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.IntegerField(max_length=11)

    def __str__(self):
        return f"{self.first_name}"
    
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
class Items(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="bag")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image =models.ImageField(upload_to='images/', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='bags', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    sold_to = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="new_owner")

    def __str__(self):
        return f"{self.created_by.username}: {self.name}"
    
class Listings(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image =models.ImageField(upload_to='images/', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    sold_to = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="new_malik")

    def __str__(self):
        return f"{self.created_by.username}: {self.name}"
    
class Bids(models.Model):
    product = models.CharField(max_length=265, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bids = models.DecimalField(default=0, null=True,max_digits=10, decimal_places=2)

    class Meta:
        get_latest_by = 'bids'

    def __str__(self):
        return f"{self.bidder}:{self.product}: {self.bids}"
    
class Watchlist(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers")
    products = models.ForeignKey(Items,on_delete=models.CASCADE, related_name="mera_saman", null=True)

    def __str__(self):
        return  f"{self.User}: {self.products.name}"
    

class Comments(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="charcha", null=True)
    product = models.ForeignKey(Items, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=256)
    comment_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.User}: {self.product.name}"



