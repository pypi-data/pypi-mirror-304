Here’s a more organized and clear version of your README.md file:
MySQL Module

A Python module for managing MySQL databases, offering methods to connect, create databases, insert data, and more.

## Installation


Install the module via pip:

```bash
pip install mysql_module

```

## Usage

# Connecting to a MySQL Database

First, import the module and create an instance to connect to the database:

```python
from mysql_module import MySQLModule
```
## Create an instance of MySQLModule

```python
db = MySQLModule(hostname="localhost", username="root", password="your_password")
```
## Connect to the database
db.connect_to_database()

# Creating a Database

Once connected, you can create a new database using the following function:

```python
db.create_database("buyer")
```
Replace "buyer" with the name of the database you wish to create.
# Creating a Table

To create a table in your MySQL database, use the create_table() function. Below is an example:

## SQL query for creating the table

```python

create_my_table = """
CREATE TABLE IF NOT EXISTS fuhj (
    o_id INT AUTO_INCREMENT PRIMARY KEY,
    o_f_name VARCHAR(100),
    o_l_name VARCHAR(100),
    hourly_pay DECIMAL(10, 2),
    price DECIMAL(10, 2),
    comman_rate DECIMAL(10, 2)
)
"""

# Table name
my_table_name = "fuhj"

# Create the table
db.create_table(create_my_table, my_table_name)
```

This will create the fuhj table in your MySQL database if it doesn't already exist.
# Listing Databases and Tables

To display all the databases and tables in your MySQL server, use the following functions.

Show Databases:

## Retrieve and print the list of databases

```python

databases = db.show_databases()
if databases:
    print("Databases:")
    for db_name in databases:
        print(db_name[0])

```

## Show Tables:

```python

if db.connect_to_database():
    print("Connected successfully!")
    db.show_tables()  # Prompts for database name and shows its tables
else:
    print("Failed to connect.")

```

    Connects to MySQL: Checks if the connection is successful.
    Show Tables: If connected, it asks for a database name and lists its tables.
    Error Handling: Displays a message if the connection fails.

# Inserting Data into a Table

You can insert data into a table using built-in Python string methods. Use the insert_data_with_builtins_methods() function to apply string manipulation (e.g., lower(), upper(), strip(), etc.) before inserting data into the database.
If you does not want to insert the values with to str() methods so enter skipall on the place of methods to skipall methods. 
Example: Insert Data with String Methods

## Example table and data

```python

table_name = "employees"
columns = ["name", "address", "monthly_salary", "additional_info_0"]
values = [" sadsej jweina ", "  red house ", 15040.00, "piza seller"]

# Insert data with string methods (e.g., 'lower', 'upper', etc.)
db.insert_data_with_builtins_methods(table_name, columns, values)
```
During execution, you will be prompted to enter string methods (comma-separated) to apply to string values before they are inserted into the database.

## Inserting Data into a Table

This module provides various methods for inserting data into MySQL tables. Below are the examples of how to use them effectively.

# Insert Data Using Built-in Functions

Use the insert_data_only_with_builtins() method to insert data with correctly formatted values into a table.

## Example: Insert data with built-in Python functions

```python

table_name = "employees"
columns = ['name', 'address', 'age', 'monthly_salary', 'additional_info_0']
values = ['jobiden', 'muslime house', 48, 932433.14, 'dissioner']

# Insert the data
db.insert_data_only_with_builtins(table_name, columns, values)

```
This method ensures that all values are of the correct type and inserts them into the specified columns.
# Insert Multiple Rows Without Additional String Methods

Use the insert_mul_val_data_without() method to insert multiple rows into the table without applying additional string manipulations.

## Example: Insert multiple rows without additional methods

```python

table_name = "employees"
columns = ['name', 'address', 'age', 'monthly_salary']
values_list = [
    ('jorgen', 'stright gargen', 29, 424533.24),
    ('alice', 'baker street', 34, 500000.00),
    ('bob', 'main street', 22, 300000.00)
]

# Insert multiple rows
db.insert_mul_val_data_without(table_name, columns, values_list)

```

This method inserts multiple sets of values directly into the database.

# Insert Multiple Rows with String Methods

