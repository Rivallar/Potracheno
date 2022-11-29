from django.urls import path

from . import views

app_name = 'my_expense'

urlpatterns = [
	path('', views.view_expenses, name='view_expenses'),
	]
