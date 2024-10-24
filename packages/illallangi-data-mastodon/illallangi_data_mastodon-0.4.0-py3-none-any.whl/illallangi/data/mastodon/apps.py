from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

from illallangi.mastodon.adapters import MastodonAdapter


def add_model(
    **_kwargs: dict[str, object],
) -> None:
    from illallangi.django.data.models import Model, Synchronize

    Model.objects.update_or_create(
        description="Each status is a step towards discovering new horizons, embracing diverse cultures, and enriching your soul.",
        icon="mastodon/statuses.png",
        model="illallangi.data.mastodon.models.Status",
        plural="Statuses",
        singular="Status",
        url="statuses_html",
    )

    Synchronize.objects.update_or_create(
        callable="illallangi.data.mastodon.apps.synchronize",
    )


class MastodonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "illallangi.data.mastodon"

    def ready(
        self,
    ) -> None:
        post_migrate.connect(
            add_model,
            sender=self,
        )


def synchronize() -> None:
    from illallangi.data.mastodon.adapters import (
        MastodonAdapter as DjangoAdapter,
    )

    src = MastodonAdapter(
        **settings.MASTODON,
    )
    dst = DjangoAdapter()

    src.load()
    dst.load()

    src.sync_to(dst)
