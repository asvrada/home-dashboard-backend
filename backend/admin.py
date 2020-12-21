from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.MonthlyBudget)
admin.site.register(models.Icon)


@admin.register(models.EnumCategory)
class EnumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon', 'user')
    list_display_links = list_display
    list_filter = ('category', 'user')


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'company', 'card', 'note', 'skip_summary_flag', 'creator', 'time_created', 'user')
    list_display_links = list_display


@admin.register(models.RecurringBill)
class RecurringBillAdmin(admin.ModelAdmin):
    list_display = ('view_recurring_date', 'note', 'amount', 'category', 'company', 'skip_summary_flag',
                    'time_created', 'user')
    list_display_links = list_display
    list_filter = ('frequency', 'user')

    def view_recurring_date(self, obj):
        """
        For annually bill: Every 4/2
        For monthly bill: Every 2
        """
        if obj.frequency == 'Y':
            return f"{obj.recurring_month}/{obj.recurring_day} every year"

        return f"{obj.recurring_day} every month"
