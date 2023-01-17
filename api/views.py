from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics

import datetime

from my_expense.models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer


# Create your views here.
class ExpenseAPIView(generics.ListAPIView):
    queryset = Expense.objects.all().order_by('-timestamp')
    serializer_class = ExpenseSerializer


class CategoriesAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(profile=self.request.user.profile)
        return queryset


class AddExpenseAPIView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, id=self.request.data.get('user'))
        category = get_object_or_404(Category, id=self.request.data.get('category'), profile=user.profile)
        return serializer.save(user=user, timestamp=datetime.date.today())
