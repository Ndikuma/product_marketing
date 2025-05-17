from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Product, Ad, PerformanceMetric, ProductImage

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
            'placeholder': 'Password (min 8 characters)',
            'aria-label': 'Password'
        }),
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
            'placeholder': 'Confirm Password',
            'aria-label': 'Confirm Password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'Username',
                'aria-label': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'Email address',
                'aria-label': 'Email address'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'sku', 'price', 'discount_price', 'purchase_url',
            'description', 'stock', 'tags', 'category', 'low_stock_threshold', 'notify_email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Product name'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'SKU'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'step': '0.01',
                'aria-label': 'Price'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'step': '0.01',
                'aria-label': 'Discount price'
            }),
            'purchase_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'https://example.com/buy',
                'aria-label': 'Purchase URL'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'rows': 4,
                'aria-label': 'Description'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Stock'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'e.g., electronics,headphones',
                'aria-label': 'Tags'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Category'
            }),
            'low_stock_threshold': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Low stock threshold'
            }),
            'notify_email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'email@example.com',
                'aria-label': 'Notify email'
            }),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'image_url', 'alt_text', 'is_primary']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'accept': 'image/*',
                'aria-label': 'Image file'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'https://example.com/image.jpg',
                'aria-label': 'Image URL'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'Describe the image',
                'aria-label': 'Alt text'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-500 focus:ring-blue-500 border-gray-600 rounded bg-gray-700',
                'aria-label': 'Is primary image'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')
        if not image and not image_url:
            raise forms.ValidationError("Either an image file or image URL must be provided.")
        if image and image_url:
            raise forms.ValidationError("Provide either an image file or an image URL, not both.")
        return cleaned_data

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
            'name', 'product', 'ad_type', 'content', 'media_url', 'destination_url', 'status',
            'budget', 'daily_budget', 'cost_per_click', 'schedule_start', 'schedule_end', 'timezone',
            'target_location', 'target_interests', 'target_age_min', 'target_age_max',
            'target_gender', 'target_device', 'target_platform', 'ab_test_group', 'notify_email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Ad name'
            }),
            'product': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Product'
            }),
            'ad_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Ad type'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'rows': 4,
                'aria-label': 'Ad content'
            }),
            'media_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'https://example.com/ad-media.jpg',
                'aria-label': 'Media URL'
            }),
            'destination_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'https://example.com/landing-page',
                'aria-label': 'Destination URL'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Status'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'step': '0.01',
                'aria-label': 'Budget'
            }),
            'daily_budget': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'step': '0.01',
                'aria-label': 'Daily budget'
            }),
            'cost_per_click': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'step': '0.01',
                'aria-label': 'Cost per click'
            }),
            'schedule_start': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'type': 'datetime-local',
                'aria-label': 'Schedule start'
            }),
            'schedule_end': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'type': 'datetime-local',
                'aria-label': 'Schedule end'
            }),
            'timezone': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Timezone'
            }),
            'target_location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'Country, Region, City',
                'aria-label': 'Target location'
            }),
            'target_interests': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'e.g., sports,technology',
                'aria-label': 'Target interests'
            }),
            'target_age_min': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Minimum age'
            }),
            'target_age_max': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Maximum age'
            }),
            'target_gender': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Target gender'
            }),
            'target_device': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Target device'
            }),
            'target_platform': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Target platform'
            }),
            'ab_test_group': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'A/B test group'
            }),
            'notify_email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'placeholder': 'email@example.com',
                'aria-label': 'Notify email'
            }),
        }

class PerformanceMetricForm(forms.ModelForm):
    class Meta:
        model = PerformanceMetric
        fields = ['ad', 'date', 'impressions', 'clicks', 'conversions', 'revenue', 'cost', 'engagement_count']
        widgets = {
            'ad': forms.Select(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Ad'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'type': 'date',
                'aria-label': 'Date'
            }),
            'impressions': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Impressions'
            }),
            'clicks': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Clicks'
            }),
            'conversions': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Conversions'
            }),
            'revenue': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'step': '0.01',
                'aria-label': 'Revenue'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'step': '0.01',
                'aria-label': 'Cost'
            }),
            'engagement_count': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
                'aria-label': 'Engagement count'
            }),
        }

class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with Tailwind CSS styling."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
            'placeholder': 'Enter your username',
            'aria-label': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-3 py-2 bg-gray-700 text-gray-300 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base',
            'placeholder': 'Enter your password',
            'aria-label': 'Password'
        })

    class Meta:
        fields = ['username', 'password']