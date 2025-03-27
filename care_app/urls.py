from django.contrib import admin
from django.urls import path
from care_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('create_order', views.create_order, name='create_order'),
    path('create_review/<int:order_id>', views.create_review, name='create_review'),
    path('all_orders/', views.all_orderds, name='all_orders'),
    path('order/<int:order_id>/accept/', views.order_accept, name='order_accept'),
    path('order/<int:order_id>/finish/', views.order_finish, name='order_finish'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('order_request/<int:request_id>/accept/', views.order_request_accept, name='order_request_accept'),
    path('order_request/<int:request_id>/reject/', views.order_request_reject, name='order_request_reject'),
    path('password_recovery/<slug:code>', views.password_recovery, name='password_recovery'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('forgot_password_success/<int:user_id>', views.forgot_password_success, name='forgot_password_success'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('profile_view/<int:user_id>/', views.profile_view, name='profile_view'),
    path('profile/', views.profile, name='profile'),
    path('chat/<int:chat_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:chat_id>/', views.chat, name='chat'),
    path('chats/', views.chats, name='chats'),
    path('notifications/', views.notifications, name='notifications'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)