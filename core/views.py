from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework_gis.filters import DistanceToPointOrderingFilter

from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from core import models, serializers
from permissions import IsAdminUser
from core import filters as core_filters

User = get_user_model()


class RideViewSet(viewsets.ModelViewSet):
    queryset = models.Ride.objects.all()
    serializer_class = serializers.RideSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_class = core_filters.RideListFilterSet
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        DistanceToPointOrderingFilter,
    ]
    ordering_fields = ['pickup_time']
    distance_ordering_filter_field = 'pickup_location'

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.RideListSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        lat = request.data.get("pickup_latitude")
        lon = request.data.get("pickup_longitude")
        request.data["pickup_location"] = Point(lat, lon, srid=4326)
        print(request.data)
        return super(RideViewSet, self).create(request, *args, **kwargs)

    @action(detail=True)
    def pickup(self, request, pk=None):
        ride = models.Ride.objects.get(pk=pk)
        if ride.status != "en-route":
            raise ValidationError({"details": "Cannot move status to 'pickup'."})
        
        # Update Ride
        ride.status = "pickup"
        ride.pickup_time = timezone.now()
        ride.save()

        # Create RideEvent
        models.RideEvent.objects.create(id_ride=ride, description='Status changed to pickup')
        return Response("picked up")

    @action(detail=True)
    def dropoff(self, request, pk=None):
        ride = models.Ride.objects.get(pk=pk)
        if ride.status != "pickup":
            raise ValidationError({"details": "Cannot move status to 'dropoff'."})
        
        # Update Ride
        ride.status = "dropoff"
        ride.save()

        # Create RideEvent
        models.RideEvent.objects.create(id_ride=ride, description='Status changed to dropoff')
        return Response("dropped off")
