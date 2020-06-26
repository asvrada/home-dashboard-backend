from graphene_django.utils.testing import GraphQLTestCase

from backend.schema import schema
from ..setup import BasicAPITestCase


class GraphQLBasicAPITestCase(BasicAPITestCase, GraphQLTestCase):
    access_token = None

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

    def query(self, query, op_name=None, input_data=None, variables=None, headers=None):
        if headers is None:
            headers = dict()

        if self.access_token is not None:
            headers.update({
                "HTTP_AUTHORIZATION": "Bearer " + self.access_token
            })

        return super(GraphQLBasicAPITestCase, self).query(query, op_name, input_data, variables, headers)
