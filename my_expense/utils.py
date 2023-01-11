import datetime


def get_group_info(categories):

	"""For displaying category group headers in html-table.
	If several groups standing one-by-one have same category, they will have one big category header,
	spanned above all of them"""

	search_flag = False
	cat_name = ''
	counter = 0
	position = ''
	groups = {}     # dict key - index of first in a row category with cat. group, value - digit of colspan in a table
	for i in range(len(categories)):
		if categories[i].category_group:
			if search_flag:
				if categories[i].category_group == cat_name:
					counter += 1
				else:
					groups[position] = counter * 2
					counter = 1
					cat_name = categories[i].category_group
					position = i + 1
			else:
				search_flag = True
				cat_name = categories[i].category_group
				counter = 1
				position = i + 1
		else:
			if search_flag:
				groups[position] = counter * 2
				search_flag = False
	if search_flag:
		groups[position] = counter * 2
	return groups


def get_date_range(start=None, end=None):

	"""Provides a range of dates"""

	if not end:
		end = datetime.date.today()
	if not start:
		start = datetime.date(end.year, end.month, 1)
	delta = (end - start).days
	dates = [(start + datetime.timedelta(days=i)) for i in range(delta + 1)]
	return dates


def analyze_expenses(expense_list, user_expense_categories):

	"""Performs expense analytics. Returns 3 dictionaries: expenses grouped by day with daily sum,
	total sum of each category for requested period and total sum of each category group"""

	expenses_by_day = {}
	summary_by_category = {category.title: 0 for category in user_expense_categories}
	summary_by_group = {category.category_group: 0 for category in user_expense_categories if category.category_group}
	for expense in expense_list:
		day = expense.timestamp  # поменять потом на timestamp!
		if not expenses_by_day.get(day):
			expenses_by_day[day] = {'day_sum': 0}
		if not expenses_by_day[day].get(expense.category.title):
			expenses_by_day[day][expense.category.title] = [expense.price, expense.comment]
		else:
			expenses_by_day[day][expense.category.title][0] += expense.price
			expenses_by_day[day][expense.category.title][1] += f'\n{expense.comment}'
		expenses_by_day[day]['day_sum'] += expense.price
		summary_by_category[expense.category.title] += expense.price
		if expense.category.category_group:
			summary_by_group[expense.category.category_group] += expense.price
	summary_by_category['ALL'] = sum(summary_by_category.values())

	return expenses_by_day, summary_by_category, summary_by_group
