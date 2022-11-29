from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm
from my_expense.models import Profile

# Create your views here.
def index_view(request):
	return render(request, 'accounts/index.html')

@login_required
def profile_view(request):
	return render(request, 'accounts/profile.html')

def user_register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid:
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			Profile.objects.create(user=new_user)
			login(request, new_user)
			return redirect('accounts:profile')
	else:
		user_form = UserRegistrationForm()
		return render(request, 'accounts/register.html', {'user_form': user_form})
