from django.shortcuts import redirect, render
from advance_realestate.forms import ContactForm
from listings.models import Property, Property_Image
from django.conf import settings
from django.core.mail import send_mail

# Landing Page
def home_view(request):
    try:
        # Check if any listing is featured
        featured_listing = Property.objects.get(property_feature_status=True)
        featured_listing_id = featured_listing.id  # Get the ID of the featured listing to redirect to listing detail page
        images = Property_Image.objects.select_related().filter(property_id=featured_listing)
        image_urls = [str(image.property_image_location) for image in images]
    except Property.DoesNotExist:
        # Handle the case when no featured listing is found
        featured_listing = None
        featured_listing_id = None
        image_urls = None

    # Render the 'home.html' template with the context data
    return render(request, 'home.html', {
        'listing_featured': featured_listing,
        'featured_listing_id': featured_listing_id,
        'image_urls': image_urls
    })

# AreaInfo Page
def area_view(request):   
    return render(request, 'area-info.html')

# AboutUs Page
def about_view(request):
    success = None
    subject = 'CONTACT FORM: '
    message = 'New message from: '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["marco@kaltenstadler.net",]
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact_name = request.POST.get("name")
                contact_mail = request.POST.get("email")
                contact_message = request.POST.get("message")
                subject = subject + str(contact_name) + str(contact_mail)
                message = message + str(contact_name) + "    " + str(contact_mail) + "    " + str(contact_message)
                send_mail(subject, message, email_from, recipient_list)  
                success = True
            except Exception as e:
                print(e)
                success = False
    else:
        form = ContactForm()
    return render(request, 'about-us.html', {'form': form, 'alert': success})