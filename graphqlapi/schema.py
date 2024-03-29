import graphene
from django.utils.timezone import now
from graphene import Enum, relay, Int
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

from backend import exceptions, models

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
    skip = payload.get("skipSummaryFlag", None)

    return amount, category, company, card, note, skip


def update_fragment_given_payload(obj_fragment, payload):
    amount, category, company, card, note, skip = get_amount_category_company_card_note(payload)

    if amount is not None:
        obj_fragment.amount = amount
    obj_fragment.category = category
    obj_fragment.company = company
    obj_fragment.card = card
    if note is not None:
        obj_fragment.note = note
    if skip is not None:
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


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ["id", "email", "username", "has_password", "google_user_id", "icons", "enums", "rbs", "bills"]
        filter_fields = fields
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.is_authenticated:
            raise exceptions.PermissionDeniedException(exceptions.MESSAGE_PERMISSION_DENIED)
        return queryset.filter(pk=info.context.user.pk)


class IconType(DjangoObjectType):
    class Meta:
        model = models.Icon
        fields = "__all__"
        filter_fields = fields
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.is_authenticated:
            raise exceptions.PermissionDeniedException(exceptions.MESSAGE_PERMISSION_DENIED)
        return queryset.filter(user=info.context.user)


class EnumCategoryType(DjangoObjectType):
    # overwrite field
    category = EnumEnumCategory()

    count_bill = Int()

    class Meta:
        model = models.EnumCategory
        fields = "__all__"
        filter_fields = fields
        interfaces = (relay.Node,)

    def resolve_category(self, info, **kwargs):
        return self.category

    def resolve_count_bill(self: models.EnumCategory, info, **kwargs):
        table = {
            EnumEnumCategory.Category.value: self.bill_categories,
            EnumEnumCategory.Company.value: self.bill_companies,
            EnumEnumCategory.Card.value: self.bill_cards,
        }

        if self.category == EnumEnumCategory.NULL.value:
            raise Exception("Category of enum cannot be NUL")

        return len(table[self.category].all())

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.is_authenticated:
            raise exceptions.PermissionDeniedException(exceptions.MESSAGE_PERMISSION_DENIED)
        return queryset.filter(user=info.context.user)


class RecurringBillType(DjangoObjectType):
    # overwrite field
    frequency = EnumRecurringBillFrequency()

    class Meta:
        model = models.RecurringBill
        fields = "__all__"
        filter_fields = fields
        interfaces = (relay.Node,)

    def resolve_frequency(self, info, **kwargs):
        return self.frequency

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.is_authenticated:
            raise exceptions.PermissionDeniedException(exceptions.MESSAGE_PERMISSION_DENIED)
        return queryset.filter(user=info.context.user)


class TransactionType(DjangoObjectType):
    class Meta:
        model = models.Transaction
        fields = "__all__"
        filter_fields = fields
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        if not info.context.user.is_authenticated:
            raise exceptions.PermissionDeniedException(exceptions.MESSAGE_PERMISSION_DENIED)
        return queryset.filter(user=info.context.user)


# Create

class CreateIcon(relay.ClientIDMutation):
    class Input:
        keyword = graphene.String(required=True)
        path = graphene.String(required=True)

    # output
    icon = graphene.Field(IconType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **payload):
        user = info.context.user
        keyword = payload["keyword"]
        path = payload["path"]

        icon = models.Icon.objects.create(keyword=keyword, path=path, user=user)

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
        user = info.context.user
        icon = from_payload_to_object(payload, "icon", models.Icon)
        name = payload["name"]
        category = payload["category"]

        enum = models.EnumCategory.objects.create(icon=icon, name=name, category=category, user=user)

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
        user = info.context.user
        frequency = payload["frequency"]
        recurring_month = payload["recurring_month"]
        recurring_day = payload["recurring_day"]

        amount, category, company, card, note, skip = get_amount_category_company_card_note(payload)

        if skip is None:
            skip = 0

        recurring_bill = models.RecurringBill.objects.create(
            frequency=frequency,
            recurring_month=recurring_month,
            recurring_day=recurring_day,
            amount=amount,
            category=category,
            company=company,
            card=card,
            note=note,
            skip_summary_flag=skip,
            user=user
        )
        return CreateRecurringBill(recurring_bill=recurring_bill)


class CreateTransaction(relay.ClientIDMutation):
    class Input:
        amount = graphene.Float(required=True)
        # If missing (undefined), then set to None
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
        user = info.context.user
        amount, category, company, card, note, skip = get_amount_category_company_card_note(payload)
        time_created = payload.get("timeCreated", now())

        if skip is None:
            skip = 0

        transaction = models.Transaction.objects.create(
            amount=amount,
            category=category,
            company=company,
            card=card,
            note=note,
            skip_summary_flag=skip,
            time_created=time_created,
            user=user
        )

        return CreateTransaction(transaction=transaction)


"""
Update
"""


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
        return UpdateIcon(icon=icon)


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
        return UpdateEnum(enum=enum)


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
        return UpdateRecurringBill(recurring_bill=recurring_bill)


class UpdateTransaction(relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(required=True)
        amount = graphene.Float(required=False)
        # If missing (undefined), then set to None
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
        return UpdateTransaction(transaction=bill)


"""
Delete
"""


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
        objects = model_class.objects.filter(id=id)
        if objects:
            count, result = objects.delete()
        else:
            result = "None"

        return DeleteMutation(ok=f"Deleted {result}")


class Mutation(graphene.ObjectType):
    deleteObj = DeleteMutation().Field()

    create_icon = CreateIcon.Field()
    update_icon = UpdateIcon.Field()

    create_enum = CreateEnum.Field()
    update_enum = UpdateEnum.Field()

    create_recurring_bill = CreateRecurringBill.Field()
    update_recurring_bill = UpdateRecurringBill.Field()

    create_transaction = CreateTransaction.Field()
    update_transaction = UpdateTransaction.Field()


class Query(graphene.ObjectType):
    icon = relay.Node.Field(IconType)
    icons = DjangoFilterConnectionField(IconType)

    enum = relay.Node.Field(EnumCategoryType)
    enums = DjangoFilterConnectionField(EnumCategoryType)

    recurring_bill = relay.Node.Field(RecurringBillType)
    recurring_bills = DjangoFilterConnectionField(RecurringBillType)

    bill = relay.Node.Field(TransactionType)
    bills = DjangoFilterConnectionField(TransactionType)


schema = graphene.Schema(query=Query, mutation=Mutation)
