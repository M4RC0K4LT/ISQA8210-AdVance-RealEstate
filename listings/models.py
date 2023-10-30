from django.db import models
 
class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    last_modified = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    img = models.ImageField(upload_to="images/")
 
    def __str__(self):
        return self.title
    
    #Remove existing featured property
    def save(self, *args, **kwargs):
        if self.featured:
            try:
                temp = Listing.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Listing.DoesNotExist:
                pass
        super(Listing, self).save(*args, **kwargs)
        
        
        #Remove existing featured property
    def delete(self, *args, **kwargs):
        if self.featured:
            try:
                temp = Listing.objects.all()[0]
                temp.featured = True
                temp.save()
            except Listing.DoesNotExist:
                pass
        super(Listing, self).delete(*args, **kwargs)
