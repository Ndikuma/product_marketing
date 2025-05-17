from django.core.management.base import BaseCommand
from django.utils import timezone
from marketing.models import Product, Ad, PerformanceMetric, StatusChoices, AdTypeChoices, PlatformChoices, DeviceChoices, GenderChoices
from datetime import timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with sample data for testing'

    def handle(self, *args, **kwargs):
        # Create products
        product1 = Product.objects.create(
            name="Wireless Headphones",
            sku="WH2025",
            price=99.99,
            discount_price=89.99,
            purchase_url="https://example.com/shop/wireless-headphones",
            image_url="https://example.com/images/headphones.jpg",
            description="High-quality wireless headphones",
            stock=100,
            tags="headphones,electronics",
            category="Electronics"
        )

        product2 = Product.objects.create(
            name="Smartwatch",
            sku="SW2025",
            price=199.99,
            discount_price=179.99,
            purchase_url="https://example.com/shop/smartwatch",
            image_url="https://example.com/images/smartwatch.jpg",
            description="Advanced smartwatch with fitness tracking",
            stock=50,
            tags="smartwatch,electronics",
            category="Electronics"
        )

        # Create ads
        ad1 = Ad.objects.create(
            name="Headphones Banner",
            product=product1,
            ad_type=AdTypeChoices.BANNER,
            content="Buy Wireless Headphones for $89.99!",
            media_url="https://example.com/ads/headphones-banner.jpg",
            destination_url=product1.purchase_url,
            status=StatusChoices.ACTIVE,
            budget=1000.00,
            daily_budget=100.00,
            cost_per_click=0.50,
            schedule_start=timezone.now(),
            schedule_end=timezone.now() + timedelta(days=30),
            timezone="Africa/Johannesburg",
            target_location="South Africa",
            target_interests="technology,headphones",
            target_age_min=18,
            target_age_max=35,
            target_gender=GenderChoices.ALL,
            target_device=DeviceChoices.MOBILE,
            target_platform=PlatformChoices.INSTAGRAM,
            ab_test_group="headphones_promo"
        )

        ad2 = Ad.objects.create(
            name="Smartwatch Video",
            product=product2,
            ad_type=AdTypeChoices.VIDEO,
            content="Discover the Smartwatch for $179.99!",
            media_url="https://example.com/ads/smartwatch-video.mp4",
            destination_url=product2.purchase_url,
            status=StatusChoices.ACTIVE,
            budget=1500.00,
            daily_budget=150.00,
            cost_per_click=0.75,
            schedule_start=timezone.now(),
            schedule_end=timezone.now() + timedelta(days=30),
            timezone="Africa/Johannesburg",
            target_location="Global",
            target_interests="technology,fitness",
            target_age_min=25,
            target_age_max=45,
            target_gender=GenderChoices.ALL,
            target_device=DeviceChoices.ALL,
            target_platform=PlatformChoices.TIKTOK
        )

        # Create performance metrics
        PerformanceMetric.objects.create(
            ad=ad1,
            date=timezone.now().date(),
            impressions=5000,
            clicks=250,
            conversions=20,
            revenue=1799.80,  # 20 * $89.99
            cost=125.00,
            engagement_count=50
        )

        PerformanceMetric.objects.create(
            ad=ad2,
            date=timezone.now().date(),
            impressions=3000,
            clicks=180,
            conversions=15,
            revenue=2699.85,  # 15 * $179.99
            cost=135.00,
            engagement_count=30
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))