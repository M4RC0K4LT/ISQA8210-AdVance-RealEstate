from django.contrib import admin

from listings.models import Listing, ListingHomeType, ListingImages, ListingNeigborhood, ListingStatus


# Registering all models for admin page
@admin.register(Listing, ListingStatus, ListingImages, ListingHomeType, ListingNeigborhood)
class ListingAdmin(admin.ModelAdmin):
    pass