from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Product, Ad, PerformanceMetric, ProductImage
from .forms import ProductForm, AdForm, PerformanceMetricForm, ProductImageForm, RegistrationForm,CustomAuthenticationForm

def is_staff_user(user):
    """Check if the user is a staff member."""
    return user.is_authenticated and user.is_staff

staff_required = user_passes_test(is_staff_user, login_url='marketing:login')

def home(request):
    """Display the homepage with summary, featured products, and ads."""
    product_count = Product.objects.count()
    ad_count = Ad.objects.count()
    metric_count = PerformanceMetric.objects.count()
    featured_products = Product.objects.all()[:6]  # Limit to 6 for carousel
    ads = Ad.objects.filter(status='active', ad_type='adsense')[:2]  # AdSense ads for homepage
    core_modules = [
        {'title': 'Marketers', 'description': 'Create and track ad campaigns with AI insights.', 'icon': 'person'},
        {'title': 'Businesses', 'description': 'Manage products and optimize stock levels.', 'icon': 'business'},
        {'title': 'Analysts', 'description': 'Monitor performance metrics like CTR and ROAS.', 'icon': 'people'},
        {'title': 'Retailers', 'description': 'Promote products across multiple platforms.', 'icon': 'store'},
    ]
    how_it_works_steps = [
        {'title': 'Add Product', 'description': 'Create and manage products with affiliate links.', 'image': 'https://picsum.photos/seed/step1/384/288'},
        {'title': 'Launch Ad', 'description': 'Set up targeted ads or integrate ad networks.', 'image': 'https://picsum.photos/seed/step2/384/288'},
        {'title': 'Track Earnings', 'description': 'Monitor clicks and commissions in real-time.', 'image': 'https://picsum.photos/seed/step3/384/288'},
    ]
    testimonials = [
        {'name': 'Jane Doe', 'role': 'Digital Marketer', 'quote': 'This platform made ad creation so easy!', 'avatar': 'https://picsum.photos/seed/jane/100/100'},
        {'name': 'John Smith', 'role': 'Retailer', 'quote': 'Managing products and stock is a breeze.', 'avatar': 'https://picsum.photos/seed/john/100/100'},
        {'name': 'Alex Lee', 'role': 'Analyst', 'quote': 'Real-time metrics helped optimize our campaigns.', 'avatar': 'https://picsum.photos/seed/alex/100/100'},
    ]
    faqs = [
        {'question': 'How do I add a product?', 'answer': 'Staff users can add products with affiliate links via the Create Product page.'},
        {'question': 'What ad networks are supported?', 'answer': 'We support Google AdSense and can integrate others like Media.net.'},
        {'question': 'How are earnings tracked?', 'answer': 'Clicks and conversions are tracked via performance metrics, with commissions calculated based on affiliate rates.'},
    ]
    context = {
        'product_count': product_count,
        'ad_count': ad_count,
        'metric_count': metric_count,
        'featured_products': featured_products,
        'ads': ads,
        'core_modules': core_modules,
        'how_it_works_steps': how_it_works_steps,
        'testimonials': testimonials,
        'faqs': faqs,
    }
    return render(request, 'index.html', context)

@login_required
def affiliate_dashboard(request):
    """Display affiliate dashboard with earnings and performance."""
    products = Product.objects.filter(ads__metrics__clicks__gt=0).distinct()
    metrics = PerformanceMetric.objects.filter(ad__product__in=products).order_by('-date')
    total_clicks = metrics.aggregate(total=Sum('clicks'))['total'] or 0
    total_conversions = metrics.aggregate(total=Sum('conversions'))['total'] or 0
    total_earnings = sum(
        (m.conversions * m.ad.product.price * (m.ad.product.affiliate_commission_rate / 100))
        for m in metrics
    )
    context = {
        'products': products,
        'metrics': metrics,
        'total_clicks': total_clicks,
        'total_conversions': total_conversions,
        'total_earnings': total_earnings,
    }
    return render(request, 'affiliate_dashboard.html', context)

