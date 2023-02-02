from django.urls import path

from .views import AddExpenseAPIView, CategoriesAPIView, UpdateProfileChatAPIView

urlpatterns = [
    path('add_expense/', AddExpenseAPIView.as_view()),
    path('update_chat_id/<int:phone>/', UpdateProfileChatAPIView.as_view()),
    path('user_categories/<chat_id>/', CategoriesAPIView.as_view()),
]

