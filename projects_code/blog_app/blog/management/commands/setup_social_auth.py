import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Seeds the Site domain and Google SocialApp for production'

    def handle(self, *args, **options):
        # ── 1. Update Site domain ──────────────────────────────────────────────
        site_domain = os.environ.get('SITE_DOMAIN', 'my-portfolio-yphw.onrender.com')
        site, created = Site.objects.get_or_create(id=1)
        site.domain = site_domain
        site.name = site_domain
        site.save()
        self.stdout.write(self.style.SUCCESS(f'Site set to: {site_domain}'))

        # ── 2. Set up Google SocialApp ─────────────────────────────────────────
        google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        google_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')

        if not google_client_id or not google_secret:
            self.stdout.write(self.style.WARNING(
                'GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET env vars not set. '
                'Skipping SocialApp seed.'
            ))
            return

        from allauth.socialaccount.models import SocialApp

        app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': google_client_id,
                'secret': google_secret,
            }
        )

        if not created:
            # Update credentials in case they changed
            app.client_id = google_client_id
            app.secret = google_secret
            app.save()

        # Associate with site
        app.sites.add(site)
        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            f'{action} Google SocialApp and linked to site {site_domain}'
        ))
