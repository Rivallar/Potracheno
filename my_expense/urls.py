from django.urls import path

from . import views

app_name = 'my_expense'

urlpatterns = [
	path('profile/', views.profile_view, name='profile'),
	path('profile/settings/', views.profile_settings_view, name='profile_settings'),
	path('profile/settings/add_categories/', views.edit_categories_view, name='add_categories'),
	path('profile/settings/category_order/', views.CategoriesOrderView.as_view(), name='category_order'),
	path('profile/settings/delete_categories/delete/', views.delete_categories_view, name='delete'),
	path('profile/settings/delete_categories/', views.profile_settings_view, name='delete_categories'),
	path('profile/settings/edit_categories/', views.edit_categories_view, name='edit_categories'),
	path('', views.view_expenses, name='view_expenses'),
	]


