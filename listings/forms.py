from django import forms
from .models import Listing
 
 
class ListingUploadForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'img', 'featured']