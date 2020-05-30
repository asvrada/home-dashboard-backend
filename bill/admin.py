from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.MonthlyBudget)
admin.site.register(models.Icon)


@admin.register(models.EnumCategory)
class EnumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon')
    list_display_links = ('name',)
    list_filter = ('category',)


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'company', 'note', 'skip_summary_flag', 'creator', 'time_created')
    list_display_links = list_display


@admin.register(models.RecurringBill)
class RecurringBillAdmin(admin.ModelAdmin):
    list_display = ('view_recurring_date', 'note', 'amount', 'category', 'company', 'skip_summary_flag', 'time_created')
    list_display_links = list_display
    list_filter = ('frequency',)

    def view_recurring_date(self, obj):
        """
        For annually bill: Every 4/2
        For monthly bill: Every 2
        """
        if obj.frequency == 'Y':
            return f"{obj.recurring_month}/{obj.recurring_day} every year"

        return f"{obj.recurring_day} every month"
