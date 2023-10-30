from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Listing
from .forms import ListingUploadForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def listings_view(request):   
    listings = Listing.objects.all()
    return render(request, 'listings_all.html', {'listings_all': listings})

def listing_detail_view(request, listing_id):  
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listing_detail.html', context={'listing': listing}) 

@login_required
def listings_upload(request):

    if request.method == 'POST':
        form = ListingUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')        
    else:
        form = ListingUploadForm()    
    return render(request, 'upload_listing.html', {'form': form})
 
 
def upload_success(request):
    return HttpResponse('successfully uploaded')

@login_required
def listing_delete(request, listing_id):
  listing = Listing.objects.get(id=listing_id)
  listing.delete()
  return HttpResponseRedirect("/listings")