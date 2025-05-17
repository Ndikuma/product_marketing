from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:product_id>/click/', views.product_click, name='product_click'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/images/create/', views.product_image_create, name='product_image_create'),
    path('products/<int:pk>/images/<int:image_pk>/delete/', views.product_image_delete, name='product_image_delete'),
    path('ads/list/', views.ad_list, name='ad_list'),
    path('ads/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ads/<int:pk>/click', views.ad_click, name='ad_click'),
    path('ads/create/', views.ad_create, name='ad_create'),
    path('ads/<int:pk>/update/', views.ad_update, name='ad_update'),
    path('ads/<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('metrics/', views.metric_list, name='metric_list'),
    path('metrics/<int:pk>/', views.metric_detail, name='metric_detail'),
    path('metrics/create/', views.metric_create, name='metric_create'),
    path('metrics/<int:pk>/update/', views.metric_update, name='metric_update'),
    path('metrics/<int:pk>/delete/', views.metric_delete, name='metric_delete'),
]