from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
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


class RideSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Ride
        geo_field = "pickup_location"
        fields = "__all__"


class RideListSerializer(GeoFeatureModelSerializer):
    ride_events = serializers.SerializerMethodField()
    id_rider = UserSerializer()
    id_driver = UserSerializer()
    class Meta:
        model = models.Ride
        geo_field = "pickup_location"
        fields = "__all__"

    def get_ride_events(self, obj):
        datetime_now = datetime.now()
        last_24_hrs = datetime.now() - timedelta(hours=24)
        todays_ride_events = (
            models.RideEvent.objects
            .filter(id_ride=obj.id_ride)
            .filter(created_at__gte=last_24_hrs, created_at__lte=datetime_now)
        )
        serializer = RideEventSerializer(todays_ride_events, many=True)
        return serializer.data
