from django.conf import settings
from django.db import models


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


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    def __str__(self) -> str:
        return str(self.title)


class TheaterHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return (
            f"Hall: {self.name} rows:{self.rows} with {self.seats_in_row} seats in row"
        )


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)

class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theater_hall = models.ForeignKey(TheaterHall, on_delete=models.CASCADE)
    showtime = models.DateTimeField()

    def __str__(self) -> str:
        return f"Perfomance {self.play} on {self.showtime}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.DO_NOTHING)
    reservation = models.ForeignKey(Reservation, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Row({self.row}), seat({self.seat})"
