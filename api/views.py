from rest_framework import generics

import datetime

from my_expense.models import Category, Profile
from .serializers import ExpenseSerializer, CategorySerializer, ProfileChatIDSerializer


# Create your views here.
class CategoriesAPIView(generics.ListAPIView):

    """Returns expense categories of a single user based on his profile`s telegram_chat_id."""

    serializer_class = CategorySerializer

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        queryset = Category.objects.filter(profile__telegram_chat_id=chat_id)
        return queryset


class AddExpenseAPIView(generics.CreateAPIView):

    """Saves received expense record.
    User is category-->profile-->user."""

    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        category = Category.objects.filter(id=category_id).select_related('profile', 'profile__user')[0]
        user = category.profile.user
        return serializer.save(user=user, timestamp=datetime.date.today())


class UpdateProfileChatAPIView(generics.UpdateAPIView):

    """Looks for profile by a given phone. Saves given telegram_chat_id in this profile."""

    queryset = Profile.objects.all()
    serializer_class = ProfileChatIDSerializer
    lookup_field = 'phone'

