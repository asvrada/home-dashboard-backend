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
    query icon {
      icon(id: "%s") {
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
    mutation updateIcon {
      updateIcon(input: {
        id: "%s"
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
    mutation updateIcon {
      updateIcon(input: {
        id: "%s",
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
        response = self.post_query(self.query_icons)

        # then
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = response.json()["data"]["icons"]["edges"]
        self.assertEqual(1, len(content))

    def test_GIVEN_WHEN_get_icon_THEN_return_icon(self):
        # when
        response = self.post_query(self.query_icon % self.id_valid_icon)

        # then
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = response.json()["data"]["icon"]
        self.assertDictEqual(content, {
            "id": self.id_valid_icon,
            "keyword": "Test Icon id 1",
            "path": "/path/to/icon1"
        })

    def test_GIVEN_all_parameter_WHEN_create_icon_THEN_success(self):
        # when
        res = self.post_query(self.mutation_create_icon)

        # then
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        content = res.json()["data"]["createIcon"]["icon"]
        self.assertEqual(content["keyword"], "create keyword")
        self.assertEqual(content["path"], "create path")

    def test_GIVEN_min_parameter_WHEN_update_icon_THEN_success(self):
        # when
        res = self.post_query(self.mutation_update_icon_min % self.id_valid_icon)

        # then
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        content = res.json()["data"]["updateIcon"]["icon"]
        self.assertDictEqual(content, {
            "id": self.id_valid_icon,
            "keyword": "Test Icon id 1",
            "path": "/path/to/icon1"
        })

    def test_GIVEN_max_parameter_WHEN_update_icon_THEN_success(self):
        # when
        res = self.post_query(self.mutation_update_icon_max % self.id_valid_icon)

        # then
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        content = res.json()["data"]["updateIcon"]["icon"]
        self.assertDictEqual(content, {
            "id": self.id_valid_icon,
            "keyword": "update keyword",
            "path": "update path"
        })

    def test_GIVEN_existing_icon_WHEN_delete_THEN_icon_deleted(self):
        # when
        res = self.post_query(self.mutation_delete % self.id_valid_icon)

        # then
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        content = res.json()["data"]["delete"]
        self.assertIn("ok", content, msg="ok not in response")

        # check icon count
        res = self.post_query(self.query_icons)
        content = res.json()["data"]["icons"]["edges"]
        self.assertEqual(0, len(content))
