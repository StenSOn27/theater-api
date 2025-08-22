from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse

from theater.models import Genre, Actor, Reservation, TheaterHall, Play, Performance, Ticket
from theater.serializers import (
    GenreSerializer, ActorSerializer, ReservationListSerializer,
    TheaterHallSerializer, PlayListSerializer, PerformanceListSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class Url:
    @staticmethod
    def list_url(obj: str) -> str:
        return reverse(f"theater:{obj}-list")

    @staticmethod
    def detail_url(obj: str, id: int) -> str:
        return reverse(f"theater:{obj}-detail", kwargs={"pk": id})


class AdminUserTheaterApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin@example.com', 'password123')
        self.client.force_authenticate(self.user)

        self.instances = {}

        self.instances["genre"] = Genre.objects.create(name="Comedy")
        self.instances["actor"] = Actor.objects.create(first_name="Jane", last_name="Doe")
        self.instances["theaterhall"] = TheaterHall.objects.create(name="Main Hall", rows=5, seats_in_row=10)
        self.instances["play"] = Play.objects.create(title="Funny Show", description="A comedy")

        self.instances["play"].genres.add(self.instances["genre"])
        self.instances["play"].actors.add(self.instances["actor"])

        self.instances["performance"] = Performance.objects.create(
            show_time="2030-01-01T20:00:00Z",
            play=self.instances["play"],
            theater_hall=self.instances["theaterhall"]
        )
        self.instances["reservation"] = Reservation.objects.create(user=self.user)

        self.methods = {
            "get": {},
            "post": {
                "genre": {"name": "New Genre"},
                "actor": {"first_name": "John", "last_name": "Doe"},
                "theaterhall": {"name": "New Hall", "rows": 10, "seats_in_row": 15},
                "play": {
                    "title": "New Play",
                    "description": "A description",
                    "genres": [self.instances["genre"].id],
                    "actors": [self.instances["actor"].id],
                },
                "performance": {
                    "show_time": "2030-01-01T20:00:00Z",
                    "play": self.instances["play"].id,
                    "theater_hall": self.instances["theaterhall"].id,
                },
                "reservation": {
                    "tickets": [{
                        "row": 1,
                        "seat": 1,
                        "performance": self.instances["performance"].id
                    }]
                }
            },
            "put": {
                "genre": {"name": "Updated Genre"},
                "actor": {"first_name": "Updated", "last_name": "Actor"},
                "theaterhall": {"name": "Updated Hall", "rows": 20, "seats_in_row": 25},
                "play": {
                    "title": "Updated Play",
                    "description": "Updated description",
                    "genres": [self.instances["genre"].id],
                    "actors": [self.instances["actor"].id],
                },
                "performance": {
                    "show_time": "2030-01-02T20:00:00Z",
                    "play": self.instances["play"].id,
                    "theater_hall": self.instances["theaterhall"].id,
                },
            },
            "patch": {
                "genre": {"name": "Patched Genre"},
                "actor": {"first_name": "Patched"},
                "reservation": {
                    "user": self.user.id
                },
                "theaterhall": {"name": "Patched Hall"},
                "play": {"title": "Patched Play"},
                "performance": {"show_time": "2030-01-03T20:00:00Z"},
            },
            "delete": {},
        }

    def get_url(self, obj_name, detail=False, instance_id=None):
        if detail and instance_id is not None:
            return Url.detail_url(obj_name, instance_id)
        return Url.list_url(obj_name)

    def check_list_access(self, obj_name, method, expected_status):
        url = self.get_url(obj_name)
        data = self.methods.get(method, {}).get(obj_name, None)

        http_method = getattr(self.client, method)
        response = http_method(url, data, format='json')

        self.assertEqual(response.status_code, expected_status)

        if method == "get" and expected_status == status.HTTP_200_OK:
            serializer_class = {
                "genre": GenreSerializer,
                "actor": ActorSerializer,
                "theaterhall": TheaterHallSerializer,
                "play": PlayListSerializer,
                "performance": PerformanceListSerializer,
                "reservation": ReservationListSerializer,
            }.get(obj_name)

            if serializer_class:
                queryset = None
                if obj_name == "reservation":
                    queryset = Reservation.objects.all()
                else:
                    queryset = self.instances[obj_name].__class__.objects.all()

                serializer = serializer_class(queryset, many=True)
                if isinstance(response.data, dict) and "results" in response.data:
                    self.assertEqual(response.data["results"], serializer.data)
                else:
                    self.assertEqual(response.data, serializer.data)

    def check_detail_access(self, obj_name, instance, method, expected_status):
        url = self.get_url(obj_name, detail=True, instance_id=instance.id)
        data = self.methods.get(method, {}).get(obj_name, None)

        http_method = getattr(self.client, method)
        response = http_method(url, data, format='json')

        self.assertEqual(response.status_code, expected_status)

        if method == "get" and expected_status == status.HTTP_200_OK:
            serializer_class = {
                "genre": GenreSerializer,
                "actor": ActorSerializer,
                "theaterhall": TheaterHallSerializer,
                "play": PlayListSerializer,
                "performance": PerformanceListSerializer,
                "reservation": ReservationListSerializer,
            }.get(obj_name)

            if serializer_class:
                serializer = serializer_class(instance)
                self.assertEqual(response.data, serializer.data)

    def check_admin(self, obj_name):
        self.check_list_access(obj_name, "get", status.HTTP_200_OK)
        self.check_list_access(obj_name, "post", status.HTTP_201_CREATED)

        instance = self.instances[obj_name]
        if obj_name != "reservation":
            self.check_detail_access(obj_name, instance, "put", status.HTTP_200_OK)
            self.check_detail_access(obj_name, instance, "patch", status.HTTP_200_OK)
        self.check_detail_access(obj_name, instance, "delete", status.HTTP_204_NO_CONTENT)

    def test_genre(self):
        self.check_admin("genre")

    def test_actor(self):
        self.check_admin("actor")

    def test_play(self):
        self.check_admin("play")

    def test_performance(self):
        self.check_admin("performance")

    def test_reservation(self):
        self.check_admin("reservation")

    def test_theaterhall(self):
        self.check_admin("theaterhall")