def track_ad_click(request, ad_id):
    """Track ad click and redirect to destination URL."""
    ad = get_object_or_404(Ad, id=ad_id)
    metric, created = PerformanceMetric.objects.get_or_create(
        ad=ad,
        date=timezone.now().date(),
        defaults={'impressions': 0, 'clicks': 0, 'conversions': 0, 'revenue': 0.00, 'cost': 0.00}
    )
    metric.clicks += 1
    metric.save()
    return redirect(ad.destination_url)


def product_list(request):
    """List all products."""
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    """Display product details, images, and related ads."""
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    ads = Ad.objects.filter(product=product, status='active')
    context = {
        'product': product,
        'images': images,
        'ads': ads,
    }
    return render(request, 'product_detail.html', context)

def product_delete(request, pk):
    """Confirm and delete a product."""
    product = get_object_or_404(Product, pk=pk)
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete products.")
        return redirect('marketing:product_list')
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product {product.name} deleted successfully.")
        return redirect('marketing:product_list')
    return render(request, 'product_detail.html', {'product': product, 'delete': True})

def product_image_delete(request, pk, image_pk):
    """Confirm and delete a product image."""
    product = get_object_or_404(Product, pk=pk)
    image = get_object_or_404(ProductImage, pk=image_pk, product=product)
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete images.")
        return redirect('marketing:product_detail', pk=pk)
    if request.method == 'POST':
        image.delete()
        messages.success(request, "Image deleted successfully.")
        return redirect('marketing:product_detail', pk=pk)
    return render(request, 'product_detail.html', {'product': product, 'image': image, 'delete_image': True})

def product_click(request, product_id):
    """Track product affiliate link click and redirect to purchase URL."""
    product = get_object_or_404(Product, pk=product_id)
    ad = Ad.objects.filter(product=product, status='active').first()
    if ad:
        today = timezone.now().date()
        metric, created = PerformanceMetric.objects.get_or_create(
            ad=ad,
            date=today,
            defaults={'impressions': 0, 'clicks': 1, 'commission_earned': 0.00}
        )
        if not created:
            metric.clicks += 1
            metric.save()
    return redirect(product.purchase_url)


