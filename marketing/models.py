from django.db import models
from django.core.validators import MinValueValidator, URLValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Sum
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from decimal import Decimal
import pytz

# TextChoices Classes
class AdTypeChoices(models.TextChoices):
    BANNER = 'banner', 'Banner'
    TEXT = 'text', 'Text'
    VIDEO = 'video', 'Video'
    NATIVE = 'native', 'Native'
    ADSENSE = 'adsense', 'Google AdSense'  # Added for ad network

class StatusChoices(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    PAUSED = 'paused', 'Paused'
    COMPLETED = 'completed', 'Completed'

class PlatformChoices(models.TextChoices):
    GOOGLE = 'google', 'Google Ads'
    FACEBOOK = 'facebook', 'Facebook Ads'
    INSTAGRAM = 'instagram', 'Instagram Ads'
    TIKTOK = 'tiktok', 'TikTok Ads'
    X = 'x', 'X Ads'

class DeviceChoices(models.TextChoices):
    ALL = 'all', 'All Devices'
    MOBILE = 'mobile', 'Mobile'
    DESKTOP = 'desktop', 'Desktop'
    TABLET = 'tablet', 'Tablet'

class GenderChoices(models.TextChoices):
    ALL = 'all', 'All'
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'

# Product Image Model
class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', help_text="Associated product")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, help_text="Uploaded image")
    image_url = models.URLField(blank=True, null=True, validators=[URLValidator()], help_text="External image URL")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for accessibility")
    is_primary = models.BooleanField(default=False, help_text="Set as primary image for product")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

    def get_image_url(self):
        """Return image URL (local or external)."""
        if self.image:
            return self.image.url
        return self.image_url or ''

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200, help_text="Product name")
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Stock keeping unit")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Regular price")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discounted price")
    purchase_url = models.URLField(validators=[URLValidator()], help_text="Affiliate or purchase URL")
    affiliate_commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Commission rate for affiliate sales (%)"
    )
    description = models.TextField(blank=True, null=True, help_text="Product description")
    stock = models.PositiveIntegerField(default=0, help_text="Available stock")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated targeting tags, e.g., electronics,headphones")
    category = models.CharField(max_length=100, blank=True, help_text="Product category, e.g., Electronics")
    low_stock_threshold = models.PositiveIntegerField(default=10, help_text="Send alert when stock falls below this")
    notify_email = models.EmailField(blank=True, help_text="Email for low stock notifications, defaults to staff user's email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_suggested_audience(self):
        """Suggest audience targeting based on tags and category."""
        tags = self.tags.split(',') if self.tags else []
        interests = tags + [self.category] if self.category else tags
        return {
            "location": "Global",
            "interests": ", ".join([i for i in interests if i]),
            "age_min": 18,
            "age_max": 65,
            "gender": GenderChoices.ALL,
            "device": DeviceChoices.ALL,
            "platform": PlatformChoices.GOOGLE
        }

    def predict_conversion_rate(self):
        """Predict conversion rate based on similar products' ads."""
        similar_ads = Ad.objects.filter(
            product__tags__contains=self.tags, status=StatusChoices.ACTIVE
        ).exclude(product=self)
        metrics = PerformanceMetric.objects.filter(ad__in=similar_ads).aggregate(
            total_conversions=Sum('conversions'), total_impressions=Sum('impressions')
        )
        conversions = metrics['total_conversions'] or 0
        impressions = metrics['total_impressions'] or 0
        return (conversions / impressions * 100) if impressions > 0 else 0

    def get_primary_image(self):
        """Return the primary image or first available image."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.get_image_url()
        return self.images.first().get_image_url() if self.images.exists() else ''

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['tags']),
        ]

# Ad Model
class Ad(models.Model):
    name = models.CharField(max_length=200, help_text="Ad name")
    is_affiliate = models.BooleanField(default=True, help_text="True for affiliate ads, False for ad network banners")

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ads', help_text="Promoted product")
    ad_type = models.CharField(max_length=20, choices=AdTypeChoices.choices, default=AdTypeChoices.BANNER, help_text="Type of ad")
    content = models.TextField(blank=True, null=True, help_text="Ad copy or ad network script (e.g., AdSense code)")
    media_url = models.URLField(blank=True, null=True, validators=[URLValidator()], help_text="Ad image or video URL")
    destination_url = models.URLField(validators=[URLValidator()], help_text="URL users are directed to")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT, help_text="Ad status")
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)], help_text="Total ad budget")
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)], help_text="Daily budget limit")
    cost_per_click = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, validators=[MinValueValidator(0)], help_text="Cost per click")
    schedule_start = models.DateTimeField(null=True, blank=True, help_text="Ad start date/time")
    schedule_end = models.DateTimeField(null=True, blank=True, help_text="Ad end date/time")
    timezone = models.CharField(max_length=50, default='UTC', help_text="Timezone for scheduling, e.g., Africa/Johannesburg")
    target_location = models.CharField(max_length=200, blank=True, help_text="Target audience location")
    target_interests = models.CharField(max_length=200, blank=True, help_text="Target audience interests")
    target_age_min = models.PositiveIntegerField(null=True, blank=True, help_text="Minimum target age")
    target_age_max = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum target age")
    target_gender = models.CharField(max_length=50, choices=GenderChoices.choices, default=GenderChoices.ALL, help_text="Target gender")
    target_device = models.CharField(max_length=20, choices=DeviceChoices.choices, default=DeviceChoices.ALL, help_text="Target device")
    target_platform = models.CharField(max_length=20, choices=PlatformChoices.choices, default=PlatformChoices.GOOGLE, help_text="Target platform")
    ab_test_group = models.CharField(max_length=50, blank=True, null=True, help_text="A/B test group identifier")
    notify_email = models.EmailField(blank=True, help_text="Email for ad notifications, defaults to staff user's email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.product.name}"

    def get_ctr(self):
        """Calculate click-through rate (CTR)."""
        metrics = self.metrics.aggregate(total_clicks=Sum('clicks'), total_impressions=Sum('impressions'))
        clicks = metrics['total_clicks'] or 0
        impressions = metrics['total_impressions'] or 0
        return (clicks / impressions * 100) if impressions > 0 else 0

    def get_roas(self):
        """Calculate return on ad spend (ROAS)."""
        metrics = self.metrics.aggregate(total_revenue=Sum('revenue'), total_cost=Sum('cost'))
        revenue = metrics['total_revenue'] or Decimal('0.00')
        cost = metrics['total_cost'] or Decimal('0.00')
        return (revenue / cost) if cost > 0 else Decimal('0.00')

    def get_engagement_rate(self):
        """Calculate engagement rate (clicks + conversions / impressions)."""
        metrics = self.metrics.aggregate(
            total_clicks=Sum('clicks'), total_conversions=Sum('conversions'), total_impressions=Sum('impressions')
        )
        engagements = (metrics['total_clicks'] or 0) + (metrics['total_conversions'] or 0)
        impressions = metrics['total_impressions'] or 0
        return (engagements / impressions * 100) if impressions > 0 else 0

    def optimize_status(self, ctr_threshold=0.5, roas_threshold=1.0, engagement_threshold=1.0):
        """Pause ad if performance is below thresholds and send notification."""
        if self.status != StatusChoices.ACTIVE:
            return None
        ctr = self.get_ctr()
        roas = self.get_roas()
        engagement = self.get_engagement_rate()
        if ctr < ctr_threshold or roas < roas_threshold or engagement < engagement_threshold:
            self.status = StatusChoices.PAUSED
            self.save()
            return f"Paused {self.name} (CTR: {ctr:.2f}%, ROAS: {roas:.2f}, Engagement: {engagement:.2f}%)"
        return None

    def is_scheduled(self):
        """Check if ad is within its scheduled period in the specified timezone."""
        if not (self.schedule_start and self.schedule_end):
            return True
        try:
            tz = pytz.timezone(self.timezone)
            now = timezone.now().astimezone(tz)
            start = self.schedule_start.astimezone(tz)
            end = self.schedule_end.astimezone(tz)
            return start <= now <= end
        except pytz.exceptions.UnknownTimeZoneError:
            return False

    def run_ab_test(self, other_ad):
        """Compare this ad with another in the same A/B test group."""
        if not other_ad or self.ab_test_group != other_ad.ab_test_group or not self.ab_test_group:
            return None
        self_ctr = self.get_ctr()
        other_ctr = other_ad.get_ctr()
        return self if self_ctr >= other_ctr else other_ad

    def clean(self):
        """Validate schedule, targeting, and budget fields."""
        from django.core.exceptions import ValidationError
        if self.schedule_start and self.schedule_end and self.schedule_end <= self.schedule_start:
            raise ValidationError("End date must be after start date.")
        if self.target_age_min and self.target_age_max and self.target_age_max < self.target_age_min:
            raise ValidationError("Maximum age must be greater than minimum age.")
        if self.daily_budget and self.budget and self.daily_budget > self.budget:
            raise ValidationError("Daily budget cannot exceed total budget.")

    class Meta:
        verbose_name = "Ad"
        verbose_name_plural = "Ads"
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['schedule_start', 'schedule_end']),
            models.Index(fields=['ab_test_group']),
        ]

# Performance Metric Model
class PerformanceMetric(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='metrics', help_text="Associated ad")
    date = models.DateField(default=timezone.now, help_text="Date of metrics")
    impressions = models.PositiveIntegerField(default=0, help_text="Number of ad views")
    clicks = models.PositiveIntegerField(default=0, help_text="Number of clicks to destination URL")
    conversions = models.PositiveIntegerField(default=0, help_text="Number of purchases or sign-ups")
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Revenue from conversions")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Ad spend")
    engagement_count = models.PositiveIntegerField(default=0, help_text="Custom engagement actions, e.g., likes, shares")
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Commission from affiliate conversions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Metrics for {self.ad.name} on {self.date}"

    @classmethod
    def allocate_budget(cls, total_budget, ads, weight_ctr=0.6, weight_roas=0.4):
        """Allocate budget based on weighted CTR and ROAS."""
        if not ads:
            return []
        ad_metrics = [(ad, ad.get_ctr(), ad.get_roas()) for ad in ads]
        max_ctr = max((ctr for _, ctr, _ in ad_metrics), default=1) or 1
        max_roas = max((roas for _, _, roas in ad_metrics), default=1) or 1
        allocations = []
        total_score = sum((weight_ctr * (ctr / max_ctr) + weight_roas * (roas / max_roas)) for _, ctr, roas in ad_metrics) or 1
        for ad, ctr, roas in ad_metrics:
            score = weight_ctr * (ctr / max_ctr) + weight_roas * (roas / max_roas)
            ad_budget = (score / total_score) * total_budget if total_score > 0 else total_budget / len(ads)
            ad.budget = round(ad_budget, 2)
            ad.save()
            allocations.append((ad.name, ad.budget))
        return allocations

    class Meta:
        verbose_name = "Performance Metric"
        verbose_name_plural = "Performance Metrics"
        unique_together = ('ad', 'date')
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['ad', 'date']),
        ]

# Signals for Email Notifications
@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    """Send low stock email notification to notify_email (defaults to staff user's email)."""
    if instance.stock <= instance.low_stock_threshold and instance.notify_email:
        subject = f"Low Stock Alert: {instance.name}"
        context = {
            'product_name': instance.name,
            'stock': instance.stock,
            'threshold': instance.low_stock_threshold,
            'purchase_url': instance.purchase_url
        }
        send_mail(
            subject=subject,
            message=render_to_string('emails/low_stock.txt', context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.notify_email],
            html_message=render_to_string('emails/low_stock.html', context),
            fail_silently=True,
        )

@receiver(post_save, sender=Ad)
def notify_ad_status(sender, instance, **kwargs):
    """Send email if ad is paused or created to notify_email (defaults to staff user's email)."""
    if not instance.notify_email:
        return
    if instance.status == StatusChoices.PAUSED:
        subject = f"Ad Paused: {instance.name}"
        context = {
            'ad_name': instance.name,
            'product_name': instance.product.name,
            'ctr': instance.get_ctr(),
            'roas': instance.get_roas(),
            'engagement': instance.get_engagement_rate()
        }
        send_mail(
            subject=subject,
            message=render_to_string('emails/ad_paused.txt', context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.notify_email],
            html_message=render_to_string('emails/ad_paused.html', context),
            fail_silently=True,
        )
    elif kwargs.get('created', False):
        subject = f"New Ad Created: {instance.name}"
        context = {
            'ad_name': instance.name,
            'product_name': instance.product.name,
            'destination_url': instance.destination_url
        }
        send_mail(
            subject=subject,
            message=f"New ad '{instance.name}' for product '{instance.product.name}' created.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.notify_email],
            html_message=f"<p>New ad <strong>{instance.name}</strong> for product <strong>{instance.product.name}</strong> created. View: <a href='{instance.destination_url}'>Link</a></p>",
            fail_silently=True,
        )