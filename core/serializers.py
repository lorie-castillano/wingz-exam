from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone_number",)
        # fields = "__all__"


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RideEvent
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    ride_events = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.Ride
        fields = "__all__"

    def get_ride_events(self, obj):
        ride_events = models.RideEvent.objects.filter(id_ride=obj.id_ride)
        serializer = RideEventSerializer(ride_events, many=True)
        return serializer.data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        id_rider = User.objects.get(pk=response["id_rider"])
        rider_serializer = UserSerializer(id_rider)
        response["id_rider"] = rider_serializer.data

        id_driver = User.objects.get(pk=response["id_driver"])
        driver_serializer = UserSerializer(id_driver)
        response["id_driver"] = driver_serializer.data
        
        return response
