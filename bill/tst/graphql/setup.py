from django.urls import reverse
from graphene_django.utils.testing import GraphQLTestCase
from rest_framework import status

from bill.tst.setup import setup_db
from bill.schema import schema


class GraphQLBasicAPITestCase(GraphQLTestCase):
    accessToken = None

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

        admin, jeff = setup_db()

        # get access token
        url = reverse('token_auth')
        res = self.client.post(url, {'username': 'jeff', 'password': '4980'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in res.data)
        self.accessToken = res.data['access']

