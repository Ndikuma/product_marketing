from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum
from marketing.models import Ad, StatusChoices

class Command(BaseCommand):
    help = 'Sends performance reports for all active ads'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Override default admin email')

    def handle(self, *args, **kwargs):
        email = kwargs.get('email') or settings.ADMIN_EMAIL
        ads = Ad.objects.filter(status=StatusChoices.ACTIVE)
        if not ads:
            self.stdout.write(self.style.WARNING('No active ads found.'))
            return

        for ad in ads:
            context = {
                'ad_name': ad.name,
                'product_name': ad.product.name,
                'ctr': ad.get_ctr(),
                'roas': ad.get_roas(),
                'engagement': ad.get_engagement_rate(),
                'impressions': ad.metrics.aggregate(total=Sum('impressions'))['total'] or 0,
                'clicks': ad.metrics.aggregate(total=Sum('clicks'))['total'] or 0,
                'conversions': ad.metrics.aggregate(total=Sum('conversions'))['total'] or 0,
                'revenue': ad.metrics.aggregate(total=Sum('revenue'))['total'] or 0,
                'cost': ad.metrics.aggregate(total=Sum('cost'))['total'] or 0
            }
            send_mail(
                subject=f"Performance Report: {ad.name}",
                message=render_to_string('emails/performance_report.txt', context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=render_to_string('emails/performance_report.html', context),
                fail_silently=True,
            )
        self.stdout.write(self.style.SUCCESS(f'Sent performance reports to {email}'))