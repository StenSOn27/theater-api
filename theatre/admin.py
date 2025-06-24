from django.contrib import admin

from .models import (
    TheatreHall,
    Genre,
    Actor,
    Reservation,
    Performance,
    Play,
    Ticket,
)

admin.site.register(TheatreHall)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Reservation)
admin.site.register(Performance)
admin.site.register(Play)
admin.site.register(Ticket)
