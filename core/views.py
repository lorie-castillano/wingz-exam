from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core import models, serializers
from permissions import IsAdminUser

User = get_user_model()


class RideViewSet(viewsets.ModelViewSet):
    queryset = models.Ride.objects.all()
    serializer_class = serializers.RideSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    # def get_serializer_class(self):
    #     if self.action in ["list", "retrieve"]:
    #         return serializers.RideListSerializer
    #     return self.serializer_class

    @action(detail=True)
    def pickup(self, request, pk=None):
        ride = models.Ride.objects.get(pk=pk)
        if ride.status != "en-route":
            ValidationError({"details": "Cannot move status to 'pickup'."})
        
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
            ValidationError({"details": "Cannot move status to 'dropoff'."})
        
        # Update Ride
        ride.status = "dropoff"
        ride.save()

        # Create RideEvent
        models.RideEvent.objects.create(id_ride=ride, description='Status changed to dropoff')
        return Response("dropped off")
