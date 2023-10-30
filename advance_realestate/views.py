from django.shortcuts import get_object_or_404, render
from listings.models import Listing

def home_view(request): 
    try:
        featured_listing = Listing.objects.get(featured=True)
    except Listing.DoesNotExist:
        featured_listing = None
    
    return render(request, 'home.html', {'listing_featured': featured_listing})