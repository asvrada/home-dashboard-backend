from graphene import Node, relay, Enum
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
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
    # overwrite field
    category = EnumEnumCategory()

    class Meta:
        model = models.EnumCategory
        interfaces = (Node,)
        filter_fields = ["name", "category", "icon"]

    def resolve_category(self, info, **kwargs):
        return self.category


class RecurringBillType(DjangoObjectType):
    # overwrite field
    frequency = EnumRecurringBillFrequency()

    class Meta:
        model = models.RecurringBill
        interfaces = (Node,)
        filter_fields = ["frequency", "recurring_month", "recurring_day",
                         "amount", "category", "company", "card", "note", "time_created"]

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


# Update
def get_id_from_global_id(global_id):
    if not global_id:
        return None

    return from_global_id(global_id)[1]


class UpdateIcon(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)
        keyword = graphene.String()
        path = graphene.String()

    # output
    icon = graphene.Field(IconType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        id = get_id_from_global_id(payload["id"])
        keyword = payload.get("keyword", None)
        path = payload.get("path", None)

        # Get object
        icon = models.Icon.objects.get(id=id)

        # Update object
        if keyword:
            icon.keyword = keyword

        if path:
            icon.path = path

        icon.save()
        return CreateIcon(icon=icon)


class UpdateEnum(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)
        icon = graphene.GlobalID()
        name = graphene.String()
        category = EnumEnumCategory()

    # output
    enum = graphene.Field(EnumCategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        id = get_id_from_global_id(payload["id"])
        _, icon_id = get_id_from_global_id(payload.get("icon", None))
        name = payload.get("name", None)
        category = payload.get("category", None)

        # Get object
        enum = models.EnumCategory.objects.get(id=id)

        # Update object
        if icon_id:
            icon = models.Icon.objects.get(id=icon_id)
            enum.icon = icon
        if name:
            enum.name = name
        if category:
            enum.category = category

        enum.save()
        return CreateEnum(enum=enum)


class UpdateRecurringBill(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)
        frequency = EnumRecurringBillFrequency()
        recurring_month = graphene.Int()
        recurring_day = graphene.Int()
        amount = graphene.Float()
        category = graphene.GlobalID(required=False)
        company = graphene.GlobalID(required=False)
        card = graphene.GlobalID(required=False)
        note = graphene.String()

    # output
    recurring_bill = graphene.Field(RecurringBillType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        id = get_id_from_global_id(payload["id"])
        frequency = payload.get("frequency", None)
        recurring_month = payload.get("recurring_month", None)
        recurring_day = payload.get("recurring_day", None)
        amount = payload.get("amount", None)

        category_id = get_id_from_global_id(payload.get("category", None))
        company_id = get_id_from_global_id(payload.get("company", None))
        card_id = get_id_from_global_id(payload.get("card", None))

        note = payload.get("note", None)

        # Get object
        recurring_bill = models.RecurringBill.objects.get(id=id)

        # Update object
        if frequency:
            recurring_bill.frequency = frequency
        if recurring_month:
            recurring_bill.recurring_month = recurring_month
        if recurring_day:
            recurring_bill.recurring_day = recurring_day
        if amount:
            recurring_bill.amount = amount
        if category_id:
            category = models.EnumCategory.objects.get(id=category_id)
            recurring_bill.category = category
        if company_id:
            company = models.EnumCategory.objects.get(id=company_id)
            recurring_bill.company = company
        if card_id:
            card = models.EnumCategory.objects.get(id=id)
            recurring_bill.card = card
        if note:
            recurring_bill.note = note

        recurring_bill.save()
        return CreateRecurringBill(recurring_bill=recurring_bill)


class UpdateTransaction(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)
        amount = graphene.Float()
        category = graphene.GlobalID(required=False)
        company = graphene.GlobalID(required=False)
        card = graphene.GlobalID(required=False)
        note = graphene.String()

    # output
    transaction = graphene.Field(TransactionType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        id = get_id_from_global_id(payload["id"])
        amount = payload.get("amount", None)

        category_id = get_id_from_global_id(payload.get("category", None))
        company_id = get_id_from_global_id(payload.get("company", None))
        card_id = get_id_from_global_id(payload.get("card", None))

        note = payload.get("note", None)

        # Get object
        bill = models.Transaction.objects.get(id=id)

        # Update object
        if amount:
            bill.amount = amount
        if category_id:
            category = models.EnumCategory.objects.get(id=category_id)
            bill.category = category
        if company_id:
            company = models.EnumCategory.objects.get(id=company_id)
            bill.company = company
        if card_id:
            card = models.EnumCategory.objects.get(id=id)
            bill.card = card
        if note:
            bill.note = note

        bill.save()
        return CreateTransaction(transaction=bill)


# Delete
class DeleteMutation(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)

    # output
    ok = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        str_type, id = from_global_id(payload["id"])

        dict_model_class = {
            "IconType": models.Icon,
            "EnumCategoryType": models.EnumCategory,
            "RecurringBillType": models.RecurringBill,
            "TransactionType": models.Transaction
        }

        model_class = dict_model_class[str_type]

        # delete
        count, result = model_class.objects.get(id=id).delete()
        if count != 1:
            raise Exception("Delete count is not 1 but ", count)

        return DeleteMutation(ok=f"Deleted {result}")


class Mutation(graphene.ObjectType):
    create_icon = CreateIcon.Field()
    create_enum = CreateEnum.Field()
    create_recurring_bill = CreateRecurringBill.Field()
    create_transaction = CreateTransaction.Field()

    delete = DeleteMutation().Field()

    update_icon = UpdateIcon.Field()
    update_enum = UpdateEnum.Field()
    update_recurring_bill = UpdateRecurringBill.Field()
    update_transaction = UpdateTransaction.Field()


class Query(graphene.ObjectType):
    """
    GraphQL schema
    """
    icon = Node.Field(IconType)
    icons = DjangoConnectionField(IconType)

    enum = Node.Field(EnumCategoryType)
    enums = DjangoConnectionField(EnumCategoryType)

    recurring_bill = Node.Field(RecurringBillType)
    recurring_bills = DjangoConnectionField(RecurringBillType)

    bill = Node.Field(TransactionType)
    bills = DjangoConnectionField(TransactionType)


# schema = graphene.Schema(query=Query)
schema = graphene.Schema(query=Query, mutation=Mutation)
