from django.urls import path

from .views import ExpenseAPIView, AddExpenseAPIView, CategoriesAPIView

urlpatterns = [
    path('add_expense/', AddExpenseAPIView.as_view()),
    path('user_categories/', CategoriesAPIView.as_view()),
    path('', ExpenseAPIView.as_view()),
]

