from dataclasses import field
from django_filters import FilterSet, CharFilter, NumberFilter, OrderingFilter
from .models import Product

class ProductFilter(FilterSet):
    categories = CharFilter(method='filter_category')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('categories', 'min_price', 'max_price')

    def filter_category(self, queryset, name, value):
        categories = value.split(',')
        return queryset.filter(categories__name__in=categories)
    