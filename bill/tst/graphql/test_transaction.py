from .setup import GraphQLBasicAPITestCase


class GraphQLTransactionTest(GraphQLBasicAPITestCase):
    query_bills = ""

    query_bill = ""

    mutation_create_bill_min = ""

    mutation_create_bill_max = ""

    mutation_update_bill_min = ""

    mutation_update_bill_max = ""

    def test_GIVEN_WHEN_get_icons_THEN_return_all(self):
        pass
