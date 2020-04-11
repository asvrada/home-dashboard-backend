from graphene import Node, relay
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
import graphene

from . import models
from . import serializers


class IconType(DjangoObjectType):
    class Meta:
        model = models.Icon
        interfaces = (Node,)
        filter_fields = ["keyword", "path"]


class EnumCategoryType(DjangoObjectType):
    class Meta:
        model = models.EnumCategory
        interfaces = (Node,)
        filter_fields = ["name", "category", "icon"]


class RecurringBillType(DjangoObjectType):
    class Meta:
        model = models.RecurringBill
        interfaces = (Node,)
        filter_fields = ["frequency", "recurring_month", "recurring_day",
                         "amount", "category", "company", "card", "note", "time_created"]


class TransactionType(DjangoObjectType):
    class Meta:
        model = models.Transaction
        interfaces = (Node,)
        filter_fields = ["amount", "category", "company", "card", "note", "time_created"]


class IntroduceEnum(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        category = graphene.String(required=True)

    # output
    enum = graphene.Field(EnumCategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        name = payload["name"]
        category = payload["category"]
        enum = models.EnumCategory.objects.create(name=name, category=category)
        return IntroduceEnum(enum=enum)


class Mutation(graphene.ObjectType):
    create_enum = IntroduceEnum.Field()


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
