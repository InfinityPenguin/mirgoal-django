from django.contrib import admin
from .models import User
from .forms import UserCreationForm #, UserChangeForm

class UserAdmin(admin.ModelAdmin):
	add_form = UserCreationForm
	fields = ['email', 'password', 'name_first', 'name_last', 'last_login']
	list_display = ('email', 'name_first', 'name_last')

# Register your models here.
admin.site.register(User, UserAdmin)
