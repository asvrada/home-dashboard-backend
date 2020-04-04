from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

import pandas as pd
import pytz
from datetime import datetime

admin.site.register(models.User, UserAdmin)
admin.site.register(models.MonthlyBudget)


@admin.register(models.EnumCategory)
class EnumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_display_links = ('name',)
    list_filter = ('category',)
    empty_value_display = '-empty-'


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'company', 'note', 'creator', 'time_created')
    list_display_links = list_display
    empty_value_display = '-empty-'


@admin.register(models.RecurringBill)
class RecurringBillAdmin(admin.ModelAdmin):
    list_display = ('view_recurring_date', 'note',
                    'amount', 'category', 'company', 'time_created')
    list_display_links = list_display
    empty_value_display = '-empty-'

    def view_recurring_date(self, obj):
        """
        For annually bill: Every 4/2
        For monthly bill: Every 2
        """
        if obj.frequency == 'Y':
            return f"{obj.recurring_month}/{obj.recurring_day} every year"

        return f"{obj.recurring_day} every month"


##################
# Help functions #
##################
FILE_DUMMY_DATA = "./restful/tst/dummy_data.xlsx"


def read_excel(file):
    """
    Return a tuple of generator (enum, transaction)
    """

    def consume_series(row):
        return {
            'id': int(row['id']),
            'amount': float(row['amount']),
            'category': map_name_to_id[row['category']],
            'company': map_name_to_id[row['company']],
            'card': map_name_to_id[row['card']],
            'note': row['note'],
            'time_created': list(map(int, row['time_created'].split()))
        }

    df = pd.read_excel(file)
    # Don't leave number field empty in Excel
    df = df.fillna("")

    enum_category = set()
    enum_company = set()
    enum_card = set()

    for _, row in df.iterrows():
        enum_category.add(row['category'])
        enum_company.add(row['company'])
        enum_card.add(row['card'])

    # create enum first
    enum = []
    idx = 1

    for enums, category in zip([enum_category, enum_company, enum_card],
                               ["CAT", "COM", "CAR"]):
        for each in enums:
            enum.append({
                "id": idx,
                "name": each,
                "category": category
            })
            idx += 1

    # Map from name to enum id
    map_name_to_id = dict()
    for each in enum:
        map_name_to_id[each["name"]] = each["id"]

    # create transaction
    transactions = [consume_series(row) for _, row in df.iterrows()]

    return enum, transactions


def load_into_database(enum, transactions):
    """
    enum: [{id, img, name, category(3 letter choice)}]
    transaction: [{amount, category, company, card, note, time_created}]
    """
    # Create enum in database
    for payload in enum:
        models.EnumCategory.objects.create(**payload)

    # Create map from id to enum instance in database
    map_id_to_enum_instance = dict()
    for each in models.EnumCategory.objects.all():
        map_id_to_enum_instance[each.id] = each

    # Create transaction in database
    for payload in transactions:
        # Modify payload to point to enum instance
        payload["category"] = map_id_to_enum_instance[payload["category"]]
        payload["company"] = map_id_to_enum_instance[payload["company"]]
        payload["card"] = map_id_to_enum_instance[payload["card"]]

        # Create actual datetime object
        payload["time_created"] = datetime(*payload["time_created"], tzinfo=pytz.utc)
        models.Transaction.objects.create(**payload)
