from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from .forms import UserRegistrationForm
from my_expense.models import Profile


# Create your views here.
def index_view(request):

	"""Landing page with login/register links"""

	return render(request, 'accounts/index.html')


def user_register(request):

	"""Registers new user, creates his empty profile and automatically logs him in"""

	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			cd = user_form.cleaned_data
			if not Profile.objects.filter(phone=cd['phone']).exists():
				new_user = user_form.save(commit=False)
				new_user.set_password(user_form.cleaned_data['password'])
				new_user.save()
				Profile.objects.create(user=new_user, phone=cd['phone'])
				login(request, new_user)
				return redirect('my_expense:profile_settings')
			else:
				user_form.add_error('phone', 'Номер телефона уже используется')
				return render(request, 'accounts/register.html', {'user_form': user_form})
		return render(request, 'accounts/register.html', {'user_form': user_form})
	else:
		user_form = UserRegistrationForm()
		return render(request, 'accounts/register.html', {'user_form': user_form})


class AccountDeleteView(DeleteView, LoginRequiredMixin):
	model = User
	success_url = reverse_lazy('accounts:logout')
	template_name = 'accounts/delete_account.html'
