from .setup import GraphQLBasicAPITestCase


class GraphQLIconTest(GraphQLBasicAPITestCase):
    query_rb = """
    query recurringBill($id: ID!) {
      recurringBill(id: $id) {
        id,
        amount,
        recurringMonth,
        recurringDay
      }
    }
    """

    query_rbs = """
    query recurringBills {
      recurringBills {
        edges {
          node {
            id,
            recurringDay,
            recurringMonth,
            note,
            timeCreated
          }
        }
      }
    }
    """

    mutation_create_rb_min = """
    mutation create_rb_min($fre: EnumRecurringBillFrequency!, $month: Int!, $day: Int!, $amount: Float!) {
      createRecurringBill(input: {
        frequency: $fre,
        recurringMonth: $month,
        recurringDay: $day,
        amount: $amount
      }) {
        recurringBill {
          id,
          user {
            id,
            email,
            username,
            hasPassword,
            googleUserId
          },
          frequency,
          recurringMonth,
          recurringDay,
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
          skipSummaryFlag,
          timeCreated
        }
      } 
    }
    """

    mutation_create_rb_max = """
    mutation create_rb_max(
      $fre: EnumRecurringBillFrequency!, 
      $month: Int!, 
      $day: Int!, 
      $amount: Float!,
      $cat: ID,
      $com: ID,
      $car: ID
    ) {
      createRecurringBill(input: {
        frequency: $fre,
        recurringMonth: $month,
        recurringDay: $day,
        amount: $amount,
        category: $cat,
        company: $com,
        card: $car,
        note: "some note",
        skipSummaryFlag: 3
      }) {
        recurringBill {
          id,
          user {
            id,
            email,
            username,
            hasPassword,
            googleUserId
          },
          frequency,
          recurringMonth,
          recurringDay,
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
          skipSummaryFlag,
          timeCreated
        }
      } 
    }
    """

    mutation_update_rb_min = """
    mutation update_rb_min(
      $id: ID!
    ) {
      updateRecurringBill(input: {
        id: $id
      }) {
        recurringBill {
          id,
          user {
            id,
            email,
            username,
            hasPassword,
            googleUserId
          },
          frequency,
          recurringMonth,
          recurringDay,
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
          skipSummaryFlag,
          timeCreated
        }
      } 
    }
    """

    mutation_update_rb_max = """
    mutation update_rb_max(
      $id: ID!,
      $fre: EnumRecurringBillFrequency, 
      $month: Int, 
      $day: Int, 
      $amount: Float,
      $category: ID,
      $company: ID,
      $card: ID
    ) {
      updateRecurringBill(input: {
        id: $id,
        frequency: $fre,
        recurringMonth: $month,
        recurringDay: $day,
        amount: $amount,
        category: $category,
        company: $company,
        card: $card,
        note: "some note",
        skipSummaryFlag: 3
      }) {
        recurringBill {
          id,
          user {
            id,
            email,
            username,
            hasPassword,
            googleUserId
          },
          frequency,
          recurringMonth,
          recurringDay,
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
          skipSummaryFlag,
          timeCreated
        }
      } 
    }
    """

    def setUp(self):
        super().setUp()

        self.access_token = self.access_token_jeff

    def test_WHEN_query_rb_THEN_return(self):
        # when
        response = self.query(self.query_rb, variables={"id": self.id_valid_recurring_bill})

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["recurringBill"]
        self.assertDictEqual({
            'amount': 456.0,
            'id': 'UmVjdXJyaW5nQmlsbFR5cGU6Mg==',
            'recurringDay': 2,
            'recurringMonth': 1
        }, content)

    def test_GIVEN_wrong_account_WHEN_query_rb_THEN_no_result(self):
        self.access_token = self.access_token_admin

        # when
        response = self.query(self.query_rb, variables={"id": self.id_valid_recurring_bill})

        # then
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertEqual(None, content["data"]["recurringBill"])

    def test_WHEN_query_rbs_THEN_all_return(self):
        # when
        response = self.query(self.query_rbs)

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["recurringBills"]["edges"]
        self.assertEqual(2, len(content))

    def test_GIVEN_min_param_WHEN_create_rb_THEN_created(self):
        # when
        response = self.query(self.mutation_create_rb_min, variables={
            "fre": "Month",
            "month": 10,
            "day": 10,
            "amount": 2022.12,
        })

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["createRecurringBill"]["recurringBill"]
        self.assertIn("amount", content)
        self.assertIn("user", content)
        self.assertIsNotNone(content["user"])
        self.assertIn("note", content)

    def test_GIVEN_max_param_WHEN_create_rb_THEN_created(self):
        # when
        response = self.query(self.mutation_create_rb_max, variables={
            "fre": "Year",
            "month": 10,
            "day": 10,
            "amount": 2022.12,
            "cat": self.id_valid_enum_category,
            "com": self.id_valid_enum_company,
            "car": self.id_valid_enum_card
        })

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["createRecurringBill"]["recurringBill"]
        self.assertIn("amount", content)
        self.assertIsNotNone(content["user"])
        self.assertIsNotNone(content["category"])
        self.assertIsNotNone(content["company"])
        self.assertIsNotNone(content["card"])
        self.assertIn("note", content)

    def test_GIVEN_max_param_WHEN_update_rb_THEN_updated(self):
        # when
        response = self.query(self.mutation_update_rb_max, variables={
            "id": self.id_valid_recurring_bill,
            "fre": "Year",
            "month": 10,
            "day": 10,
            "amount": 2022.12,
            "category": self.id_valid_enum_category,
            "company": self.id_valid_enum_company,
            "card": self.id_valid_enum_card
        })

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["updateRecurringBill"]["recurringBill"]
        self.assertEqual(2022.12, content["amount"])
        self.assertIsNotNone(content["user"])
        self.assertEqual(self.id_valid_enum_category, content["category"]["id"])
        self.assertEqual(self.id_valid_enum_company, content["company"]["id"])
        self.assertEqual(self.id_valid_enum_card, content["card"]["id"])
        self.assertEqual("some note", content["note"])

    def test_GIVEN_min_param_WHEN_update_rb_THEN_not_changed(self):
        # when
        response = self.query(self.mutation_update_rb_min, variables={
            "id": self.id_valid_recurring_bill,
        })

        # then
        self.assertResponseNoErrors(response)
        content = response.json()["data"]["updateRecurringBill"]["recurringBill"]
        self.assertIsNotNone(content)
