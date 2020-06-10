
from .setup import GraphQLBasicAPITestCase


class GraphQLEnumTest(GraphQLBasicAPITestCase):
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
    query getEnum($id: ID!) {
      enum(id: $id) {
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
    """

    mutation_create_enum_min = """
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

    mutation_create_enum_max = """
    mutation createEnum($icon: ID!) {
      createEnum(input: {
        icon: $icon,
        category: Company,
        name: "APITest created"
      }) {
        enum {
          icon {
            id,
            keyword,
            path
          },
          category,
          name
        }
      }
    }
    """

    mutation_update_enum_min = """
    mutation updateEnum($id: ID!) {
      updateEnum(input: {
        id: $id,
      }) {
        enum {
          id,
          icon {
            id
          },
          category,
          name
        }
      }
    }
    """

    mutation_update_enum_max = """
    mutation updateEnum($id: ID!, $icon: ID) {
      updateEnum(input: {
        id: $id,
        icon: $icon,
        name: "update name",
        category: Card
      }) {
        enum {
          id,
          icon {
            id
          },
          category,
          name
        }
      }
    }
    """

    def test_GIVEN_WHEN_get_enums_THEN_return_all(self):
        # when
        response = self.query(self.query_enums)

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["enums"]["edges"]
        self.assertEqual(4, len(content))

    def test_GIVEN_WHEN_get_enum_THEN_return_that_enum(self):
        # when
        res = self.query(self.query_enum, variables={"id": self.id_valid_enum})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["enum"]
        self.assertEqual(self.id_valid_enum, content["id"])
        self.assertEqual("Card", content["category"])
        self.assertEqual("Test Card 1", content["name"])
        self.assertIn("icon", content)

    def test_GIVEN_min_parameter_WHEN_create_enum_THEN_enum_created(self):
        # when
        res = self.query(self.mutation_create_enum_min)

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["createEnum"]["enum"]
        self.assertDictEqual(content, {
            "category": "Company",
            "name": "APITest created"
        })

    def test_GIVEN_max_parameter_WHEN_create_enum_THEN_enum_created(self):
        # when
        res = self.query(self.mutation_create_enum_max, variables={"icon": self.id_valid_icon})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["createEnum"]["enum"]
        self.assertIn("icon", content)
        self.assertIn("category", content)
        self.assertIn("name", content)

    def test_GIVEN_min_parameter_WHEN_update_enum_THEN_enum_unchanged(self):
        # when
        res = self.query(self.mutation_update_enum_min, variables={"id": self.id_valid_enum})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["updateEnum"]["enum"]
        self.assertIn("icon", content)
        self.assertIn("category", content)
        self.assertIn("name", content)

    def test_GIVEN_max_parameter_WHEN_update_enum_THEN_enum_updated(self):
        # when
        res = self.query(self.mutation_update_enum_max, variables={
            "id": self.id_valid_enum,
            "icon": self.id_valid_icon
        })

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["updateEnum"]["enum"]
        self.assertDictEqual(content, {
            "id": self.id_valid_enum,
            "icon": {
                "id": self.id_valid_icon
            },
            "category": "Card",
            "name": "update name"
        })

    def test_GIVEN_existing_enum_WHEN_delete_THEN_enum_deleted(self):
        # when
        res = self.query(self.mutation_delete, variables={"id": self.id_valid_enum})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["deleteObj"]
        self.assertIn("ok", content, msg="ok not in response")

        # check icon count
        res = self.query(self.query_enums)
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["enums"]["edges"]
        self.assertEqual(3, len(content))
