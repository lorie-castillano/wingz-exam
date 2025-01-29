from django_filters import rest_framework as filters
from core import models


class RideListFilterSet(filters.FilterSet):
    ride_status = filters.BaseInFilter(field_name="status")
    rider_email = filters.BaseInFilter(method="filter_rider_email", field_name="id_rider")

    class Meta:
        model = models.Ride
        fields = []
        exclude = []

    def filter_rider_email(self, queryset, name, value):
        if value:
            return queryset.filter(id_rider__email=value[0])
        return queryset
