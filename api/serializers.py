from rest_framework import serializers
from my_expense.models import Expense, Category


class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ('category', 'price', 'comment', 'user')


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('order', 'title', 'category_group')
