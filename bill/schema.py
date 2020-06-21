import graphene
import graphql_jwt
from django.utils.timezone import now
from graphene import relay, Enum
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id

from . import models

"""
Helper functions
"""


def from_payload_to_object(payload, key, model):
    if key not in payload:
        return None

    _, obj_id = from_global_id(payload[key])
    return model.objects.get(id=obj_id)


def get_id_from_global_id(global_id):
    if not global_id:
        return None

    return from_global_id(global_id)[1]


def get_amount_category_company_card_note(payload):
    amount = payload.get("amount", None)

    category = from_payload_to_object(payload, "category", models.EnumCategory)
    company = from_payload_to_object(payload, "company", models.EnumCategory)
    card = from_payload_to_object(payload, "card", models.EnumCategory)

    note = payload.get("note", None)
    skip = payload.get("skipSummaryFlag", False)

    return amount, category, company, card, note, skip


def update_fragment_given_payload(obj_fragment, payload):
    amount, category, company, card, note, skip = get_amount_category_company_card_note(payload)

    if amount:
        obj_fragment.amount = amount
    if category:
        obj_fragment.category = category
    if company:
        obj_fragment.company = company
    if card:
        obj_fragment.card = card
    if note:
        obj_fragment.note = note
    if skip:
        obj_fragment.skip_summary_flag = skip


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
        filter_fields = ["id", "keyword", "path"]
        interfaces = (relay.Node,)


class EnumCategoryType(DjangoObjectType):
    # overwrite field
    category = EnumEnumCategory()

    class Meta:
        model = models.EnumCategory
        filter_fields = ["id", "name", "category", "icon"]
        interfaces = (relay.Node,)

    @login_required
    def resolve_category(self, info, **kwargs):
        return self.category


class RecurringBillType(DjangoObjectType):
    # overwrite field
    frequency = EnumRecurringBillFrequency()

    class Meta:
        model = models.RecurringBill
        filter_fields = ["id", "frequency", "recurring_month", "recurring_day",
                         "amount", "category", "company", "card", "note", "skip_summary_flag", "time_created"]
        interfaces = (relay.Node,)

    def resolve_frequency(self, info, **kwargs):
        return self.frequency


