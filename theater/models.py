import uuid
from django.conf import settings
from django.db import models
import os
from django.utils.text import slugify

class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.name)


def play_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/plays/", filename)


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="plays",
    )
    actors = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="plays",
    )
    image = models.ImageField(null=True, upload_to=play_image_file_path)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class TheaterHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Performance(models.Model):
    show_time = models.DateTimeField()
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performance"
    )
    theater_hall = models.ForeignKey(
        TheaterHall,
        on_delete=models.CASCADE,
        related_name="performance"
    )

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return self.play.title + " " + str(self.show_time)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.DO_NOTHING)
    reservation = models.ForeignKey(Reservation, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Row({self.row}), seat({self.seat})"
