from django import forms
from django.forms import modelformset_factory

from .models import Category, Expense


class UserEditForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    email = forms.EmailField(label='E-mail', required=False)
    phone = forms.IntegerField(label='Телефон', required=False, widget=forms.TextInput)


# formset to delete categories
DeleteCategoryFormset = modelformset_factory(Category,
                                             can_delete=True, extra=0,  # checkbox is hidden, controlled by javascript
                                             fields=('title', 'category_group', 'id'),
                                             widgets={'title': forms.HiddenInput,  # field values shown as text
                                                      'category_group': forms.HiddenInput})


class AddExpenseForm(forms.ModelForm):

    """A form for formset to add new expenses"""

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Категория')
    price = forms.DecimalField(max_digits=6, decimal_places=2, required=False, label='Сумма')

    def __init__(self, *args, prof_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(profile=prof_id)  # Shows only users categories

    def clean_price(self):  # price and category fields must be both filled in or empty
        cd = self.cleaned_data
        if (cd['category'] and not cd['price']) or (cd['price'] and not cd['category']):
            raise forms.ValidationError("Оба поля 'Категория' и 'Цена' должны быть заполнены!")
        return cd['price']

    class Meta:
        model = Expense
        fields = ('category', 'price', 'comment', 'timestamp')
        labels = {'comment': 'Комментарий', 'timestamp': 'Дата'}
        widgets = {'timestamp': forms.SelectDateWidget}


AddExpenseFormSet = modelformset_factory(Expense, form=AddExpenseForm, extra=15)
