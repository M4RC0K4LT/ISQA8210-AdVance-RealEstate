from django.shortcuts import render
from listings.models import Listing, ListingImages

# Landing Page
def home_view(request):
    try:
        #Check if any listing is featured
        featured_listing = Listing.objects.get(featured=True)
        images = ListingImages.objects.select_related().filter(listing = featured_listing.id).values()
        image_urls = []
        for image in images:
            image_urls.append(image["image"])
    except Listing.DoesNotExist:
        featured_listing = None
        image_urls = None
    return render(request, 'home.html', {'listing_featured': featured_listing, 'image_urls' : image_urls})


# AreaInfo Page
def area_view(request):   
    return render(request, 'area-info.html')

# AboutUs Page
def about_view(request):   
    return render(request, 'about-us.html')