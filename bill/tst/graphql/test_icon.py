from rest_framework import status

from ..setup import BasicAPITestCase


class GraphQLIconTest(BasicAPITestCase):
    endpoint = "/graphql/"

    id_icon = ""

    query_icons = """
    query icons {
      icons {
        edges {
          node {
            id,
            keyword,
            path
          }
        }
      }
    }
    """

    pass
