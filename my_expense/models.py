from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
	"""Categories of expenses to spare money"""
	
	title = models.CharField(max_length=50, unique=True)
	category_group = models.CharField(max_length=50, blank=True)
	
	def __str__(self):
		return self.title
		
	class Meta:
		verbose_name = 'category'
		verbose_name_plural = 'categories'
		ordering = ('title', )

	
class Profile(models.Model):
	"""User profile with additional info"""
	
	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
	expense_categories = models.ManyToManyField(Category, related_name='profiles', blank=True)
	
	phone = models.CharField(max_length=50, blank=True)

	
class Expense(models.Model):
	"""Keeps information about one expense"""
	
	user = models.ForeignKey(User, related_name='expenses',
		on_delete=models.CASCADE)
	category = models.ForeignKey(Category, related_name='all_cat_expenses',
		null=True, on_delete=models.SET_NULL)
		
	price = models.DecimalField(max_digits=6, decimal_places=2)
	comment = models.CharField(max_length=254, blank=True)
	timestamp = models.DateTimeField(default=timezone.now, db_index=True)
	
