from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render

from .forms import UserEditForm, CategoryFormset
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
	user = request.user
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
				except IntegrityError as e:
					if 'UNIQUE constraint failed: auth_user.username' in e.args[0]:     # this username already exists
						messages.error(request, f'Username "{cd["username"]}" уже занят.')
						user_form = UserEditForm(initial=initial)
					else:
						messages.error(request, 'Ошибка! Проверьте введённые данные.')
	else:
		user_form = UserEditForm(initial=initial)
	return render(request, 'my_expense/settings/profile_settings.html', {'user_form': user_form})


@login_required
def add_categories_view(request):
	formset = CategoryFormset(queryset=Category.objects.none())
	return render(request, 'my_expense/settings/add_categories.html', {'formset': formset})
