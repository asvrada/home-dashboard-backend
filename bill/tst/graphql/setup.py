from graphene_django.utils.testing import GraphQLTestCase

from bill.tst.setup import setup_db
from bill.schema import schema


class GraphQLBasicAPITestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    id_valid_icon = 'SWNvblR5cGU6Mg=='
    id_valid_enum = "RW51bUNhdGVnb3J5VHlwZTo0"
    id_valid_enum_company = 'RW51bUNhdGVnb3J5VHlwZToz'
    id_valid_enum_category = 'RW51bUNhdGVnb3J5VHlwZTox'
    id_valid_enum_card = "RW51bUNhdGVnb3J5VHlwZTo0"
    id_valid_bill = 'VHJhbnNhY3Rpb25UeXBlOjM='

    mutation_delete = """
    mutation delete($id: ID!) {
      deleteObj(input: {
        id: $id
      }) {
        ok
      }
    }
    """

    def setUp(self):
        super().setUp()

        setup_db()
