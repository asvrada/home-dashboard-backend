from graphene import Node, relay, Enum
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
import graphene

from graphql_relay.node.node import from_global_id

from . import models


# Type declaration

class EnumEnumCategory(Enum):
    # left: the string you want frontend to see
    # right: the actual data in DB
    Category = 'CAT'
    Company = 'COM'
    Card = 'CAR'
    NULL = 'NUL'


class EnumRecurringBillFrequency(Enum):
    Year = 'Y'
    Month = 'M'


class IconType(DjangoObjectType):
    class Meta:
        model = models.Icon
        interfaces = (Node,)
        filter_fields = ["keyword", "path"]


class EnumCategoryType(DjangoObjectType):
    category = EnumEnumCategory()

    class Meta:
        model = models.EnumCategory
        interfaces = (Node,)
        filter_fields = ["name", "category", "icon"]
        # exclude fields from model
        exclude_fields = ["category"]

    def resolve_category(self, info, **kwargs):
        return self.category


class RecurringBillType(DjangoObjectType):
    frequency = EnumRecurringBillFrequency()

    class Meta:
        model = models.RecurringBill
        interfaces = (Node,)
        filter_fields = ["frequency", "recurring_month", "recurring_day",
                         "amount", "category", "company", "card", "note", "time_created"]
        # exclude fields from model
        exclude_fields = ["frequency"]

    def resolve_frequency(self, info, **kwargs):
        return self.frequency


class TransactionType(DjangoObjectType):
    class Meta:
        model = models.Transaction
        interfaces = (Node,)
        filter_fields = ["amount", "category", "company", "card", "note", "time_created"]


# Create

class CreateIcon(relay.ClientIDMutation):
    class Input:
        keyword = graphene.String(required=True)
        path = graphene.String(required=True)

    # output
    icon = graphene.Field(IconType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        keyword = payload["keyword"]
        path = payload["path"]
        icon = models.Icon.objects.create(keyword=keyword, path=path)
        return CreateIcon(icon=icon)


class CreateEnum(relay.ClientIDMutation):
    class Input:
        icon = graphene.GlobalID(required=True)
        name = graphene.String(required=True)
        category = EnumEnumCategory(required=True)

    # output
    enum = graphene.Field(EnumCategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        _, icon_id = from_global_id(payload["icon"])
        icon = models.Icon.objects.get(id=icon_id)
        name = payload["name"]
        category = payload["category"]
        enum = models.EnumCategory.objects.create(icon=icon, name=name, category=category)
        return CreateEnum(enum=enum)


class CreateRecurringBill(relay.ClientIDMutation):
    class Input:
        frequency = EnumRecurringBillFrequency(required=True)
        recurring_month = graphene.Int(required=True)
        recurring_day = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        category = graphene.GlobalID(required=True)
        company = graphene.GlobalID(required=True)
        card = graphene.GlobalID(required=True)
        note = graphene.String(required=True)

    # output
    recurring_bill = graphene.Field(RecurringBillType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        frequency = payload["frequency"]
        recurring_month = payload["recurring_month"]
        recurring_day = payload["recurring_day"]
        amount = payload["amount"]

        _, category_id = from_global_id(payload["category"])
        category = models.EnumCategory.objects.get(id=category_id)
        _, company_id = from_global_id(payload["company"])
        company = models.EnumCategory.objects.get(id=company_id)
        _, card_id = from_global_id(payload["card"])
        card = models.EnumCategory.objects.get(id=card_id)

        note = payload["note"]

        recurring_bill = models.RecurringBill.objects.create(
            frequency=frequency,
            recurring_month=recurring_month,
            recurring_day=recurring_day,
            amount=amount,
            category=category,
            company=company,
            card=card,
            note=note
        )
        return CreateRecurringBill(recurring_bill=recurring_bill)


class CreateTransaction(relay.ClientIDMutation):
    class Input:
        amount = graphene.Float(required=True)
        category = graphene.GlobalID(required=True)
        company = graphene.GlobalID(required=True)
        card = graphene.GlobalID(required=True)
        note = graphene.String(required=True)

    # output
    transaction = graphene.Field(TransactionType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        amount = payload["amount"]

        _, category_id = from_global_id(payload["category"])
        category = models.EnumCategory.objects.get(id=category_id)
        _, company_id = from_global_id(payload["company"])
        company = models.EnumCategory.objects.get(id=company_id)
        _, card_id = from_global_id(payload["card"])
        card = models.EnumCategory.objects.get(id=card_id)

        note = payload["note"]

        transaction = models.Transaction.objects.create(
            amount=amount,
            category=category,
            company=company,
            card=card,
            note=note
        )

        return CreateTransaction(transaction=transaction)


class Mutation(graphene.ObjectType):
    create_icon = CreateIcon.Field()
    create_enum = CreateEnum.Field()
    create_recurring_bill = CreateRecurringBill.Field()
    create_transaction = CreateTransaction.Field()


class Query(graphene.ObjectType):
    """
    GraphQL schema
    """
    icon = Node.Field(IconType)
    all_icons = DjangoConnectionField(IconType)

    enum = Node.Field(EnumCategoryType)
    all_enums = DjangoConnectionField(EnumCategoryType)

    recurring_bill = Node.Field(RecurringBillType)
    all_recurring_bills = DjangoConnectionField(RecurringBillType)

    bill = Node.Field(TransactionType)
    all_bills = DjangoConnectionField(TransactionType)


# schema = graphene.Schema(query=Query)
schema = graphene.Schema(query=Query, mutation=Mutation)
