from .setup import GraphQLBasicAPITestCase


class GraphQLTransactionTest(GraphQLBasicAPITestCase):
    query_bills = """
    query getBills {
      bills {
        edges {
          node {
            id,
            amount,
            category {
              id
            },
            company {
              id
            },
            card {
              id
            },
            note,
            creator {
              id
            },
            timeCreated
          }
        }
      }
    }
    """

    query_bill = """
    query getBil($id: ID!) {
      bill(id: $id) {
        id,
        note,
        timeCreated
      }
    }
    """

    mutation_create_bill_min = """
    mutation createBill {
      createTransaction(input: {
        amount: -99
      }) {
        transaction {
          id,
          amount,
          company {
            id
          },
          category {
            id
          },
          card {
            id
          },
          note
        }
      }
    }
    """

    mutation_create_bill_max = """
    mutation createBill($cat: ID!, $com: ID!, $car: ID!) {
      createTransaction(input: {
        amount: -99
        category: $cat,
        company: $com,
        card: $car,
        note: "helene"
      }) {
        transaction {
          id,
          amount,
          company {
            id,
            name,
            category
          },
          category {
            id,
            name,
            category
          },
          card {
            id,
            name,
            category
          },
          note
        }
      }
    }
    """

    mutation_update_bill_min = """
    mutation updateBill($id: ID!) {
      updateTransaction(input: {
        id: $id
      }) {
        transaction {
          id,
          amount,
          note
        }
      }
    }
    """

    mutation_update_bill_max = """
    mutation updateBill($id: ID!, $cat: ID, $com: ID, $car: ID) {
      updateTransaction(input: {
        id: $id,
        amount: -9999,
        category: $cat,
        company: $com,
        card: $car,
        note: "New note"
      }) {
        transaction {
          id,
          amount,
          note
        }
      }
    }
    """

    def test_GIVEN_WHEN_get_transactions_THEN_return_all(self):
        # when
        response = self.query(self.query_bills)

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["bills"]["edges"]
        self.assertEqual(9, len(content))

    def test_GIVEN_WHEN_get_transaction_THEN_return_one(self):
        # when
        res = self.query(self.query_bill, variables={"id": self.id_valid_bill})

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["bill"]
        self.assertDictEqual(content, {
            "id": self.id_valid_bill,
            'note': "Test 12 Stock",
            'timeCreated': '2020-03-23T19:00:00+00:00'
        })

    def test_GIVEN_WHEN_create_transaction_min_THEN_bill_created(self):
        # when
        res = self.query(self.mutation_create_bill_min)

        # then
        self.assertResponseNoErrors(res)
        content = res.json()["data"]["createTransaction"]["transaction"]
        self.assertEqual(-99, content["amount"])

    def test_GIVEN_all_same_enum_WHEN_create_transaction_max_THEN_bill_created(self):
        # when
        res = self.query(self.mutation_create_bill_max, variables={
            "cat": self.id_valid_enum,
            "com": self.id_valid_enum,
            "car": self.id_valid_enum
        })

        # then
        self.assertResponseHasErrors(res)

    def test_GIVEN_WHEN_create_transaction_max_THEN_bill_created(self):
        # when
        res = self.query(self.mutation_create_bill_max, variables={
            "cat": self.id_valid_enum_category,
            "com": self.id_valid_enum_company,
            "car": self.id_valid_enum_card
        })

        # then
        self.assertResponseNoErrors(res)

    def test_GIVEN_WHEN_update_transaction_min_THEN_unchanged(self):
        # when
        res = self.query(self.mutation_update_bill_min, variables={"id": self.id_valid_bill})

        # then
        self.assertResponseNoErrors(res)

    def test_GIVEN_WHEN_update_transaction_max_THEN_updated(self):
        # when
        res = self.query(self.mutation_update_bill_max, variables={
            "id": self.id_valid_bill,
            "cat": self.id_valid_enum_category,
            "com": self.id_valid_enum_company,
            "car": self.id_valid_enum_card
        })

        # then
        self.assertResponseNoErrors(res)