@login_required
@staff_required
def product_create(request):
    """Create a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.notify_email:
                product.notify_email = request.user.email
            product.save()
            messages.success(request, 'Product created successfully.')
            return redirect('marketing:product_image_create', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(initial={'notify_email': request.user.email})
    return render(request, 'product_form.html', {'form': form, 'title': 'Create Product'})

@login_required
@staff_required
def product_update(request, pk):
    """Update an existing product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('marketing:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'title': 'Update Product'})

@login_required
@staff_required
def product_delete(request, pk):
    """Delete a product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('marketing:product_list')
    return render(request, 'product_detail.html', {'product': product, 'delete': True})

@login_required
@staff_required
def product_image_create(request, pk):
    """Add images to a product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            messages.success(request, 'Image added successfully.')
            if 'add_another' in request.POST:
                return redirect('marketing:product_image_create', pk=pk)
            return redirect('marketing:product_detail', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductImageForm()
    return render(request, 'product_image_form.html', {'form': form, 'product': product, 'title': 'Add Product Image'})

@login_required
@staff_required
def product_image_delete(request, pk, image_pk):
    """Delete a product image."""
    product = get_object_or_404(Product, pk=pk)
    image = get_object_or_404(ProductImage, pk=image_pk, product=product)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully.')
        return redirect('marketing:product_detail', pk=pk)
    return render(request, 'product_detail.html', {'product': product, 'image': image, 'delete_image': True})

def ad_list(request):
    """Display affiliate products and ad network banners."""
    # Get affiliate products
    affiliate_products = Product.objects.all()[:10]  # Limit to 10 for performance
    # Get ad network banners
    ad_banners = Ad.objects.filter(is_affiliate=False)[:3]  # Limit to 3 banners
    # Track ad impressions
    if ad_banners:
        today = timezone.now().date()
        for ad in ad_banners:
            # Check if a metric exists for this ad and date
            metric, created = PerformanceMetric.objects.get_or_create(
                ad=ad,
                date=today,
                defaults={'impressions': 1, 'clicks': 0, 'commission_earned': 0.00}
            )
            if not created:
                # Increment impressions if record exists
                metric.impressions += 1
                metric.save()
    context = {
        'affiliate_products': affiliate_products,
        'ad_banners': ad_banners,
    }
    return render(request, 'ads_list.html', context)

def ad_click(request, ad_id):
    """Track ad click and redirect to destination URL."""
    ad = get_object_or_404(Ad, pk=ad_id)
    # Record click
    today = timezone.now().date()
    metric, created = PerformanceMetric.objects.get_or_create(
        ad=ad,
        date=today,
        defaults={'impressions': 0, 'clicks': 1, 'commission_earned': 0.00}
    )
    if not created:
        # Increment clicks if record exists
        metric.clicks += 1
        metric.save()
    return redirect(ad.destination_url)



def ad_detail(request, pk):
    """Display ad details with metrics."""
    ad = get_object_or_404(Ad, pk=pk)
    metrics = ad.metrics.all()
    context = {'ad': ad, 'metrics': metrics}
    return render(request, 'ad_detail.html', context)

@login_required
@staff_required
def ad_create(request):
    """Create a new ad."""
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            if not ad.notify_email:
                ad.notify_email = request.user.email
            ad.save()
            messages.success(request, 'Ad created successfully.')
            return redirect('marketing:ad_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdForm(initial={'notify_email': request.user.email})
    return render(request, 'ad_form.html', {'form': form, 'title': 'Create Ad'})

@login_required
@staff_required
def ad_update(request, pk):
    """Update an existing ad."""
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ad updated successfully.')
            return redirect('marketing:ad_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ad_form.html', {'form': form, 'title': 'Update Ad'})

@login_required
@staff_required
def ad_delete(request, pk):
    """Delete an ad."""
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Ad deleted successfully.')
        return redirect('marketing:ad_list')
    return render(request, 'ad_detail.html', {'ad': ad, 'delete': True})

@login_required
@staff_required
def metric_list(request):
    """List all performance metrics."""
    metrics = PerformanceMetric.objects.select_related('ad__product').all()
    return render(request, 'metric_list.html', {'metrics': metrics})

@login_required
@staff_required
def metric_detail(request, pk):
    """Display metric details."""
    metric = get_object_or_404(PerformanceMetric, pk=pk)
    return render(request, 'metric_detail.html', {'metric': metric})

@login_required
@staff_required
def metric_create(request):
    """Create a new performance metric."""
    if request.method == 'POST':
        form = PerformanceMetricForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Performance metric created successfully.')
            return redirect('marketing:metric_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PerformanceMetricForm()
    return render(request, 'metric_form.html', {'form': form, 'title': 'Create Performance Metric'})

@login_required
@staff_required
def metric_update(request, pk):
    """Update an existing performance metric."""
    metric = get_object_or_404(PerformanceMetric, pk=pk)
    if request.method == 'POST':
        form = PerformanceMetricForm(request.POST, instance=metric)
        if form.is_valid():
            form.save()
            messages.success(request, 'Performance metric updated successfully.')
            return redirect('marketing:metric_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PerformanceMetricForm(instance=metric)
    return render(request, 'metric_form.html', {'form': form, 'title': 'Update Performance Metric'})

@login_required
@staff_required
def metric_delete(request, pk):
    """Delete a performance metric."""
    metric = get_object_or_404(PerformanceMetric, pk=pk)
    if request.method == 'POST':
        metric.delete()
        messages.success(request, 'Performance metric deleted successfully.')
        return redirect('marketing:metric_list')
    return render(request, 'metric_detail.html', {'metric': metric, 'delete': True})

def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('marketing:home')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('marketing:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('marketing:home')

def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('marketing:home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('marketing:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})