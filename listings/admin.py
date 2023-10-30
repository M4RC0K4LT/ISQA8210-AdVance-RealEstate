from django.contrib import admin

from listings.models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    pass