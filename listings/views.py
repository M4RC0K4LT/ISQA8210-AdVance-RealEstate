from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import ListingImagesUploadForm, ListingUploadForm
from .models import Listing, ListingImages
from .filters import ListingsFilter


# All Listings view including filter option
def listings_view(request):   
    listings = Listing.objects.all()
    filtered_listings = ListingsFilter(request.GET, queryset=Listing.objects.all())
    
    #TODO: Filter tracking / analysis
    #print(request.GET.dict())
    #print(filtered_listings)
    
    # Collect all image links for listings to hand them over to template
    listings_images = {}
    for listing in listings:
        images_to_listing = ListingImages.objects.select_related().filter(listing = listing.id).values()
        image_urls = []
        for image in images_to_listing:
            image_urls.append(image["image"])
        listings_images.update({listing.id : image_urls})
    return render(request, 'listings_all.html', {'listings': filtered_listings, "images_all" : listings_images})


# Detailed listing view
def listing_detail_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)#
    images = ListingImages.objects.select_related().filter(listing = listing.id).values()
    image_urls = []
    for image in images:
        image_urls.append(image["image"])
    return render(request, 'listing_detail.html', context={'listing': listing, 'image_urls': image_urls}) 


# Upload of new listing
@login_required
def listings_upload(request):   
    if request.method == 'POST':   
        #Two forms combined: 
        listing_form = ListingUploadForm(request.POST)
        image_form = ListingImagesUploadForm(request.POST, request.FILES)
        
        if listing_form.is_valid() and image_form.is_valid():
            lis = listing_form.save()
            #Save every uploaded image in ListingImage Model
            for img in request.FILES.getlist("image"):
                images = ListingImages(listing=lis, image=img)
                images.save()
            return HttpResponseRedirect('/listing/' + str(lis.id))            
    else:
        listing_form = ListingUploadForm()
        image_form = ListingImagesUploadForm()
    return render(request, 'upload_listing.html', {'listing_form': listing_form, 'image_form': image_form})
 

# Delete listing
@login_required
def listing_delete(request, listing_id):
  listing = Listing.objects.get(id=listing_id)
  listing.delete()
  return HttpResponseRedirect("/listings")


# Feature listing
@login_required
def listing_feature(request, listing_id):
  listing = Listing.objects.get(id=listing_id)
  if listing.featured == True:
      listing.featured = False
  else:
      listing.featured = True
  listing.save()
  return HttpResponseRedirect("/listing/" + str(listing_id))


# Change status of listing
@login_required
def listing_status(request, listing_id, status_id):
  listing = Listing.objects.get(id=listing_id)
  listing.status_id = status_id
  listing.save()
  return HttpResponseRedirect("/listing/" + str(listing_id))