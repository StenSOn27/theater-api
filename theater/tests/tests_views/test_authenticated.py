from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from dateutil import parser

from theater.models import Actor, Genre, Play, TheaterHall, Performance, Reservation
from theater.serializers import (
    GenreSerializer,
    ActorSerializer,
    TheaterHallSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ReservationListSerializer,
)

CLASSES = {
    "genre": Genre,
    "actor": Actor,
    "theaterhall": TheaterHall,
    "play": Play,
    "performance": Performance,
    "reservation": Reservation,
}

SERIALIZERS = {
    "genre": GenreSerializer,
    "actor": ActorSerializer,
    "theaterhall": TheaterHallSerializer,
    "play": PlayListSerializer,
    "performance": PerformanceListSerializer,
    "reservation": ReservationListSerializer,
}

DETAIL_SERIALIZERS = {
    "play": PlayDetailSerializer,
    "performance": PerformanceDetailSerializer,
}

METHODS = ["get", "post", "put", "patch", "delete"]

User = get_user_model()


class Url:
    @staticmethod
    def list_url(obj: str) -> str:
        return reverse(f"theater:{obj}-list")

    @staticmethod
    def detail_url(obj: str, id: int) -> str:
        return reverse(f"theater:{obj}-detail", kwargs={"pk": id})


def normalize_datetime(dt_str):
    dt = parser.isoparse(dt_str)
    return dt.replace(microsecond=0, tzinfo=None)


class AuthenticatedUserTheaterApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@example.com", password="pass123")
        self.client.force_authenticate(self.user)

        self.genre = Genre.objects.create(name="Comedy")
        self.actor = Actor.objects.create(first_name="Jane", last_name="Doe")
        self.theaterhall = TheaterHall.objects.create(name="Main Hall", rows=5, seats_in_row=10)
        self.play = Play.objects.create(title="Funny Show", description="A comedy")
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)
        self.performance = Performance.objects.create(
            play=self.play,
            theater_hall=self.theaterhall,
            show_time="2030-01-01T20:00:00Z",
        )
        self.reservation = Reservation.objects.create(user=self.user)

        self.instances = {
            "genre": self.genre,
            "actor": self.actor,
            "theaterhall": self.theaterhall,
            "play": self.play,
            "performance": self.performance,
            "reservation": self.reservation,
        }

    def check_list_access(self, obj_name: str, method: str, expected_status: int):
        url = Url.list_url(obj_name)
        method_func = getattr(self.client, method)
        response = method_func(url)

        self.assertEqual(response.status_code, expected_status,
                        msg=f"{method.upper()} list view for '{obj_name}' should return {expected_status}, got {response.status_code}")

        if method == "get" and expected_status == status.HTTP_200_OK:
            serializer_class = SERIALIZERS[obj_name]
            objects = CLASSES[obj_name].objects.all()
            serializer = serializer_class(objects, many=True)

            if isinstance(response.data, dict) and "results" in response.data:
                self.assertEqual(response.data["results"], serializer.data)
            else:
                self.assertEqual(response.data, serializer.data)

    def check_detail_access(self, obj_name: str, instance, method: str, expected_status: int):
        url = Url.detail_url(obj_name, instance.id)
        method_func = getattr(self.client, method)
        response = method_func(url)

        self.assertEqual(response.status_code, expected_status,
                         msg=f"{method.upper()} detail view for '{obj_name}' should return {expected_status}, got {response.status_code}")

        if method == "get" and expected_status == status.HTTP_200_OK:
            serializer_class = DETAIL_SERIALIZERS.get(obj_name, SERIALIZERS[obj_name])
            serializer = serializer_class(instance)
            self.assertEqual(response.data, serializer.data)


    def authenticated_user_access(self, obj_name):
        instance = self.instances[obj_name]
        for method in METHODS:
            with self.subTest(method=method):
                if method == "get":
                    self.check_list_access(obj_name, method, status.HTTP_200_OK)
                    self.check_detail_access(obj_name, instance, method, status.HTTP_200_OK)
                else:
                    self.check_list_access(obj_name, method, status.HTTP_403_FORBIDDEN)
                    self.check_detail_access(obj_name, instance, method, status.HTTP_403_FORBIDDEN)

    def test_genre(self):
        self.authenticated_user_access("genre")
    
    def test_actor(self):
        self.authenticated_user_access("actor")
    
    def test_play(self):
        self.authenticated_user_access("play")
    
    def test_theaterhall(self):
        self.authenticated_user_access("theaterhall")
    
    def test_performance(self):
        self.authenticated_user_access("performance")
    
    def test_reservation(self):
        self.authenticated_user_access("reservation")
