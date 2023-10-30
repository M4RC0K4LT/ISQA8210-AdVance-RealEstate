from django.urls import include, path
from . import views

urlpatterns = [
    path('listings/', views.listings_view, name='listings_viewall'),
    path('listings/upload/', views.listings_upload, name='listings_upload'),
    path('listings/success/', views.upload_success, name='success'),
    path('listing/<int:listing_id>', views.listing_detail_view, name='listing_detail'),
    path('listing/delete/<int:listing_id>', views.listing_delete, name='listing_delete'),
]