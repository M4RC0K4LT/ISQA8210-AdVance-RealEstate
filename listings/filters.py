import django_filters
from .models import Listing
from django_filters.filters import RangeFilter
from .forms import ListingsFilterFormHelper
from .widgets import CustomRangeWidget

# Adjusted range filter for price range of listing
class AllRangeFilter(RangeFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        values = [p.price for p in Listing.objects.all()]
        min_value = int(0)   #int(min(values))
        max_value = int(1000000)   #int(max(values))
        self.extra['widget'] = CustomRangeWidget(attrs={'data-range_min':min_value,'data-range_max':max_value})


# Listings filter containing three required filters (including adjusted RangeFilter)
#  Using ListingsFilterFormHelper for 'crispy'|bootstrap of form
class ListingsFilter(django_filters.FilterSet):
    price = AllRangeFilter()
    class Meta:
        model = Listing
        fields = ['hometype', 'neighborhood', 'price', ]
        form = ListingsFilterFormHelper