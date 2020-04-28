import json

from graphene_django.utils.testing import GraphQLTestCase

from bill.tst.setup import setup_db
from bill.schema import schema


class GraphQLBasicAPITestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    id_valid_icon = "SWNvblR5cGU6MQ=="
    id_valid_enum = "RW51bUNhdGVnb3J5VHlwZTo3"

    mutation_delete = """
    mutation delete($id: ID!) {
      delete(input: {
        id: $id
      }) {
        ok
      }
    }
    """

    def setUp(self):
        super().setUp()

        setup_db()
