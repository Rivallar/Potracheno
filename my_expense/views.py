from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic.base import View

from .forms import UserEditForm, DeleteCategoryFormset
from .models import Expense, Category


# Create your views here.
@login_required
def profile_view(request):
	return render(request, 'my_expense/profile.html')


@login_required
def view_expenses(request):
	expenses = Expense.objects.filter(user=request.user)
	return render(request, 'my_expense/view_expenses.html', {'expenses': expenses})


@login_required
def profile_settings_view(request):

	"""Manages user and profile info in a form.
	Changes user`s expense categories order or deletes them (depends on request URI)"""

	user = request.user
	context = {}
	initial = {
		'username': user.username,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'email': user.email,
		'phone': user.profile.phone}

	if request.method == 'POST':
		user_form = UserEditForm(request.POST)
		if user_form.is_valid():
			cd = user_form.cleaned_data
			if initial != cd:   # check if something changed
				try:
					User.objects.filter(id=user.id).update(
						username=cd['username'],
						first_name=cd['first_name'],
						last_name=cd['last_name'],
						email=cd['email']
						)
					user.profile.phone = cd['phone']
					user.profile.save()
					messages.success(request, 'Профиль успешно обновлён.')
					return redirect('my_expense:profile_settings')
				except IntegrityError as e:
					if 'UNIQUE constraint failed: auth_user.username' in e.args[0]:     # this username already exists
						messages.error(request, f'Username "{cd["username"]}" уже занят.')
						context['user_form'] = UserEditForm(initial=initial)
					else:
						messages.error(request, 'Ошибка! Проверьте введённые данные.')
	else:
		context['user_form'] = UserEditForm(initial=initial)

		# whether to delete or change order of expense categories
		if 'delete_categories' in request.path.split('/'):
			context['delete_formset'] = DeleteCategoryFormset(queryset=Category.objects.filter(profile=user.profile))
		else:
			context['expense_categories'] = Category.objects.filter(profile=user.profile)
	return render(request, 'my_expense/settings/profile_settings.html', context)


@login_required
def edit_categories_view(request):

	"""Handles both adding new expense categories and editing old ones"""

	CategoryFormset = modelformset_factory(Category, fields=('title', 'category_group'))
	if request.method == 'POST':
		formset = CategoryFormset(request.POST)
		if formset.is_valid():
			for item in formset.cleaned_data:
				if item:                # filters empty forms
					if item['id']:      # if there is an id we update existing category
						Category.objects.filter(id=item['id'].id).update(title=item['title'],
						                                              category_group=item['category_group'])
					else:
						Category.objects.create(title=item['title'], category_group=item['category_group'],
						                        profile=request.user.profile)
			messages.success(request, 'Изменения сохранены.')
			return redirect('my_expense:profile_settings')

	else:
		user_categories = Category.objects.filter(profile=request.user.profile)

		# Using same template for adding and editing (Formset info depends on request URI)
		if 'edit_categories' in request.path.split('/'):
			extra = 0
			queryset = user_categories
			button_name = 'Изменить'
		else:
			extra = 10 - user_categories.count()
			queryset = Category.objects.none()
			button_name = 'Добавить'

		CategoryFormset = modelformset_factory(Category, fields=('title', 'category_group'), extra=extra,
		                                       labels={'title': 'Категория', 'category_group': 'Группа'})
		formset = CategoryFormset(queryset=queryset)
	return render(request, 'my_expense/settings/edit_categories.html', {'formset': formset, 'button_name': button_name})


@login_required
@require_POST
def delete_categories_view(request):

	"""Separate view to actually manage categories deletion"""

	formset = DeleteCategoryFormset(request.POST)
	if formset.is_valid():
		for item in formset.cleaned_data:
			if item['check']:   # checkbox for deletion
				category = get_object_or_404(Category, id=item['id'].id, profile=request.user.profile)
				category.delete()
				messages.success(request, f'Категория \"{item["title"]}\" удалена.')
		return redirect('my_expense:profile_settings')
	messages.error(request, 'Что-то пошло не так. Не удалось удалить категории')
	return redirect('my_expense:profile_settings')


class CategoriesOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

	"""AJAX view to manage categories order"""

	def post(self, request):
		for cat_id, cat_order in self.request_json.items():
			Category.objects.filter(id=cat_id, profile=request.user.profile).update(order=cat_order+1)
		return self.render_json_response({'saved': 'OK'})
