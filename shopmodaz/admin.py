from django.contrib import admin
from .models import Product, Category, Subategory, Type, Contact, Wishlist, Benner, ProductDesc

# Register your models here.
admin.site.register(Product)

admin.site.register(ProductDesc)

admin.site.register(Category)

admin.site.register(Subategory)

admin.site.register(Type)

admin.site.register(Contact)

admin.site.register(Wishlist)

admin.site.register(Benner)

