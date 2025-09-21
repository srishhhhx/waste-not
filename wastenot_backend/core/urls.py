from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from core.views import analyze_item_condition
from django.contrib.auth import views as auth_views
router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/schedule/', views.schedule_exchange, name='schedule_exchange'),
    path('schedule/<int:schedule_id>/confirm/', views.confirm_exchange, name='confirm_exchange'),
    path('schedule/<int:schedule_id>/cancel/', views.cancel_exchange, name='cancel_exchange'),
    
    # Messaging URLs
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:message_id>/', views.view_message, name='view_message'),
    path('messages/send/', views.send_message, name='send_message'),
    # Change this URL pattern name to be consistent
    path('messages/send/<int:recipient_id>/', views.send_message, name='send_message'),
    path('messages/send/item/<int:item_id>/', views.send_message, name='send_message_about_item'),
    path('messages/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    
    # QR Code URLs
    # Add this to your urlpatterns
    path('item/<int:item_id>/qr-code/', views.item_qr_code, name='item_qr_code'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('pickup/confirm/<str:pickup_code>/', views.confirm_pickup, name='confirm_pickup'),
    
    path('analyze-condition/', analyze_item_condition, name='analyze_item_condition'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),]

