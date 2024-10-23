from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'transaction_type', 'amount', 'date', 'description']
        
        # Optional: Add labels and help texts for better UX
        labels = {
            'category': 'Category',
            'transaction_type': 'Type',
            'amount': 'Amount',
            'date': 'Date',
            'description': 'Description',
        }
        widgets = {
            'date': forms.SelectDateWidget(),  # This widget allows date selection
        }
# finance/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')