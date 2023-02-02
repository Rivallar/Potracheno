from rest_framework import serializers
from my_expense.models import Expense, Category, Profile


class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ('category', 'price', 'comment')


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('order', 'title', 'id')


class ProfileChatIDSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('telegram_chat_id', )
