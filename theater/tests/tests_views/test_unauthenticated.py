from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from theater.models import Actor, Genre, Play, TheaterHall, Performance, Reservation

CLASSES = {
    "genre": Genre,
    "actor": Actor,
    "theaterhall": TheaterHall,
    "play": Play,
    "performance": Performance,
    "reservation": Reservation,
}

METHODS = ["get", "post", "put", "patch", "delete"]

User = get_user_model()

class Url:
    @staticmethod
    def list_url(obj: str) -> str:
        return reverse(f"theater:{obj}-list")

    @staticmethod
    def detail_url(obj: str, pk: int) -> str:
        return reverse(f"theater:{obj}-detail", kwargs={"pk": pk})


class UnauthenticatedTheaterApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser@example.com", password="password")

        self.genre = Genre.objects.create(name="Tragedy")
        self.actor = Actor.objects.create(first_name="John", last_name="Smith")
        self.theaterhall = TheaterHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.play = Play.objects.create(title="Hamlet", description="Shakespeare tragedy")
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


    def check_list_access(self, obj_name: str, method: str = "get", expected_status: int = 401, data=None):
        list_url = Url.list_url(obj_name)
        method_func = getattr(self.client, method.lower())

        if method.lower() == "post":
            response = method_func(list_url, data=data or {})
        else:
            response = method_func(list_url)

        self.assertEqual(
            response.status_code,
            expected_status,
            msg=f"{method.upper()} list view for '{obj_name}' should return {expected_status}, got {response.status_code}"
        )

    def check_detail_access(self, obj_name: str, instance, method: str = "get", expected_status: int = 401, data=None):
        detail_url = Url.detail_url(obj_name, instance.id)
        method_func = getattr(self.client, method.lower())

        if method.lower() in ["put", "patch", "post", "delete"]:
            response = method_func(detail_url, data=data or {})
        else:
            response = method_func(detail_url)

        self.assertEqual(
            response.status_code,
            expected_status,
            msg=f"{method.upper()} detail view for '{obj_name}' id={instance.id} should return {expected_status}, got {response.status_code}"
        )

    def unauthorized_access_to_all_views(self, obj_name):
        instance = self.instances[obj_name]
        for method in METHODS:
            with self.subTest(method=method):
                self.check_list_access(obj_name, method)
                self.check_detail_access(obj_name, instance, method)

    def test_genre(self):
        self.unauthorized_access_to_all_views("genre")
    
    def test_actor(self):
        self.unauthorized_access_to_all_views("actor")
    
    def test_play(self):
        self.unauthorized_access_to_all_views("play")
    
    def test_theaterhall(self):
        self.unauthorized_access_to_all_views("theaterhall")
    
    def test_performance(self):
        self.unauthorized_access_to_all_views("performance")
    
    def test_reservation(self):
        self.unauthorized_access_to_all_views("reservation")
    