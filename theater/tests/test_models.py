from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

from theater.models import (
    Actor,
    Genre,
    Play,
    TheaterHall,
    Reservation,
    Performance,
    Ticket,
)

User = get_user_model()

class ActorModelTest(TestCase):

    def test_str_and_full_name(self):
        actor = Actor.objects.create(first_name="Leonardo", last_name="DiCaprio")
        self.assertEqual(str(actor), "Leonardo DiCaprio")
        self.assertEqual(actor.full_name, "Leonardo DiCaprio")


class GenreModelTest(TestCase):

    def test_str(self):
        genre = Genre.objects.create(name="Drama")
        self.assertEqual(str(genre), "Drama")


class PlayModelTest(TestCase):

    def test_str_and_genres_actors(self):
        play = Play.objects.create(title="Hamlet", description="Shakespeare tragedy")
        genre1 = Genre.objects.create(name="Tragedy")
        genre2 = Genre.objects.create(name="Drama")
        actor1 = Actor.objects.create(first_name="John", last_name="Smith")
        actor2 = Actor.objects.create(first_name="Jane", last_name="Doe")

        play.genres.add(genre1, genre2)
        play.actors.add(actor1, actor2)

        self.assertEqual(str(play), "Hamlet")
        self.assertIn(genre1, play.genres.all())
        self.assertIn(actor1, play.actors.all())


class TheaterHallModelTest(TestCase):

    def test_capacity_and_str(self):
        hall = TheaterHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.assertEqual(hall.capacity, 200)
        self.assertEqual(str(hall), "Main Hall")


class ReservationModelTest(TestCase):

    def test_str_and_ordering(self):
        user = User.objects.create_user("user@example.com", "password")
        r1 = Reservation.objects.create(user=user)
        r2 = Reservation.objects.create(user=user)
        self.assertEqual(str(r1), str(r1.created_at))
        # ordering by -created_at
        reservations = Reservation.objects.all()
        self.assertTrue(reservations[0].created_at >= reservations[1].created_at)


class PerformanceModelTest(TestCase):

    def test_str_and_ordering(self):
        hall = TheaterHall.objects.create(name="Small Hall", rows=5, seats_in_row=10)
        play = Play.objects.create(title="Othello", description="Tragedy")
        p1 = Performance.objects.create(play=play, theater_hall=hall, show_time=timezone.now())
        p2 = Performance.objects.create(play=play, theater_hall=hall, show_time=timezone.now() + timedelta(days=1))

        self.assertEqual(str(p1), f"{play.title} {p1.show_time}")
        # ordering by -show_time
        performances = Performance.objects.all()
        self.assertTrue(performances[0].show_time >= performances[1].show_time)


class TicketModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("testuser@example.com", "password")
        self.hall = TheaterHall.objects.create(name="Hall 1", rows=10, seats_in_row=10)
        self.play = Play.objects.create(title="Macbeth", description="Tragedy")
        self.performance = Performance.objects.create(
            play=self.play,
            theater_hall=self.hall,
            show_time=timezone.now() + timedelta(days=1)
        )
        self.reservation = Reservation.objects.create(user=self.user)

    def test_validate_ticket_valid(self):
        # should not raise
        ticket = Ticket(row=5, seat=5, performance=self.performance, reservation=self.reservation)
        ticket.full_clean()  # no error expected

    def test_validate_ticket_row_out_of_range(self):
        ticket = Ticket(row=11, seat=5, performance=self.performance, reservation=self.reservation)
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_validate_ticket_seat_out_of_range(self):
        ticket = Ticket(row=5, seat=11, performance=self.performance, reservation=self.reservation)
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_ticket_unique_constraint(self):
        Ticket.objects.create(row=1, seat=1, performance=self.performance, reservation=self.reservation)
        reservation2 = Reservation.objects.create(user=self.user)
        duplicate_ticket = Ticket(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=reservation2
        )
        with self.assertRaises(ValidationError):
            duplicate_ticket.full_clean()

    def test_str(self):
        ticket = Ticket.objects.create(row=3, seat=4, performance=self.performance, reservation=self.reservation)
        expected_str = f"{str(self.performance)} (row: 3, seat: 4)"
        self.assertEqual(str(ticket), expected_str)
