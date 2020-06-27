from .setup import GraphQLBasicAPITestCase


class GraphQLIconTest(GraphQLBasicAPITestCase):
    def setUp(self):
        super().setUp()

        self.access_token = self.access_token_jeff