Use the insert_mul_val_data_with() method to insert multiple rows while applying string methods (like lower(), upper(), etc.).

## Example: Insert multiple rows with string methods

```python

table_name = "employees"
columns = ['name', 'address', 'age', 'monthly_salary', 'additional_info_0']
values_list = [
    ('gorgen', 'strightree jarden', 29, 424533.24, 'tveler'),
    ('ilice', 'baker rtreet', 34, 500000.00, 'vitor'),
    ('job', 'main sreet', 22, 300000.00, 'balor'),
    ('dob', 'main treet', 22, 300000.00, 'bhelor')  # Duplicate entry
]

# Insert data with error handling
try:
    db.insert_mul_val_data_with(table_name, columns, values_list)
except Exception as e:
    print(f"Error occurred while inserting data: {e}")

```

This method also handles errors like duplicate entries and provides feedback if an error occurs during insertion.
# Insert with Set Operations

For more complex data insertions involving set operations, use the insert_mul_val_data_with() method, which handles multiple rows with set operations.

## Example: Insert using set operations

```python

table_name = "employees"
columns = ["name", "address", "age", "monthly_salary", "additional_info_0"]
values_list = [
    ('MR', 'HR', 21, 24, 'PGM'),
    ('ME', 'RH', 34, 12345, 'SETER')
]

# Insert the data with set operations
db.insert_mul_val_data_with(table_name, columns, values_list)

```

This method is useful for inserting multiple rows and managing operations efficiently.

# Selecting and Sorting Data

You can use the select_and_sort_data() function to retrieve and sort data from a table. In this example, the data from the "employees" table is sorted by the 3rd column (age).

## Example: Sorting employees by age
```python

db.select_and_sort_data("employees", 3)

```
# Displaying All Data as a List

The print_data_as_list_only() function retrieves all rows from the "employees" table and displays them as a list.

## Example: Displaying all employees data as a list

```python

db.print_data_as_list_only("employees")

```

## Applying List Methods on Data

To retrieve data from the employees table and apply various list methods, such as append, extend, pop, remove, sort, etc., simply call the print_data_as_list_with_M() method.

## Example table name

```python

table_name = "employees"
# Call the function to apply list methods
print("=== Applying List Methods ===")
db.print_data_as_list_with_M(table_name)

```

This function will prompt you to input the list methods you want to apply, allowing you to manipulate the data in real-time.
Example 2: Aggregate Functions Query

13. To perform aggregate operations like getting the average age of employees grouped by address, use the aggregate_functions() method.

## Query example to get the average age by address

```python

aggregate_query = "SELECT address, AVG(age) FROM employees GROUP BY address"
result = db.aggregate_functions(aggregate_query)
print(result)

```

This query returns the average age of employees grouped by their address.

## MySQL Query Interface

This script provides a simple interface to interact with MySQL, allowing users to execute various query options easily. Below is an overview of the available options and their functionality:
Query Options

```python


while True:
    print("\n--- MySQL Query Options ---")
    print("1. Select with conditions")
    print("2. Select in a range")
    print("3. Select with LIKE")
    print("4. Round column values")
    print("5. Exit")
    choice = input("Choose an option (1-5): ")

    if choice == "1":
        table_name, column, condition, value = db.get_select_conditions_input()
        db.select_with_conditions_with_M(table_name, column, condition, value)

    elif choice == "2":
        table_name, column, start, end = db.get_select_in_range_input()
        db.select_in_range(table_name, column, start, end)

    elif choice == "3":
        table_name, column, pattern = db.get_select_with_like_input()
        db.select_with_like(table_name, column, pattern)

    elif choice == "4":
        table_name, column_name, decimal_places = db.get_round_column_values_input()
        db.round_column_values(table_name, column_name, decimal_places)

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please choose a valid option.")

```


# Option Descriptions

Select with Conditions
Retrieves data based on user-specified conditions (e.g., =, >, !=).

Select in a Range
Returns rows where column values fall between a specified start and end.

Select with LIKE
Searches for patterns within a column using the LIKE keyword (e.g., %pattern%).

Round Column Values
Rounds numeric values in a specified column to a given number of decimal places.

Exit
Ends the program.

Error Handling

