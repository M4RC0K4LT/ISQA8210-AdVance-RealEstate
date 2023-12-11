from django.urls import path
from . import views

urlpatterns = [
    path('listings/', views.listings_view, name='listings_viewall'),
    path('listings/upload/', views.listings_upload, name='listings_upload'),
    path('listing/<int:listing_id>', views.listing_detail_view, name='listing_detail'),
    path('listing/delete/<int:listing_id>', views.listing_delete, name='listing_delete'),
     path('listing/<int:listing_id>/change_status/', views.listing_change_status, name='listing_change_status'),
    path('listing/<int:listing_id>/add_as_featured/', views.listing_add_as_featured, name='listing_add_as_featured'),
]
