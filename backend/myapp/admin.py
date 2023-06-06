from django.contrib import admin
from .models import Artists, User, Artwork, Address, Order

admin.site.register(Address)
admin.site.register(Artwork)
admin.site.register(Artists)
admin.site.register(Order)
admin.site.register(User)
