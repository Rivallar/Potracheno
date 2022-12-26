from django.urls import path

from . import views

app_name = 'my_expense'

urlpatterns = [
	path('profile/', views.profile_view, name='profile'),
	path('profile/settings/', views.profile_settings_view, name='profile_settings'),
	path('profile/settings/add_categories', views.add_categories_view, name='add_categories'),
	path('', views.view_expenses, name='view_expenses'),
	]
