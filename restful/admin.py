from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Transaction, EnumCategory, MonthlyBudget

admin.site.register(User, UserAdmin)
admin.site.register(MonthlyBudget)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'company', 'note', 'time_created')
    list_display_links = ('amount', 'category', 'company', 'note', 'time_created')
    empty_value_display = '-empty-'


@admin.register(EnumCategory)
class EnumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_display_links = ('name',)
    list_filter = ('category',)
    empty_value_display = '-empty-'
