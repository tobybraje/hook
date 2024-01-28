# Hook Technical Challenge

Repo made to house my answers to the Hook take-home technical challenge. Tests are in the tests/ folder and can be run using the built-in python unittest framework.

## Question 1

Originally, the function modified the input in place, leading to errors in the test as the second function call was taking a mutated version of `d` as an argument. By writing the result to its own variable instead of modifying the input, this bug is fixed and the test passes.

## Question 2

This solution is fairly straightforward. For each price in the list, we calculate the loss for that buy price and every subsequent sell price. We keep track of the biggest loss so far and replace it if it is exceeded - ditto for the indexes of the prices comprising the transaction with the highest loss. After getting through all the prices, we have the highest possible loss (as a negative number) and the indexes of the prices that produced it. We round the biggest loss to 2 decimal places (because it is a price difference) and multiply it by negative one to make it positive, and we are done.

This solution is O(n^2 - n), so it is slow for large values of n i.e. for large price lists. One potential method for speeding this function up could involve creating a dictionary with the prices as keys and their indices as values, then sorting the dictionary according to prices and finding the two key-value pairs with the greatest distance between them that still satisfy the condition of index1 < index2.

## Question 3

This solution utilises a composition-over-inheritance approach to create a terse and easily extensible set of classes for simple SQL query building. The base classes `Filter`, `Column`, and `QueryBuilder` define the basic functionality of the query building. `QueryBuilder` implements methods to build a query from a list of columns and a table name. `Column` is responsible for implementing and controlling filtering functionality, as well as returning a name for `QueryBuilder` to build select statements. Building where statements is delegated to the `Filter` class - the `build_where` method on this base class is left blank as an indicator to developers that it is intended to be overriden.

Using this framework, it's simple to implement new filters, implement new columns, and mutate the available filters to each column. `Column` has an allowed_filters attribute that is used to raise an error when the wrong type of filter is used and can be easily modified to adjust column functionality. Children of `Filter` simply need to implement a `build_where` method which accepts a `column_name` as a parameter and returns a string - they can optionally also implement their own `__init__`methods to ensure inputs are of the correct type. Adding a new column is as simple as extending `Column`, providing a name and a list of `allowed_filters`.

The testing for this framework is also very developer-friendly. `ColumnFiltersTestCase` introspects the columns to check the `allowed_filters` and only test those, so just by modifying a column's `allowed_filters` attribute, the tests are automatically updated. New columns don't require new tests, they simply need to be added to the `COLUMNS` list in `ColumnFiltersTestCase`. New tests do need to be added to `FilterTestCase` (and `TestEdgeCases` as necessary) when implementing entirely new filtering functionality.
