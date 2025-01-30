from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.gis.db import models as gis_models
from django.conf import settings
from django.db import models
from model_utils import Choices


class User(AbstractBaseUser):
    REQUIRED_FIELDS = ('email',)
    USERNAME_FIELD = 'username'
    ROLES = Choices("admin", "driver", "rider")
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(
        choices=ROLES,
        max_length=10,
        null=True,
        blank=True,
        default="admin"
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=50, blank=True, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    
    objects = UserManager()


class Ride(models.Model):
    STATUSES = Choices("en-route", "pickup", "dropoff")
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(
        choices=STATUSES,
        max_length=10,
        null=True,
        blank=True,
        default="en-route"
    )
    id_rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_rider",
    )
    id_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_driver",
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(null=True, blank=True)
    pickup_location = gis_models.PointField(srid=4326)

    def pickup(self):
        self.status = "pickup"
        if not self.pickup_time:
            self.pickup_time = timezone.now()
        self.save()

    def dropoff(self):
        self.status = "dropoff"
        self.save()


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey("Ride", on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        return super(RideEvent, self).save(*args, **kwargs)