If the user inputs an invalid option, an error message prompts them to try again.
Benefits of This Structure

Clarity: Each option is clearly defined, making it easy for users to understand what they can do.
Conciseness: The text is streamlined, avoiding unnecessary repetition while still providing essential information.
Readability: The use of headings and bullet points enhances readability, making it easier for users to navigate through the content.
 
## 15. Join Operations

This module provides functionality to perform various SQL join operations between two tables. Below is an example of how to use an INNER JOIN, along with brief explanations of LEFT JOIN and RIGHT JOIN.

# INNER JOIN

The inner_join_tables() function performs an INNER JOIN operation between two tables, retrieving rows that have matching values in both tables based on a specified condition.

Example:

```python

table1 = 'employees'
table2 = 'owner'
join_condition = 'employees.e_id = owner.o_id'
columns1 = ['name', 'monthly_salary']  # From employees table
columns2 = ['o_f_name']  # From owner table

# Perform INNER JOIN
db.inner_join_tables(table1, table2, join_condition, columns1, columns2)

```

    Purpose: Retrieves rows where there is a match in both employees and owner tables based on e_id = o_id.
    Parameters:
        table1: The first table (e.g., employees).
        table2: The second table (e.g., owner).
        join_condition: The condition to join the tables (e.g., employees.e_id = owner.o_id).
        columns1: List of columns to retrieve from the first table.
        columns2: List of columns to retrieve from the second table.

# LEFT JOIN

The left_join_tables() function performs a LEFT JOIN, which returns all rows from the left table (employees), and the matched rows from the right table (owner). If there is no match, NULL values are returned from the right table.

    Purpose: Retrieves all rows from the employees table, and matching rows from the owner table. Non-matching rows will have NULL values from the owner table.

# RIGHT JOIN

The right_join_tables() function performs a RIGHT JOIN, returning all rows from the right table (owner), and the matched rows from the left table (employees). If there is no match, NULL values are returned from the left table.

    Purpose: Retrieves all rows from the owner table, and matching rows from the employees table. Non-matching rows will have NULL values from the employees table.

## Data Modification and Query Operations

This module allows performing various operations such as deleting rows, dropping tables, and executing user-defined queries. Below are examples and brief explanations for each function.

# DELETE Operation

The delete_record() function deletes rows from a specified table based on a condition (e.g., e_id > 20).

Example:

```python

table_name_for_delete = 'employees'
column_for_delete = 'e_id'
operator_for_delete = '>'  
value_for_delete = 20 

# Perform DELETE operation
db.delete_record(table_name_for_delete, column_for_delete, operator_for_delete, value_for_delete)

```

    Purpose: Deletes rows where the condition (e.g., e_id > 20) is met.
    Parameters:
        table_name_for_delete: The table to delete from.
        column_for_delete: The column to base the condition on.
        operator_for_delete: The operator (e.g., >, <, =).
        value_for_delete: The value for comparison.

# DROP Table

The drop_table() function permanently deletes a table from the database.

Example:

```python

table_name_for_drop = 'fuhj'

# Perform DROP operation
db.drop_table(table_name_for_drop)

```


    Purpose: Drops a specified table from the database.
    Parameters:
        table_name_for_drop: The name of the table to drop.

# Execute User-Defined Query

The execute_query() function allows the execution of any custom SQL query provided by the user.

Example:

```python

table_name = "owner"  # Specify table name
query = f"SELECT o_id, o_f_name, o_l_name, price FROM {table_name}"

# Execute the custom query
db.execute_query(query)

```

    Purpose: Executes any valid SQL query and displays the result.
    Parameters:
        query: The SQL query string to execute.

## Additional Query and Data Modification Operations

This module supports various advanced SQL operations, including handling NULL values, eliminating duplicates, and updating data.
# Complex Operation (with Enumerate and Type)

The complex_operation() function performs a detailed operation that showcases the use of Python's enumerate and type.

Example:

```python

db.complex_operation(table_name)

```

    Purpose: Demonstrates a complex operation using Python's enumerate and type features.
    Parameters:
        table_namez: The table involved in the operation.

# Handling NULL Values with COALESCE

The select_with_coalesce() function fetches data from a specified column and replaces NULL values with a default value using SQL's COALESCE.

