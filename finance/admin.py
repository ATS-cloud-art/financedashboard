from django.contrib import admin
from .models import Category, Transaction, RecurringPayment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'category', 'date')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('description',)

@admin.register(RecurringPayment)
class RecurringPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'amount', 'due_date', 'frequency')

