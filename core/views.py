from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework_gis.filters import DistanceToPointOrderingFilter

from rest_framework import mixins, permissions, viewsets, filters, status
from rest_framework.response import Response
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
    ordering_fields = ["pickup_time"]
    distance_ordering_filter_field = "pickup_location"

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.RideListSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        request.data["pickup_location"] = Point(
            request.data.get("pickup_latitude"),
            request.data.get("pickup_longitude"),
            srid=4326,
        )
        return super(RideViewSet, self).create(request, *args, **kwargs)

    def update(self, request, pk=None, **kwargs):
        request.data["pickup_location"] = Point(
            request.data.get("pickup_latitude"),
            request.data.get("pickup_longitude"),
            srid=4326,
        )
        return super(RideViewSet, self).update(request, pk, **kwargs)


class RideEventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.RideEvent.objects.all()
    serializer_class = serializers.RideEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend]

    def destroy(self, request, pk=None, **kwargs):
        instance = self.get_object()

        dropoff_event = models.RideEvent.objects.filter(
            id_ride=instance.id_ride, description="Status changed to dropoff"
        )
        if instance.description == "Status changed to pickup":
            if dropoff_event.exists():
                dropoff_event.delete()

            instance.id_ride.status = "en-route"
            instance.id_ride.save()

        elif instance.description == "Status changed to dropoff":
            instance.id_ride.status = "pickup"
            instance.id_ride.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
