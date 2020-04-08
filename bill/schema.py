from graphene import relay
from graphene_django import DjangoObjectType
import graphene

from . import models


class EnumCategoryNode(DjangoObjectType):
    class Meta:
        model = models.EnumCategory
        interface = (relay.Node,)


class RecurringBillNode(DjangoObjectType):
    class Meta:
        model = models.RecurringBill
        interface = (relay.Node,)


class TransactionNode(DjangoObjectType):
    class Meta:
        model = models.Transaction
        interface = (relay.Node,)


class Query(graphene.ObjectType):
    """
    GraphQL schema
    """
    all_enums = graphene.List(EnumCategoryNode)
    all_recurring_bills = graphene.List(RecurringBillNode)
    all_bills = graphene.List(TransactionNode)

    enum = graphene.Field(EnumCategoryNode, id=graphene.Int())
    recurring_bill = graphene.Field(RecurringBillNode, id=graphene.Int())
    bill = graphene.Field(TransactionNode, id=graphene.Int())

    def resolve_all_enums(self, info):
        return models.EnumCategory.objects.all()

    def resolve_all_recurring_bills(self, info):
        return models.RecurringBill.objects.all()

    def resolve_all_bills(self, info):
        return models.Transaction.objects.all()

    def resolve_enum(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return models.EnumCategory.objects.get(pk=id)

        return None

    def resolve_recurring_bill(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return models.RecurringBill.objects.get(pk=id)

        return None

    def resolve_bill(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return models.Transaction.objects.get(pk=id)

        return None


schema = graphene.Schema(query=Query)
