from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core import models, serializers

User = get_user_model()


class RideViewSet(viewsets.ModelViewSet):
    queryset = models.Ride.objects.all()
    serializer_class = serializers.RideSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True)
    def pickup(self, request, pk=None):
        
        # Update Ride
        ride = models.Ride.objects.get(pk=pk)
        ride.status = "pickup"
        ride.pickup_time = timezone.now()
        ride.save()

        # Create RideEvent
        models.RideEvent.objects.create(id_ride=ride, description='Status changed to pickup')
        return Response("picked up")

    @action(detail=True)
    def dropoff(self, request, pk=None):
        
        # Update Ride
        ride = models.Ride.objects.get(pk=pk)
        ride.status = "dropoff"
        ride.save()

        # Create RideEvent
        models.RideEvent.objects.create(id_ride=ride, description='Status changed to dropoff')
        return Response("dropped off")
