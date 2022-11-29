from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from .models import Category, Profile, Expense

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'category_group', 'title',)
	list_filter = ('category_group', )
	search_fields = ('title', 'category_group')
	ordering = ('category_group', 'title',)
	list_editable = ['category_group', 'title']
	
	
class ProfileInline(admin.StackedInline):
	model = Profile
	
	
class UserAdmin(AuthUserAdmin):
	inlines = [ProfileInline]
	list_display = ('username', 'phone', 'first_name', 'last_name')
	
	def phone(self, obj):
		return obj.profile.phone


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('timestamp','user', 'category', 'price', 'comment')
	list_filter = ('user', 'category')
	ordering = ('-timestamp', )
	search_fields = ('comment', )
	date_hierarchy = 'timestamp'

		
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
