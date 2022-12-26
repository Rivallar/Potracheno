from django import forms
from django.forms import modelformset_factory

from .models import Category


class UserEditForm(forms.Form):
	username = forms.CharField()
	first_name = forms.CharField(label='Имя', required=False)
	last_name = forms.CharField(label='Фамилия', required=False)
	email = forms.EmailField(label='E-mail', required=False)
	phone = forms.CharField(label='Телефон', required=False)


CategoryFormset = modelformset_factory(Category, fields=('title', 'category_group'), extra=10,
                                       labels={'title': 'Категория', 'category_group': 'Группа'})
