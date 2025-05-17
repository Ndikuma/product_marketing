from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum
from .models import Product, Ad, PerformanceMetric, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'image_url', 'alt_text', 'is_primary', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock', 'category', 'created_at')
    search_fields = ('name', 'sku', 'tags', 'category')
    list_filter = ('category', 'created_at')
    fields = (
        'name', 'sku', 'price', 'discount_price', 'purchase_url',
        'description', 'stock', 'tags', 'category', 'low_stock_threshold', 'notify_email'
    )
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'get_image_url', 'alt_text', 'is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    list_filter = ('is_primary', 'created_at')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'ad_type', 'status', 'budget', 'target_platform', 'created_at')
    search_fields = ('name', 'product__name', 'target_interests')
    list_filter = ('ad_type', 'status', 'target_platform', 'created_at')
    fields = (
        'name', 'product', 'ad_type', 'content', 'media_url', 'destination_url', 'status',
        'budget', 'daily_budget', 'cost_per_click', 'schedule_start', 'schedule_end', 'timezone',
        'target_location', 'target_interests', 'target_age_min', 'target_age_max',
        'target_gender', 'target_device', 'target_platform', 'ab_test_group', 'notify_email'
    )
    list_select_related = ('product',)
    actions = ['send_performance_report']

    def send_performance_report(self, request, queryset):
        """Send performance report for selected ads."""
        for ad in queryset:
            if ad.notify_email:
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
                    recipient_list=[ad.notify_email],
                    html_message=render_to_string('emails/performance_report.html', context),
                    fail_silently=True,
                )
        self.message_user(request, "Performance reports sent successfully.")

@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ('ad', 'date', 'impressions', 'clicks', 'conversions', 'revenue', 'cost')
    search_fields = ('ad__name',)
    list_filter = ('date', 'ad__product')
    fields = (
        'ad', 'date', 'impressions', 'clicks', 'conversions', 'revenue', 'cost', 'engagement_count'
    )
    list_select_related = ('ad', 'ad__product')