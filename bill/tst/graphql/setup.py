from ..setup import BasicAPITestCase


class GraphQLBasicAPITestCase(BasicAPITestCase):
    endpoint = "/graphql/"
    id_valid_icon = "SWNvblR5cGU6MQ=="
    id_valid_enum = "RW51bUNhdGVnb3J5VHlwZTo3"

    mutation_delete = """
    mutation delete {
      delete(input: {
        id: "%s"
      }) {
        ok
      }
    }
    """

    def setUp(self):
        super().setUp()

    def post_query(self, query):
        return self.client.post(self.endpoint, data={'query': query}, format="json")
