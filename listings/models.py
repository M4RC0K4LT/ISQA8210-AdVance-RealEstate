from django.db import models
import os, uuid

from django.forms import ValidationError
from advance_realestate import settings
 
 
# Status of a listing
class ListingStatus(models.Model):
    class Meta:
        verbose_name = 'Listing status'
        verbose_name_plural = 'Listing status'
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

# Neighborhoods of a listing
class ListingNeigborhood(models.Model):
    class Meta:
        verbose_name = 'Listing neighborhood'
        verbose_name_plural = 'Listing neighborhoods'
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
# HomeTypes of a listing
class ListingHomeType(models.Model):
    class Meta:
        verbose_name = 'Listing home type'
        verbose_name_plural = 'Listing home types'
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
# Main Listing-Model 
class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    last_modified = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    status = models.ForeignKey(ListingStatus, on_delete=models.PROTECT)
    hometype = models.ForeignKey(ListingHomeType, on_delete=models.PROTECT)
    neighborhood = models.ForeignKey(ListingNeigborhood, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
 
    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        # If self=featured while saving -> remove existing featured property
        if self.featured:
            try:
                temp = Listing.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Listing.DoesNotExist:
                pass
        super(Listing, self).save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        # If self=featured while deleting -> Remove and select first listing as featured
        if self.featured:
            try:
                temp = Listing.objects.all()[0]
                temp.featured = True
                temp.save()
            except Listing.DoesNotExist:
                pass
            
        # Delete all existing images on filesystem
        images = ListingImages.objects.select_related().filter(listing = self.id).values()
        for image in images:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(image["image"])))
            except Exception as e:
               pass
        super(Listing, self).delete(*args, **kwargs)



# Adjust picture upload path with UUID for unique identifier
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', filename)

def validate_file_extension(value):
    if value.file.content_type != 'application/image':
        raise ValidationError(u'Error message')


# Images belonging to listing
class ListingImages(models.Model):
    class Meta:
        verbose_name = 'Listing images'
        verbose_name_plural = 'Listing images'
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_file_path,null=True,blank=True)