class TransactionType(DjangoObjectType):
    class Meta:
        model = models.Transaction
        filter_fields = ["id", "amount", "category", "company", "card", "note", "skip_summary_flag", "creator",
                         "time_created"]
        interfaces = (relay.Node,)


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
        icon = graphene.GlobalID(required=False)
        name = graphene.String(required=True)
        category = EnumEnumCategory(required=True)

    # output
    enum = graphene.Field(EnumCategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        icon = from_payload_to_object(payload, "icon", models.Icon)
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
        category = graphene.GlobalID(required=False)
        company = graphene.GlobalID(required=False)
        card = graphene.GlobalID(required=False)
        note = graphene.String(required=False)
        skipSummaryFlag = graphene.Int(required=False)

    # output
    recurring_bill = graphene.Field(RecurringBillType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        frequency = payload["frequency"]
        recurring_month = payload["recurring_month"]
        recurring_day = payload["recurring_day"]

        amount, category, company, card, note, skip = get_amount_category_company_card_note(payload)

        recurring_bill = models.RecurringBill.objects.create(
            frequency=frequency,
            recurring_month=recurring_month,
            recurring_day=recurring_day,
            amount=amount,
            category=category,
            company=company,
            card=card,
            note=note,
            skip_summary_flag=skip
        )
        return CreateRecurringBill(recurring_bill=recurring_bill)


class CreateTransaction(relay.ClientIDMutation):
    class Input:
        amount = graphene.Float(required=True)
        category = graphene.GlobalID(required=False)
        company = graphene.GlobalID(required=False)
        card = graphene.GlobalID(required=False)
        note = graphene.String(required=False)
        skipSummaryFlag = graphene.Int(required=False)
        timeCreated = graphene.String(required=False)

    # output
    transaction = graphene.Field(TransactionType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        amount, category, company, card, note, skip = get_amount_category_company_card_note(payload)
        time_created = payload.get("timeCreated", now())

        transaction = models.Transaction.objects.create(
            amount=amount,
            category=category,
            company=company,
            card=card,
            note=note,
            skip_summary_flag=skip,
            time_created=time_created
        )

        return CreateTransaction(transaction=transaction)


# Update


class UpdateIcon(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)
        keyword = graphene.String(required=False)
        path = graphene.String(required=False)

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
        icon = graphene.GlobalID(required=False)
        name = graphene.String(required=False)
        category = EnumEnumCategory(required=False)

    # output
    enum = graphene.Field(EnumCategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        id = get_id_from_global_id(payload["id"])
        icon = from_payload_to_object(payload, "icon", models.Icon)
        name = payload.get("name", None)
        category = payload.get("category", None)

        # Get object
        enum = models.EnumCategory.objects.get(id=id)

        # Update object
        if icon:
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
        frequency = EnumRecurringBillFrequency(required=False)
        recurring_month = graphene.Int(required=False)
        recurring_day = graphene.Int(required=False)
        amount = graphene.Float(required=False)
        category = graphene.GlobalID(required=False)
        company = graphene.GlobalID(required=False)
        card = graphene.GlobalID(required=False)
        note = graphene.String(required=False)
        skipSummaryFlag = graphene.Int(required=False)

    # output
    recurring_bill = graphene.Field(RecurringBillType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        id = get_id_from_global_id(payload["id"])
        frequency = payload.get("frequency", None)
        recurring_month = payload.get("recurring_month", None)
        recurring_day = payload.get("recurring_day", None)

        # Get object
        recurring_bill = models.RecurringBill.objects.get(id=id)

        # Update object
        update_fragment_given_payload(recurring_bill, payload)

        if frequency:
            recurring_bill.frequency = frequency
        if recurring_month:
            recurring_bill.recurring_month = recurring_month
        if recurring_day:
            recurring_bill.recurring_day = recurring_day

        recurring_bill.save()
        return CreateRecurringBill(recurring_bill=recurring_bill)


class UpdateTransaction(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)
        amount = graphene.Float(required=False)
        category = graphene.GlobalID(required=False)
        company = graphene.GlobalID(required=False)
        card = graphene.GlobalID(required=False)
        note = graphene.String(required=False)
        skipSummaryFlag = graphene.Int(required=False)
        timeCreated = graphene.String(required=False)

    # output
    transaction = graphene.Field(TransactionType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        id = get_id_from_global_id(payload["id"])

        # Get object
        bill = models.Transaction.objects.get(id=id)

        # update object
        update_fragment_given_payload(bill, payload)

        time_created = payload.get("timeCreated", None)

        if time_created:
            bill.time_created = time_created

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
    token_verify = graphql_jwt.Verify.Field()

    create_icon = CreateIcon.Field()
    create_enum = CreateEnum.Field()
    create_recurring_bill = CreateRecurringBill.Field()
    create_transaction = CreateTransaction.Field()

    deleteObj = DeleteMutation().Field()

    update_icon = UpdateIcon.Field()
    update_enum = UpdateEnum.Field()
    update_recurring_bill = UpdateRecurringBill.Field()
    update_transaction = UpdateTransaction.Field()


class Query(graphene.ObjectType):
    icon = relay.Node.Field(IconType)
    icons = DjangoConnectionField(IconType)

    enum = relay.Node.Field(EnumCategoryType)
    enums = DjangoConnectionField(EnumCategoryType)

    recurring_bill = relay.Node.Field(RecurringBillType)
    recurring_bills = DjangoConnectionField(RecurringBillType)

    bill = relay.Node.Field(TransactionType)
    bills = DjangoConnectionField(TransactionType)


schema = graphene.Schema(query=Query, mutation=Mutation)
