from django import forms
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory

from .models import Category


class UserEditForm(forms.Form):
	username = forms.CharField()
	first_name = forms.CharField(label='Имя', required=False)
	last_name = forms.CharField(label='Фамилия', required=False)
	email = forms.EmailField(label='E-mail', required=False)
	phone = forms.CharField(label='Телефон', required=False)


# Hidden formset to delete Categories.
class BaseDeleteCategoryFormset(BaseModelFormSet):
	def add_fields(self, form, index):
		super().add_fields(form, index)
		form.fields['check'] = forms.BooleanField(label='', required=False)     # checkbox is hidden, controlled by javascript

DeleteCategoryFormset = modelformset_factory(Category, formset=BaseDeleteCategoryFormset, extra=0,
                                             fields=('title', 'category_group', 'id'),
                                             widgets={'title': forms.HiddenInput,   # field values shown as text
                                                      'category_group': forms.HiddenInput})
