from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

from illallangi.tripit.adapters import AirTransportAdapter as TripItAdapter


def add_model(
    **_kwargs: dict[str, object],
) -> None:
    from illallangi.django.data.models import Model, Synchronize

    Model.objects.update_or_create(
        description="Every leg of a journey, no matter how long or short, brings you closer to your destination.",
        icon="air_transport/flights.jpg",
        model="illallangi.data.air_transport.models.Flight",
        plural="Flights",
        singular="Flight",
        url="flights_html",
    )
    Model.objects.update_or_create(
        description="Each trip is a step towards discovering new horizons, embracing diverse cultures, and enriching your soul.",
        icon="air_transport/trips.jpg",
        model="illallangi.data.air_transport.models.Trip",
        plural="Trips",
        singular="Trip",
        url="trips_html",
    )

    Synchronize.objects.update_or_create(
        callable="illallangi.data.air_transport.apps.synchronize",
    )


class AirTransportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "illallangi.data.air_transport"

    def ready(
        self,
    ) -> None:
        post_migrate.connect(
            add_model,
            sender=self,
        )


def synchronize() -> None:
    from illallangi.data.air_transport.adapters import (
        AirTransportAdapter as DjangoAdapter,
    )

    src = TripItAdapter(
        **settings.TRIPIT,
    )
    dst = DjangoAdapter()

    src.load(
        **settings.AIR_TRANSPORT,
    )
    dst.load()

    src.sync_to(dst)
