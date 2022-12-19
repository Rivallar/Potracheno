from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Expense

# Create your views here.
@login_required
def profile_view(request):
	return render(request, 'my_expense/profile.html')

@login_required
def view_expenses(request):
	expenses = Expense.objects.filter(user=request.user)
	return render(request, 'my_expense/view_expenses.html', {'expenses': expenses})
