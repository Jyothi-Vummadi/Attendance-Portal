from django.contrib import admin
from .models import User,att 

# Register your models here.

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','username','password','is_fac']

@admin.register(att)
class AttModelAdmin(admin.ModelAdmin):
    list_display = ['id_s', 'date', 'time']
