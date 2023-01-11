from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


# Create your models here.
class Profile(models.Model):

    """User profile with additional info"""

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):

    """Categories of expenses to spare money"""

    profile = models.ForeignKey(Profile, related_name='categories', on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    category_group = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(validators=[MaxValueValidator(10, message="Categories order must be 1-10"),
                                                    MinValueValidator(1, message="Categories order must be 1-10")],
                                        blank=True, null=True)  # assigns automatically in save() method

    def save(self, *args, **kwargs):
        if not self.order:
            order_list = self.profile.categories.values_list('order', flat=True).order_by('order')
            for i in range(1, 11):
                if i not in order_list:
                    self.order = i
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('order',)


class Expense(models.Model):

    """Keeps information about one expense"""

    user = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='all_cat_expenses', null=True, on_delete=models.SET_NULL)

    price = models.DecimalField(max_digits=6, decimal_places=2)
    comment = models.CharField(max_length=254, blank=True)
    timestamp = models.DateField(default=timezone.now, db_index=True)

