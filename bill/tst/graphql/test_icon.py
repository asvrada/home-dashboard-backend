from rest_framework import status

from .setup import GraphQLBasicAPITestCase


class GraphQLIconTest(GraphQLBasicAPITestCase):
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

    query_icon = """
    query icon($id: ID!) {
      icon(id: $id) {
        id,
        path,
        keyword
      }
    }
    """

    mutation_create_icon = """
    mutation createIcon {
      createIcon(input: {
        keyword: "create keyword",
        path: "create path"
      }) {
        icon {
          id,
          keyword,
          path
        }
      }
    }
    """

    mutation_update_icon_min = """
    mutation updateIcon($id: ID!) {
      updateIcon(input: {
        id: $id
      }) {
        icon {
          id,
          keyword,
          path
        }
      }
    }
    """

    mutation_update_icon_max = """
    mutation updateIcon($id: ID!) {
      updateIcon(input: {
        id: $id,
        keyword: "update keyword",
        path: "update path"
      }) {
        icon {
          id,
          keyword,
          path
        }
      }
    }
    """

    def test_GIVEN_WHEN_get_icons_THEN_return_all(self):
        # when
        response = self.query(self.query_icons)

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["icons"]["edges"]
        self.assertEqual(2, len(content))

    def test_GIVEN_WHEN_get_icon_THEN_return_icon(self):
        # when
        response = self.query(self.query_icon, variables={"id": self.id_valid_icon})

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["icon"]
        self.assertDictEqual(content, {
            "id": self.id_valid_icon,
            "keyword": "Test Icon 2",
            "path": "/path/icon 2"
        })

    def test_GIVEN_all_parameter_WHEN_create_icon_THEN_success(self):
        # when
        res = self.query(self.mutation_create_icon)

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["createIcon"]["icon"]
        self.assertEqual(content["keyword"], "create keyword")
        self.assertEqual(content["path"], "create path")

    def test_GIVEN_min_parameter_WHEN_update_icon_THEN_success(self):
        # when
        res = self.query(self.mutation_update_icon_min, variables={"id": self.id_valid_icon})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["updateIcon"]["icon"]
        self.assertDictEqual(content, {
            "id": self.id_valid_icon,
            "keyword": "Test Icon 2",
            "path": "/path/icon 2"
        })

    def test_GIVEN_max_parameter_WHEN_update_icon_THEN_success(self):
        # when
        res = self.query(self.mutation_update_icon_max, variables={"id": self.id_valid_icon})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["updateIcon"]["icon"]
        self.assertDictEqual(content, {
            "id": self.id_valid_icon,
            "keyword": "update keyword",
            "path": "update path"
        })

    def test_GIVEN_existing_icon_WHEN_delete_THEN_icon_deleted(self):
        # when
        res = self.query(self.mutation_delete, variables={"id": self.id_valid_icon})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["deleteObj"]
        self.assertIn("ok", content, msg="ok not in response")

        # check icon count
        res = self.query(self.query_icons)
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["icons"]["edges"]
        self.assertEqual(1, len(content))
