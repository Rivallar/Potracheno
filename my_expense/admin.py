from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from .models import Category, Profile, Expense


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('profile', 'order', 'category_group', 'title')
	list_filter = ('profile', 'category_group', )
	search_fields = ('profile', 'title', 'category_group')
	ordering = ('order', 'category_group', 'title',)
	list_editable = ['category_group', 'title', 'order']
	
	
class ProfileInline(admin.StackedInline):
	model = Profile
	
	
class UserAdmin(AuthUserAdmin):
	inlines = [ProfileInline]
	list_display = ('username', 'phone', 'first_name', 'last_name')
	
	def phone(self, obj):
		return obj.profile.phone


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('timestamp', 'user', 'category', 'price', 'comment')
	list_filter = ('user',)
	ordering = ('-timestamp', )
	search_fields = ('comment', )
	date_hierarchy = 'timestamp'

		
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
