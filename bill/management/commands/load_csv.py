from typing import Set

from django.core.management.base import BaseCommand
import pandas as pd
import pytz
import datetime

from ... import models


def parse_time(str_time: str) -> datetime.datetime:
    format = '%Y-%m-%d %H:%M:%S'
    tz_seattle = pytz.timezone('America/Los_Angeles')

    tz_boston = pytz.timezone('America/New_York')
    datetime_before_seattle = datetime.datetime(2020, 2, 22, 12, 0, 0, tzinfo=tz_boston)

    unaware_dt = datetime.datetime.strptime(str_time, format)
    if pytz.utc.localize(unaware_dt) < datetime_before_seattle:
        aware_dt = tz_boston.localize(unaware_dt)
    else:
        aware_dt = tz_seattle.localize(unaware_dt)

    return aware_dt


class Command(BaseCommand):
    help = 'Load CSV from fixed file'

    def get_set_category(self) -> Set[str]:
        categories = models.EnumCategory.objects.all().filter(category='CAT')
        return set(categories)

    def parse_insert_row(self, row, set_category: Set[str]) -> None:
        """
        Parse
        时间
        类型 {支出/收入}
        账目名称 {category}
        金额 自然数 >= 0
        备注 {str | nan}
        """
        dt = parse_time(row["时间"])
        sub_type = row["类型"]
        amount_abs = row["金额"]
        category_full = row["账目名称"]
        note = row["备注"]

        # change amount
        amount = amount_abs if sub_type == '收入' else -amount_abs

        # change category
        category = category_full if category_full in set_category else None

        model_category_default = models.EnumCategory.objects.get(category='CAT', name="一般")
        model_category = model_category_default if category is None else models.EnumCategory.objects.get(category='CAT',
                                                                                                         name=category)
        # Set default value for card
        model_card = models.EnumCategory.objects.get(category='CAR', name='BOA')

        # Create instance in DB
        models.Transaction.objects.create(amount=amount, category=model_category, card=model_card, note=note,
                                          time_created=dt)

    def handle(self, *args, **options):
        df = pd.read_csv("./日常账本.csv").fillna('')
        set_category = self.get_set_category()

        for index, row in df.iterrows():
            self.parse_insert_row(row, set_category)
