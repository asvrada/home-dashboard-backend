from peewee import *
from datetime import datetime
from src.config import db, timezone


class BaseModel(Model):
    class Meta:
        database = db


class Transaction(BaseModel):
    # Auto added
    # id = AutoField()
    icon = CharField(max_length=64, default="Undefined Icon")
    amount = FloatField(default=0)
    category = CharField(max_length=64, default="Undefined")
    # On which company did I spent the money
    company = CharField(max_length=64, default="Undefined")
    # which credit card related to this transaction
    card = CharField(max_length=64, default="Undefined")
    note = CharField(max_length=1024, default="")
    time_created = DateTimeField(formats=['%Y-%m-%d %H:%M:%S'], default=lambda: datetime.now(timezone))

    def serialize(self):
        data = {
            'id': self.id,
            'icon': self.icon,
            'amount': self.amount,
            'category': self.category,
            'company': self.company,
            'card': self.card,
            'note': self.note,
            'time': self.time_created,
        }

        return data

    def __repr__(self):
        return f"{self.id} {self.amount} {self.category} {self.company} {self.card} {self.note} {self.time_created}"


class RecurringBill(BaseModel):
    # Auto added
    # id = AutoField()
    frequency = CharField(max_length=10)
    recurring_month = IntegerField()
    recurring_date = IntegerField()
    icon = CharField(max_length=64, default="Undefined Icon")
    amount = FloatField(default=0)
    category = CharField(max_length=64, default="Undefined")
    company = CharField(max_length=64, default="Undefined")
    card = CharField(max_length=64, default="Undefined")
    note = CharField(max_length=1024, default="")
    time_created = DateTimeField(formats=['%Y-%m-%d %H:%M:%S'], default=lambda: datetime.now(timezone))

    class Meta:
        table_name = "recurring_bill"


def db_create_table():
    db.create_tables([Transaction, RecurringBill])


if __name__ == '__main__':
    # Only use this to create DB when run for the first time
    db.connect()
    db.create_tables([Transaction, RecurringBill])
    db.close()
