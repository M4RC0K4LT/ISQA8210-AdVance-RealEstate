from django.shortcuts import render
from listings.models import Property, Property_Image

# Landing Page
def home_view(request):
    try:
        #Check if any listing is featured
        featured_listing = Property.objects.get(property_feature_status=True)
        images = Property_Image.objects.select_related().filter(property_id = featured_listing)
        image_urls = []
        for image in images:
            image_urls.append(str(image.property_image_location))
    except Property.DoesNotExist:
        featured_listing = None
        image_urls = None
    return render(request, 'home.html', {'listing_featured': featured_listing, 'image_urls' : image_urls})


# AreaInfo Page
def area_view(request):   
    return render(request, 'area-info.html')

# AboutUs Page
def about_view(request):   
    return render(request, 'about-us.html')