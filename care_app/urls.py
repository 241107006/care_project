from django.contrib import admin
from django.urls import path
from care_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('create_order', views.create_order, name='create_order'),
    path('all_orders/', views.all_orderds, name='all_orders'),
    path('order/<int:order_id>/accept/', views.order_accept, name='order_accept'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('profile/', views.profile, name='profile'),
    path('chat/<int:chat_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:chat_id>/', views.chat, name='chat'),
    path('chats/', views.chats, name='chats'),
    path('notifications/', views.notifications, name='notifications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)