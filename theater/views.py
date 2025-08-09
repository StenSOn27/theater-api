from django.contrib.auth.models import User
from rest_framework import viewsets

from theater.models import (
    Genre,
    Actor,
    Reservation,
    TheaterHall,
    Play,
    Performance,
    Ticket
)

from theater.serializers import (
    GenreSerializer,
    ActorSerializer,
    ReservationSerializer,
    TheaterHallSerializer,
    PlaySerializer,
    PerformanceSerializer,
    TicketSerializer
)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class TheaterHallViewSet(viewsets.ModelViewSet):
    queryset = TheaterHall.objects.all()
    serializer_class =  TheaterHallSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
