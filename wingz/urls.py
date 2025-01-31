from django.urls import include, path
from rest_framework import routers
from core import views as core_views


router = routers.DefaultRouter()
router.register(r'rides', core_views.RideViewSet, basename="rides")
router.register(r'ride_events', core_views.RideEventViewSet, basename="ride_events")

urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('dj_rest_auth.urls')),
]
