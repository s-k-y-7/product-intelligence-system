"""
Seed Sources Management Command
================================
Creates or updates the Source entries needed for the pipeline.

Usage:
    python manage.py seed_sources
    python manage.py seed_sources --unified   (use unified mock server on port 8050)
"""

from django.core.management.base import BaseCommand
from products.models import Source


# Default source definitions
SOURCES = [
    {
        "name": "Local Ecommerce 1",
        "code": "local_ecommerce",
        "type": "ECOMMERCE",
        "base_url": "http://localhost:8050/ecommerce1",
    },
    {
        "name": "Local Ecommerce 2",
        "code": "local_ecommerce_2",
        "type": "ECOMMERCE",
        "base_url": "http://localhost:8050/ecommerce2",
    },
    {
        "name": "Local YouTube",
        "code": "local_youtube",
        "type": "VIDEO",
        "base_url": "http://localhost:8050/youtube",
    },
    {
        "name": "Local Text Reviews",
        "code": "local_text_review",
        "type": "REVIEW",
        "base_url": "http://localhost:8050/reviews",
    },
]


class Command(BaseCommand):
    help = "Seed the Source table with local mock API sources"

    def add_arguments(self, parser):
        parser.add_argument(
            "--port",
            type=int,
            default=8050,
            help="Port of the unified mock server (default: 8050)",
        )

    def handle(self, *args, **options):
        port = options["port"]

        for source_def in SOURCES:
            # Rewrite port in base_url if non-default
            base_url = source_def["base_url"]
            if port != 8050:
                base_url = base_url.replace(":8050", f":{port}")

            source, created = Source.objects.update_or_create(
                code=source_def["code"],
                defaults={
                    "name": source_def["name"],
                    "type": source_def["type"],
                    "base_url": base_url,
                    "is_active": True,
                },
            )

            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(f"  {action}: {source.name} → {base_url}")
            )

        self.stdout.write(self.style.SUCCESS("\nDone. All sources seeded."))
