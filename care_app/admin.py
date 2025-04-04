from django.contrib import admin
from django.apps import apps
from .models import Order, CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'email', 'name', 'surname', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff') 
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password')}),
        ('Personal Info', {'fields': ('name', 'surname', 'birthday', 'sex', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'user_type')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

    search_fields = ('phone', 'email', 'name', 'surname')
    ordering = ('email',)
    
class CompletedOrderAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'author', 'full_name', 'phone', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('task_name', 'full_name', 'phone')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter()

admin.site.register(Order, CompletedOrderAdmin)

admin.site.register(CustomUser, CustomUserAdmin)

models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass