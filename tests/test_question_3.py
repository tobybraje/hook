import unittest

import question_3


class TestEdgeCases(unittest.TestCase):
    def test_two_columns(self):
        builder = question_3.QueryBuilder()

        id_filter = question_3.GreaterThan(3)
        id_column = question_3.Id(filter=id_filter)

        url_filter = question_3.Equals("fakeurl.com", preceding_operator="and")
        url_column = question_3.Url(filter=url_filter)

        query = builder.build_query([id_column, url_column], "table")

        self.assertEqual(
            query, "select id, url from table where id > 3 and url = 'fakeurl.com'"
        )

    def test_no_filters(self):
        builder = question_3.QueryBuilder()

        id_column = question_3.Id()
        url_column = question_3.Url()

        query = builder.build_query([id_column, url_column], "table")

        self.assertEqual(query, "select id, url from table")

    def test_two_filters_same_column(self):
        builder = question_3.QueryBuilder()

        filter_1 = question_3.GreaterThan(3)
        column_1 = question_3.Id(filter=filter_1)

        filter_2 = question_3.LessThan(7, preceding_operator="and")
        column_2 = question_3.Id(filter=filter_2)

        query = builder.build_query([column_1, column_2], "table")

        self.assertEqual(query, "select id from table where id > 3 and id < 7")

    def test_can_only_filter_with_allowed_filters(self):
        filter = question_3.GreaterThan(3)

        with self.assertRaises(TypeError):
            column = question_3.Url(filter=filter)

    def test_array_filters_only_accept_arrays(self):
        with self.assertRaises(TypeError):
            filter = question_3.In(3)

        with self.assertRaises(TypeError):
            filter = question_3.NotIn(3)


class FilterTestCase(unittest.TestCase):
    def equals_int(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.Equals(value=3)
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query, f"select {column.name} from table where {column.name} = 3"
        )

    def equals_str(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.Equals(value="string")
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query, f"select {column.name} from table where {column.name} = 'string'"
        )

    def greater_than_int(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.GreaterThan(value=3)
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query, f"select {column.name} from table where {column.name} > 3"
        )

    def greater_than_str(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.GreaterThan(value="3 Jan 2024")
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query, f"select {column.name} from table where {column.name} > '3 Jan 2024'"
        )

    def less_than_int(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.LessThan(value=3)
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query, f"select {column.name} from table where {column.name} < 3"
        )

    def less_than_str(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.LessThan(value="3 Jan 2024")
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query, f"select {column.name} from table where {column.name} < '3 Jan 2024'"
        )

    def in_(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.In(value=[3, 4, 5])
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query, f"select {column.name} from table where {column.name} in (3, 4, 5)"
        )

    def not_in(self, column: question_3.Column):
        builder = question_3.QueryBuilder()

        filter = question_3.NotIn(value=[3, 4, 5])
        column.filter = filter

        query = builder.build_query([column], "table")

        self.assertEqual(
            query,
            f"select {column.name} from table where {column.name} not in (3, 4, 5)",
        )


class ColumnFiltersTestCase(unittest.TestCase):
    filter_tests = FilterTestCase()
    FILTER_TEST_MAPPING = {
        question_3.Equals: [filter_tests.equals_int, filter_tests.equals_str],
        question_3.GreaterThan: [
            filter_tests.greater_than_int,
            filter_tests.greater_than_str,
        ],
        question_3.LessThan: [filter_tests.less_than_int, filter_tests.less_than_str],
        question_3.In: [filter_tests.in_],
        question_3.NotIn: [filter_tests.not_in],
        "all": [
            filter_tests.equals_int,
            filter_tests.equals_str,
            filter_tests.greater_than_int,
            filter_tests.greater_than_str,
            filter_tests.less_than_int,
            filter_tests.less_than_str,
            filter_tests.in_,
            filter_tests.not_in,
        ],
    }

    COLUMNS = [
        question_3.Id(),
        question_3.Url(),
        question_3.Date(),
        question_3.Rating(),
    ]

    def test_all_column_filters(self):
        for column in self.COLUMNS:
            tests = []
            if column.allowed_filters == "all":
                for test in self.FILTER_TEST_MAPPING[column.allowed_filters]:
                    tests.append(test)
            else:
                for filter in column.allowed_filters:
                    for test in self.FILTER_TEST_MAPPING[filter]:
                        tests.append(test)

            for test in tests:
                test(column)


if __name__ == "__main__":
    unittest.main()
