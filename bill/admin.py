from typing import Tuple, List, Dict

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

import pandas as pd
import pytz
from datetime import datetime

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
    list_display = ('amount', 'category', 'company', 'note', 'creator', 'time_created')
    list_display_links = list_display


@admin.register(models.RecurringBill)
class RecurringBillAdmin(admin.ModelAdmin):
    list_display = ('view_recurring_date', 'note',
                    'amount', 'category', 'company', 'time_created')
    list_display_links = list_display

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
FILE_DUMMY_DATA = "./bill/test_data.xlsx"


def read_excel(file: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Return a tuple of generator (enum, transaction)
    """

    def consume_series(pd_series) -> Dict:
        return {
            'id': int(pd_series['id']),
            'amount': float(pd_series['amount']),
            'category': dict_name_to_id[pd_series['category']],
            'company': dict_name_to_id[pd_series['company']],
            'card': dict_name_to_id[pd_series['card']],
            'note': pd_series['note'],
            'time_created': list(map(int, pd_series['time_created'].split()))
        }

    df = pd.read_excel(file).fillna("").astype({
        'category': 'str',
        'company': 'str',
        'card': 'str'
    })

    enum_category = set()
    enum_company = set()
    enum_card = set()

    # Gather all possible value for EnumCategory
    for _, row in df.iterrows():
        enum_category.add(row['category'])
        enum_company.add(row['company'])
        enum_card.add(row['card'])

    # create enum object
    enum = []
    idx = 1

    def set_to_sorted_list(s):
        return sorted(list(s))

    for enums, category in zip(
            [set_to_sorted_list(enum_category), set_to_sorted_list(enum_company), set_to_sorted_list(enum_card)],
            ["CAT", "COM", "CAR"]
    ):
        for each in enums:
            enum.append({
                "id": idx,
                "name": each,
                "category": category
            })
            idx += 1

    # Map from name to enum id
    dict_name_to_id = dict()
    for each in enum:
        dict_name_to_id[each["name"]] = each["id"]

    # create transaction object
    transactions = [consume_series(row) for _, row in df.iterrows()]

    return enum, transactions


def load_into_database(enum: List[Dict], transactions: List[Dict]) -> None:
    """
    enum: [{id, img, name, category(3 letter choice)}]
    transaction: [{amount, category, company, card, note, time_created}]
    """
    # Create enum in database
    for payload in enum:
        models.EnumCategory.objects.create(**payload)

    # Create map from id to enum instance in database
    dict_id_to_enum_instance = dict()
    for each in models.EnumCategory.objects.all():
        dict_id_to_enum_instance[each.id] = each

    # Create transaction in database
    for payload in transactions:
        # Modify payload to point to enum instance
        payload["category"] = dict_id_to_enum_instance[payload["category"]]
        payload["company"] = dict_id_to_enum_instance[payload["company"]]
        payload["card"] = dict_id_to_enum_instance[payload["card"]]

        # Create actual datetime object
        payload["time_created"] = datetime(*payload["time_created"], tzinfo=pytz.utc)
        models.Transaction.objects.create(**payload)