Example:

```python

table_name = "employees"
column_name = "additional_info_0"
default_value = "No email available"
db.select_with_coalesce(table_name, column_name, default_value)

```

    Purpose: Handles NULL values by returning a default value if a NULL is encountered.
    Parameters:
        table_name: The name of the table.
        column_name: The column to check for NULL values.
        default_value: The value to use when NULL is found.

# Eliminate Duplicates with DISTINCT

The select_with_distinct() function retrieves unique values from a specified column by using the DISTINCT SQL clause.

Example:

```python

table_name = "employees"
column_name_for_distinct = "address"
db.select_with_distinct(table_name, column_name_for_distinct)

```

    Purpose: Removes duplicate values from the selected column.
    Parameters:
        table_name: The table from which data is fetched.
        column_name_for_distinct: The column to retrieve distinct values from.

# Bulk Data Update

The update_data() function allows for updating multiple rows in bulk based on a list of values.

Example:

```python

update_query = "UPDATE owner SET o_f_name = %s WHERE o_id = %s"
values_list = [
    ("jan khan", 3),  
    ("salaan sal", 7), 
    ("sala nor", 2),  
    ("uawal nor", 5), 
]
db.update_data(update_query, values_list)

```

    Purpose: Updates multiple records in the database using a list of values.
    Parameters:
        update_query: The SQL query for updating data.
        values_list: A list of tuples containing new values and corresponding conditions for the update.


## Data Selection Operations using select_data()

The select_data() function is used to execute SQL SELECT queries and retrieve data from the database. This method can handle various types of SQL queries, allowing users to filter, concatenate, and perform conditions on data.

# Retrieve All Records from a Table

The select_data() function can be used to fetch all records from a table.

```python

select_query = "SELECT * FROM owner"
results = db.select_data(select_query)
for row in results:
    print(row)

```

    Purpose: Retrieves all rows from the owner table.

# Concatenate Columns

You can use the CONCAT SQL function within the select_data() method to combine multiple columns into a single result.

Example:

```python

concat_query = "SELECT CONCAT('Owner: ', o_f_name, ' ', o_l_name) AS full_Name FROM owner"
results = db.select_data(concat_query)
for row in results:
    print(row[0])

```

    Purpose: Combines first and last names of owners into a full name and retrieves it.

# Filter Data with Conditions

The select_data() function allows for filtering records based on conditions, such as comparing values or filtering based on a pattern.

    Filter by Salary and Age:

```python

select_query = "SELECT * FROM employees WHERE monthly_salary > 70000 OR age < 29 OR e_id = 3"
results = db.select_data(select_query)
for row in results:
    print(row)

```

    Filter by Name Starting with 'B':

```python

select_query = "SELECT * FROM employees WHERE name LIKE 'B%'"
results = db.select_data(select_query)
for row in results:
    print(row)

```

# Filter by Age Range (BETWEEN):

```python

select_query = "SELECT * FROM employees WHERE age BETWEEN 25 AND 35"
results = db.select_data(select_query)
for row in results:
    print(row)

```

# Filter by Specific Names (IN clause):

```python

select_query = "SELECT * FROM employees WHERE name IN ('Alice', 'Charlie')"
results = db.select_data(select_query)
for row in results:
    print(row)

```

Summary:

The select_data() function in this module provides flexibility in data retrieval by allowing users to:

    Select all data from a table.
    Concatenate multiple columns.
    Filter records based on various conditions (e.g., comparison operators, pattern matching, range filtering).

These examples demonstrate how users can adapt this function for various query needs.






## Using UNION and UNION ALL Queries with select_data()

The select_data() function can be used to execute UNION and UNION ALL SQL queries, which allow combining results from multiple SELECT statements.

    UNION removes duplicate rows from the result.
    UNION ALL includes all rows, even if duplicates exist.

Example: UNION Query

```python

union_query = """
SELECT e_id, name, monthly_salary FROM employees
UNION
SELECT o_id, o_f_name, price FROM owner;
"""
print("Results of UNION query:")
union_results = db.select_data(union_query)
for row in union_results:
    print(row)

```

    Purpose: Combines results from the employees and owner tables, removing duplicates.

