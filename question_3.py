class Filter:
    value: str
    preceding_operator: str

    def __init__(self, value: str, preceding_operator: str = None):
        self.value = value
        self.preceding_operator = preceding_operator

    def build_where(self, column_name: str) -> str:
        pass


class Column:
    name: str
    filter: Filter
    allowed_filters: list[Filter] | str = "all"

    def __init__(self, name: str = None, filter: Filter = None):
        self.name = name if name else self.name
        if (
            self.allowed_filters != "all"
            and filter
            and filter.__class__ not in self.allowed_filters
        ):
            raise TypeError(f"Filter {filter} not allowed for column {self.name}")
        self.filter = filter

    def build_select(self) -> str:
        return self.name.strip().lower()


class QueryBuilder:
    def build_query(self, columns: list[Column], table_name: str) -> str:
        selects = []
        wheres = []
        for column in columns:
            selects.append(column.build_select())
            if column.filter:
                wheres.append(column.filter.build_where(column.name))

        query = self.combine_query_elements(selects, table_name, wheres)
        return query

    def combine_query_elements(
        self, selects: list[str], table_name: str, wheres: list[str] = None
    ) -> str:
        query = "select"
        selects = list(dict.fromkeys(selects))
        for select in selects:
            if selects.index(select) == len(selects) - 1:
                query += f" {select}"
            else:
                query += f" {select},"

        query += f" from {table_name.strip()}"

        if wheres:
            query += " where"

        for where in wheres:
            query += f" {where}"

        return query


class Equals(Filter):
    def __init__(self, value, preceding_operator: str = None):
        if isinstance(value, str):
            self.value = f"'{value}'"
        else:
            self.value = str(value)

        self.preceding_operator = preceding_operator

    def build_where(self, column_name: str) -> str:
        if self.preceding_operator:
            return f"{self.preceding_operator} {column_name} = {self.value}"

        return f"{column_name} = {self.value}"


class GreaterThan(Filter):
    def __init__(self, value, preceding_operator: str = None):
        if isinstance(value, str):
            self.value = f"'{value}'"
        else:
            self.value = str(value)

        self.preceding_operator = preceding_operator

    def build_where(self, column_name: str) -> str:
        if self.preceding_operator:
            return f"{self.preceding_operator} {column_name} > {self.value}"

        return f"{column_name} > {self.value}"


class LessThan(Filter):
    def __init__(self, value, preceding_operator: str = None):
        if isinstance(value, str):
            self.value = f"'{value}'"
        else:
            self.value = str(value)

        self.preceding_operator = preceding_operator

    def build_where(self, column_name: str) -> str:
        if self.preceding_operator:
            return f"{self.preceding_operator} {column_name} < {self.value}"

        return f"{column_name} < {self.value}"


class In(Filter):
    def __init__(self, value: list, preceding_operator: str = None):
        if not isinstance(value, list):
            raise TypeError("Value must be an array")

        array_str = "("
        for element in value:
            if value.index(element) == len(value) - 1:
                array_str += f"{element})"
            else:
                array_str += f"{element}, "
        self.value = array_str
        self.preceding_operator = preceding_operator

    def build_where(self, column_name: str) -> str:
        if self.preceding_operator:
            return f"{self.preceding_operator} {column_name} in {self.value}"
        else:
            return f"{column_name} in {self.value}"


class NotIn(Filter):
    def __init__(self, value, preceding_operator=None):
        if not isinstance(value, list):
            raise TypeError("Value must be an array")

        array_str = "("
        for element in value:
            if value.index(element) == len(value) - 1:
                array_str += f"{element})"
            else:
                array_str += f"{element}, "
        self.value = array_str
        self.preceding_operator = preceding_operator

    def build_where(self, column_name: str) -> str:
        if self.preceding_operator:
            return f"{self.preceding_operator} {column_name} not in {self.value}"
        else:
            return f"{column_name} not in {self.value}"


class Id(Column):
    name = "id"
    allowed_filters = "all"


class Url(Column):
    name = "url"
    allowed_filters = [Equals]


class Date(Column):
    name = "date"
    allowed_filters = [GreaterThan, LessThan, Equals]


class Rating(Column):
    name = "rating"
    allowed_filters = [GreaterThan, LessThan, Equals]
