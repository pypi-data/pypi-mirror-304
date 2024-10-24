from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

from illallangi.rdf.adapters import ResidentialAdapter as RDFAdapter


def add_model(
    **_kwargs: dict[str, object],
) -> None:
    from illallangi.django.data.models import Model, Synchronize

    Model.objects.update_or_create(
        description="Not just a location on a map, but a place where dreams are nurtured and memories are made.",
        icon="residential/residences.jpg",
        model="illallangi.data.residential.models.Residence",
        plural="Residences",
        singular="Residence",
        url="residences_html",
    )

    Synchronize.objects.update_or_create(
        callable="illallangi.data.residential.apps.synchronize",
    )


class ResidentialHistoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "illallangi.data.residential"

    def ready(
        self,
    ) -> None:
        post_migrate.connect(
            add_model,
            sender=self,
        )


def synchronize() -> None:
    from illallangi.data.residential.adapters import (
        ResidentialAdapter as DjangoAdapter,
    )

    src = RDFAdapter(
        **settings.RDF,
    )
    dst = DjangoAdapter()

    src.load(
        **settings.RESIDENTIAL,
    )
    dst.load()

    src.sync_to(dst)
