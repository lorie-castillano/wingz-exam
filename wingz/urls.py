from django.urls import include, path
from rest_framework import routers
from core import views as core_views

router = routers.DefaultRouter()
router.register(r'rides', core_views.RideViewSet, basename="rides")

urlpatterns = [
    path('', include(router.urls)),
]