How to Use UNION ALL

To include all rows (including duplicates), simply replace the UNION keyword with UNION ALL in the query:

## ALTER TABLE Operations with alter_table()

The alter_table() function allows you to modify the structure of an existing table, such as adding columns, renaming columns, changing data types, or setting default values.
Examples:

# Add a New Column:

```python

add_column_query = "ALTER TABLE employees ADD address VARCHAR(255) AFTER name;"
db.alter_table(add_column_query)

```

    Adds a new address column to the employees table.

# Rename a Column:

```python

rename_column_query = "ALTER TABLE employees CHANGE id e_id INT AUTO_INCREMENT;"
db.alter_table(rename_column_query)

```

    Renames the id column to e_id in the employees table.

 3. Set a Default Value:

```python

default_value_query = "ALTER TABLE employees MODIFY age INT DEFAULT 0;"
db.alter_table(default_value_query)

```

    Sets a default value of 0 for the age column.

# Change Column Data Type:

```python

change_data_type_query = "ALTER TABLE employees MODIFY age SMALLINT;"
db.alter_table(change_data_type_query)

```

    Changes the data type of the age column to SMALLINT.

## UPDATE Operations with update_data()

The update_data() function allows you to update existing records in a table, whether you're modifying a single row, multiple rows, or even altering table structure.
Examples:

# Update a Single Row:

```python

update_query = "UPDATE employees SET address = %s WHERE id = %s"
updated_values = ("Green house 60", "1")
db.update_data(update_query, updated_values)

```

    Updates the address field for the employee with id 1.

# Update Multiple Rows:

```python

update_query = "UPDATE employees SET address = %s WHERE e_id = %s"
updated_values = [
    ("Jangle Street", "3"),
    ("School Street", "4")
]
db.update_data(update_query, updated_values)

```

    Updates the address field for multiple employees (with e_id 3 and 4).

# Alter Table Structure:

```python

alter_query = "ALTER TABLE employees ALTER COLUMN id DROP DEFAULT"
db.update_data(alter_query)

```

    Alters the employees table to drop the default value for the id column.


## Database Operations

 # Create a View:

```python

create_view_query = """
CREATE VIEW EM_High_Salary AS
SELECT e_id, name, monthly_salary FROM employees
WHERE monthly_salary < 600;
"""
db.update_data_view(create_view_query)

```

    This query creates a view named EM_High_Salary based on the employees table.
    A view is like a virtual table that displays specific columns and rows based on a query. Here, it selects employee IDs, names, and salaries where the monthly_salary is less than 600.
    Once created, you can query this view as if it were a table.

# Describe Table Structure:

```python

table_name = "fuhj"
table_structure = db.describe_table(table_name)

print(table_structure)

```

    This function retrieves and displays the structure of the table named fuhj.
    It returns details about each column in the table, such as column names, data types, and constraints.
    This helps users understand how the data is stored in the table.

# Drop a View:

```python

view_name = "E_High_Salary"
db.drop_view(view_name)

```

    This command deletes (drops) an existing view named E_High_Salary.
    Dropping a view will remove the virtual table from the database, but it won't affect the underlying data in the employees table.

# Delete Data:

```python

delete_query = "DELETE FROM employees WHERE name = %s"
delete_values = ("Bob",)
db.delete_data(delete_query, delete_values)

```

    This function deletes a specific record from the employees table where the name is "Bob."
    The DELETE operation permanently removes rows from the table that meet the condition specified in the WHERE clause.

# Select Data with Conditions (WHERE, LIKE, BETWEEN):

```python

select_query = "SELECT * FROM employees WHERE age BETWEEN %s AND %s AND name LIKE %s"
result = db.select_with_conditions_with_out(select_query, (25, 35, 'A%'))

```

    This query retrieves data from the employees table with multiple conditions.
    It selects employees whose age is between 25 and 35 and whose name starts with the letter 'A' (using the LIKE condition).
    This function is useful when you need to filter and retrieve specific data from the database.

# Close the Database Connection:

```python

db.close_connection()

```

    This function safely closes the connection to the database once all operations are complete.
    Closing the connection ensures that any resources associated with the database connection are released.