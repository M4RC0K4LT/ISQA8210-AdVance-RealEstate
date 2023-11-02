from django import forms
from .models import Listing, ListingImages
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Field, Layout
from django_filters.fields import RangeField
 
 
class ListingUploadForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'featured', 'status', 'hometype', 'neighborhood', 'price']
        
  
# General multiple file input     
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# General multiple file field
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# Image Upload Form consisting of multiple file field        
class ListingImagesUploadForm(forms.ModelForm):
    image = MultipleFileField()
    class Meta:
        model = ListingImages
        fields = ('image', )
        
        
  
# Form for main filter function in all listings      
class ListingsFilterFormHelper(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'
        layout_fields = []
        for field_name, field in self.fields.items():
            if isinstance(field, RangeField):
                layout_field = Field(field_name, template="forms/fields/range-slider.html")
            else:
                layout_field = Field(field_name)
            layout_fields.append(layout_field)
        layout_fields.append(StrictButton("Submit", name='submit', type='submit', css_class='btn btn-secondary'))
        self.helper.layout = Layout(*layout_fields)
    