from django.contrib import admin

from .models import User, Profile, Category, Listings, Bids, Watchlist, Items, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(Items)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(Comments)