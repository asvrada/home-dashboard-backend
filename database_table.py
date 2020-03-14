from peewee import *
import uuid
from datetime import date, datetime

db = SqliteDatabase('db/backend.db')


class BaseModel(Model):
    class Meta:
        database = db


class Transaction(BaseModel):
    # Auto added
    # id = AutoField()
    amount = FloatField(default=0)
    category = CharField(max_length=64, default="Undefined")
    company = CharField(max_length=64, default="Undefined")
    note = CharField(max_length=1024, default="")
    time_created = DateTimeField(formats='%Y-%m-%d %H:%M:%S.%f', default=datetime.today)


class RecurringBill(BaseModel):
    # Auto added
    # id = AutoField()
    frequency = CharField(max_length=10)
    recurring_month = IntegerField()
    recurring_date = IntegerField()
    amount = FloatField(default=0)
    category = CharField(max_length=64, default="Undefined")
    company = CharField(max_length=64, default="Undefined")
    note = CharField(max_length=1024, default="")
    time_created = DateTimeField(formats='%Y-%m-%d %H:%M:%S.%f', default=datetime.today)

    class Meta:
        table_name = "recurring_bill"


if __name__ == '__main__':
    db.connect()
    db.create_tables([Transaction, RecurringBill])

    Transaction.create(amount=100)
    Transaction.create(amount=200)

    print(len(Transaction.select()))

    db.close()
    # Returns: 1
