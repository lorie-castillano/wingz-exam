from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from core import models


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RideEvent
        fields = "__all__"

    def validate(self, attrs):
        ride_status = attrs.get("id_ride").status
        if (
            attrs.get("description") == "Status changed to dropoff"
            and ride_status != "pickup"
        ):
            raise serializers.ValidationError(
                {
                    "details": f"Ride is of status {ride_status}. This action is not allowed."
                }
            )

        elif (
            attrs.get("description") == "Status changed to pickup"
            and ride_status != "en-route"
        ):
            raise serializers.ValidationError(
                {
                    "details": f"Ride is of status {ride_status}. This action is not allowed."
                }
            )
        return attrs

    def create(self, validated_data):
        ride = validated_data.get("id_ride")
        if validated_data.get("description") == "Status changed to dropoff":
            ride.dropoff()
        elif validated_data.get("description") == "Status changed to pickup":
            ride.pickup()
        return super().create(validated_data)


class RideSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Ride
        geo_field = "pickup_location"
        fields = "__all__"
        read_only_fields = ("status", "pickup_time",)

    def validate_id_driver(self, id_driver):
        if id_driver.role != "driver":
            raise serializers.ValidationError(
                {"details": "`id_driver` provided is not a `driver`."}
            )

        booked_driver = models.Ride.objects.filter(id_driver=id_driver).exclude(
            status="dropoff"
        )
        if self.instance:
            booked_driver = booked_driver.exclude(id_ride=self.instance.pk)

        if booked_driver.exists():
            raise serializers.ValidationError(
                {"details": "`id_driver` provided has current booking."}
            )
        return id_driver

    def validate_id_rider(self, id_rider):
        if id_rider.role != "rider":
            raise serializers.ValidationError(
                {"details": "`id_rider` provided is not a `rider`."}
            )

        booked_rider = models.Ride.objects.filter(id_rider=id_rider).exclude(
            status="dropoff"
        )
        if self.instance:
            booked_rider = booked_rider.exclude(id_ride=self.instance.pk)

        if booked_rider.exists():
            raise serializers.ValidationError(
                {"details": "`id_rider` provided has current booking."}
            )
        return id_rider
  

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
        todays_ride_events = models.RideEvent.objects.filter(
            id_ride=obj.id_ride
        ).filter(created_at__gte=last_24_hrs, created_at__lte=datetime_now)
        serializer = RideEventSerializer(todays_ride_events, many=True)
        return serializer.data
