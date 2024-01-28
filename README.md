# Hook Technical Challenge

Repo made to house my answers to the Hook take-home technical challenge. Tests are in the tests/ folder and can be run using the built-in python unittest framework.

## Question 1

Originally, the function modified the input in place, leading to errors in the test as the second function call was taking a mutated version of `d` as an argument. By writing the result to its own variable instead of modifying the input, this bug is fixed and the test passes.

## Question 2

This solution uses python's built-in sorting to quickly find the biggest possible loss in one transaction. First, the list of prices is ordered, and a second list is created whose elements are tuples consisting of the prices in order and their index in the original list. Hence, the list can be thought of as ordered from "worst sell price" to "worst buy price". We then iterate through the "sell prices" and compare each one to each "buy price" in order - if the index of the buy price is smaller than the index of the sell price, we know we have found the biggest loss because the list is ordered, and we can exit the loop.

In the worst case, this solution is actually O(n^2) - where pricesLst is already sorted in ascending order, the function would have to iterate through every element of the input twice for each element. However, for highly randomized lists, this is much faster than my "v1" solution (can be seen in commit history), which was O(n^2 - n). For example, the test cases given took somewhere in the region of 0.5-0.6s to run for v1, as opposed to less than 0.1s for v2. So amusingly, the first version is actually marginally faster in the worst case - but the worst case is rare and the second version is faster in almost every other case.

## Question 3

This solution utilises a composition-over-inheritance approach to create a terse and easily extensible set of classes for simple SQL query building. The base classes `Filter`, `Column`, and `QueryBuilder` define the basic functionality of the query building. `QueryBuilder` implements methods to build a query from a list of columns and a table name. `Column` is responsible for implementing and controlling filtering functionality, as well as returning a name for `QueryBuilder` to build select statements. Building where statements is delegated to the `Filter` class - the `build_where` method on this base class is left blank as an indicator to developers that it is intended to be overriden.

Using this framework, it's simple to implement new filters, implement new columns, and mutate the available filters to each column. `Column` has an allowed_filters attribute that is used to raise an error when the wrong type of filter is used and can be easily modified to adjust column functionality. Children of `Filter` simply need to implement a `build_where` method which accepts a `column_name` as a parameter and returns a string - they can optionally also implement their own `__init__`methods to ensure inputs are of the correct type. Adding a new column is as simple as extending `Column`, providing a name and a list of `allowed_filters`.

The testing for this framework is also very developer-friendly. `ColumnFiltersTestCase` introspects the columns to check the `allowed_filters` and only test those, so just by modifying a column's `allowed_filters` attribute, the tests are automatically updated. New columns don't require new tests, they simply need to be added to the `COLUMNS` list in `ColumnFiltersTestCase`. New tests do need to be added to `FilterTestCase` (and `TestEdgeCases` as necessary) when implementing entirely new filtering functionality.
