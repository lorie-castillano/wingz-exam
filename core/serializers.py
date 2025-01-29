from django.contrib.auth import get_user_model
from rest_framework import serializers
from core import models


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone_number",)


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RideEvent
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    ride_events = serializers.SerializerMethodField()
    id_rider = UserSerializer()
    id_driver = UserSerializer()
    
    class Meta:
        model = models.Ride
        fields = "__all__"

    def get_ride_events(self, obj):
        ride_events = models.RideEvent.objects.filter(id_ride=obj.id_ride)
        serializer = RideEventSerializer(ride_events, many=True)
        return serializer.data
