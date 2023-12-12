from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .filters import ListingsFilter
from .forms import AddressUploadForm, ListingImagesUploadForm, ListingUploadForm
from .models import Property, Property_Address, Property_Image, Property_Status, Search_Filter
from django.utils import timezone

from django.template.loader import get_template
from xhtml2pdf import pisa

def listings_view(request):
    listings = Property.objects.all()
    filtered_listings = ListingsFilter(request.GET, queryset=Property.objects.all())

    if request.method == 'GET' and filtered_listings.form.is_valid():
        # Extract the selected values from the ListingsFilter form
        property_price_range = filtered_listings.form.cleaned_data.get('property_price_range')
        property_type = filtered_listings.form.cleaned_data.get('property_type')
        property_neighborhood = filtered_listings.form.cleaned_data.get('property_neighborhood')

        # Check if a Search_Filter instance already exists with the same values
        existing_filter = Search_Filter.objects.filter(
            property_price_range=property_price_range,
            property_type=property_type,
            property_neighborhood=property_neighborhood,
        ).first()

        # If exists, update; otherwise, create a new instance
        if existing_filter:
            existing_filter.property_filter_date = timezone.now()  # Update the timestamp if needed
            existing_filter.save()
        else:
            filter_instance = Search_Filter(
                property_price_range=property_price_range,
                property_type=property_type,
                property_neighborhood=property_neighborhood,
            )
            filter_instance.save()

    listings_images = {}
    for listing in listings:
        images_to_listing = Property_Image.objects.select_related().filter(property_id=listing.id)
        image_urls = [str(image.property_image_location) for image in images_to_listing]
        listings_images.update({listing.id: image_urls})

    return render(request, 'listings_all.html', {'listings': filtered_listings, "images_all": listings_images})


# Detailed listing view
def listing_detail_view(request, listing_id):
    listing = get_object_or_404(Property, id=listing_id)
    images = Property_Image.objects.select_related().filter(property_id = listing.id).values()
    image_urls = []
    for image in images:
        image_urls.append(image["property_image_location"])
    return render(request, 'listing_detail.html', context={'listing': listing, 'image_urls': image_urls}) 


# Upload of new listing
@login_required
def listings_upload(request):   
    if request.method == 'POST':   
        #Two forms combined: 
        address_form = AddressUploadForm(request.POST)
        image_form = ListingImagesUploadForm(request.POST, request.FILES)
        listing_form = ListingUploadForm(request.POST)
        
        if listing_form.is_valid() and image_form.is_valid() and address_form.is_valid():
            add = address_form.save()
            lis = listing_form.save(commit=False)
            lis.property_address = add
            lis.save()
            #Save every uploaded image in ListingImage Model
            for img in request.FILES.getlist("image"):
                images = Property_Image(property_id=lis.id, property_image_location=img)
                images.save()
            return HttpResponseRedirect('/listing/' + str(lis.id))            
    else:
        listing_form = ListingUploadForm()
        image_form = ListingImagesUploadForm()
        address_form = AddressUploadForm()
    return render(request, 'upload_listing.html', {'listing_form': listing_form, 'image_form': image_form, 'address_form': address_form})
 

# Delete listing
@login_required
def listing_delete(request, listing_id):
  listing = Property.objects.get(id=listing_id)
  listing.delete()
  address = Property_Address.objects.get(id=listing.property_address_id)
  address.delete()
  return HttpResponseRedirect("/listings")


# Feature listing
@login_required
def listing_feature(request, listing_id):
  listing = Property.objects.get(id=listing_id)
  if listing.property_feature_status == True:
      listing.property_feature_status = False
  else:
      listing.property_feature_status = True
  listing.save()
  return HttpResponseRedirect("/listing/" + str(listing_id))


# Change status of listing
@login_required
def listing_status(request, listing_id, status_id):
  listing = Property.objects.get(id=listing_id)
  listing.property_status_id = status_id
  listing.save()
  return HttpResponseRedirect("/listing/" + str(listing_id))





@login_required
def listing_change_status(request, listing_id):
    listing = get_object_or_404(Property, id=listing_id)

    # Get all status options from the Property_Status model
    status_options = list(Property_Status.objects.values_list('property_status_name', flat=True))

    current_status = listing.property_status.property_status_name
    next_index = (status_options.index(current_status) + 1) % len(status_options)
    new_status = status_options[next_index]

    # Update the listing status
    listing.property_status = Property_Status.objects.get(property_status_name=new_status)
    listing.save()

    # Return a JSON response (you can customize the response as needed)
    return JsonResponse({'status': 'success', 'message': 'Status changed successfully'})



@login_required
def listing_add_as_featured(request, listing_id):
    listing = get_object_or_404(Property, id=listing_id)

    # Set the property_feature_status to True
    listing.property_feature_status = True
    listing.save()

    # Return a JSON response (you can customize the response as needed)
    return JsonResponse({'status': 'success', 'message': 'Added as featured successfully'})

def generate_pdf_report(request):
    # Fetch the search history from the database
    search_history = Search_Filter.objects.all()

    # Render the HTML template with the search history
    template_path = 'pdf_report_template.html'  # Create this template
    template = get_template(template_path)
    context = {'search_history': search_history}
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="search_history_report.pdf"'

    # Generate PDF from the HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check if PDF generation was successful
    if pisa_status.err:
        return HttpResponse('Error during PDF generation.')

    return response
