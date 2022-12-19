from django.urls import path

from . import views

app_name = 'my_expense'

urlpatterns = [
	path('profile/', views.profile_view, name='profile'),
	path('', views.view_expenses, name='view_expenses'),
	]
