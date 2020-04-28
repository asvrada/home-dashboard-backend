from rest_framework import status

from ..setup import BasicAPITestCase


class GraphQLEnumTest(BasicAPITestCase):
    endpoint = "/graphql/"

    id_enum = "RW51bUNhdGVnb3J5VHlwZTo3"

    query_enums = """
    query getEnums {
      enums {
        edges {
          node {
            id,
            category,
            name,
            icon {
              id,
              path,
              keyword
            }
          }
        }
      }
    }
    """

    query_enum = """
    query getEnum {
      enum(id: "%s") {
        id,
        name,
        category,
        icon {
          id,
          path,
          keyword
        }
      }
    }
    """ % id_enum

    mutation_create_enum = """
    mutation createEnum {
      createEnum(input: {
        category: Company,
        name: "APITest created"
      }) {
        enum {
          category,
          name
        }
      }
    }
    """

    mutation_delete_enum = """
    mutation delete {
      delete(input: {
        id: "%s"
      }) {
        ok
      }
    }
    """ % id_enum

    def test_GIVEN_WHEN_get_enums_THEN_return_all(self):
        # when
        response = self.client.get(self.endpoint, data={'query': self.query_enums}, format="json")

        # then
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = response.json()["data"]["enums"]["edges"]
        self.assertEqual(16, len(content))

    def test_GIVEN_WHEN_get_any_enum_THEN_return_that_enum(self):
        # when
        res = self.client.get(self.endpoint, data={'query': self.query_enum}, format="json")

        # then
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        content = res.json()["data"]["enum"]
        self.assertEqual(content, {
            "id": 'RW51bUNhdGVnb3J5VHlwZTo3',
            "category": "Company",
            "name": "",
            "icon": None
        })

    def test_GIVEN_new_enum_WHEN_create_enum_THEN_enum_created(self):
        # when
        res = self.client.post(self.endpoint, data={'query': self.mutation_create_enum}, format="json")

        # then
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        content = res.json()["data"]["createEnum"]["enum"]
        self.assertEqual(content, {
            "category": "Company",
            "name": "APITest created"
        })

    def test_GIVEN_existing_enum_WHEN_delete_THEN_enum_deleted(self):
        # when
        res = self.client.post(self.endpoint, data={'query': self.mutation_delete_enum}, format="json")

        # then
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        content = res.json()["data"]["delete"]
        self.assertIn("ok", content, msg="ok not in response")
