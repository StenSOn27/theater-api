from django.urls import path, include
from rest_framework import routers

from theater.views import (
    GenreViewSet,
    ActorViewSet,
    TheaterHallViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet, basename="genre")
router.register("actors", ActorViewSet, basename="actor")
router.register("theater_halls", TheaterHallViewSet, basename="theaterhall")
router.register("plays", PlayViewSet, basename="play")
router.register("performances", PerformanceViewSet, basename="performance")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = [path("", include(router.urls))]

app_name = "theater"
