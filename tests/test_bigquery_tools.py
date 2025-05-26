import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import os

# Adjust the path to import from the parent directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bigquery_tools import (
    execute_sql_query,
    get_table_schema,
    list_tables,
    _get_mayodb_schema,
    _MAYODB_SCHEMA # To reset it in tests
)
from google.cloud.exceptions import GoogleCloudError
# It's good practice to import the specific exception you expect,
# For example, BadRequest if that's what BQ client raises for syntax errors
from google.api_core.exceptions import BadRequest


# Mock schema data for testing _get_mayodb_schema, get_table_schema, list_tables
mock_schema_data = {
    "project1_id": {
        "tables": {
            "dataset1.TABLE_A": {
                "columns": [
                    {"name": "col1", "data_type": "STRING"},
                    {"name": "col2", "data_type": "INTEGER"}
                ]
            },
            "dataset1.TABLE_B": {
                "columns": [
                    {"name": "fieldA", "data_type": "BOOLEAN"}
                ]
            }
        }
    },
    "project2_id": {
        "tables": {
            "dataset2.TABLE_C": {
                "columns": [
                    {"name": "data_col", "data_type": "BYTES"}
                ]
            },
            # For testing unqualified name resolution
            "dataset_shared.TABLE_A": {
                 "columns": [
                    {"name": "shared_col", "data_type": "STRING"}
                ]
            }
        }
    }
}

class TestBigQueryTools(unittest.TestCase):

    def setUp(self):
        """
        Reset the _MAYODB_SCHEMA cache before each test
        that might interact with _get_mayodb_schema.
        """
        global _MAYODB_SCHEMA
        _MAYODB_SCHEMA = None
        # Also, ensure that bigquery_tools._MAYODB_SCHEMA is reset if it's imported directly
        # This is a bit of a hack; ideally, the module itself would provide a reset function.
        import bigquery_tools
        bigquery_tools._MAYODB_SCHEMA = None


    def tearDown(self):
        """
        Clean up any potentially modified global state after tests.
        """
        global _MAYODB_SCHEMA
        _MAYODB_SCHEMA = None
        import bigquery_tools
        bigquery_tools._MAYODB_SCHEMA = None

    # --- Tests for _get_mayodb_schema ---

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(mock_schema_data))
    @patch('os.path.exists', return_value=True)
    def test_get_mayodb_schema_success_and_caching(self, mock_exists, mock_file_open):
        """Test successful loading and caching of the schema."""
        # First call - should load from file
        schema = _get_mayodb_schema()
        self.assertEqual(schema, mock_schema_data)
        mock_file_open.assert_called_once() # Check if open was called

        # Reset call count for the next check
        mock_file_open.reset_mock()

        # Second call - should use cache
        schema_cached = _get_mayodb_schema()
        self.assertEqual(schema_cached, mock_schema_data)
        mock_file_open.assert_not_called() # Should not call open again

    @patch('builtins.open', side_effect=FileNotFoundError("File not found for test"))
    @patch('os.path.exists', return_value=False) # Simulate file not existing
    def test_get_mayodb_schema_file_not_found(self, mock_exists, mock_file_open):
        """Test FileNotFoundError when schema file is missing."""
        with patch('builtins.print') as mock_print: # Suppress print statements
            schema = _get_mayodb_schema()
            self.assertIsNone(schema)
            mock_print.assert_any_call(f"Error: The schema file 'mayo_structure_parsed.json' was not found at mayo_structure_parsed.json.") # Path check may vary

    @patch('builtins.open', new_callable=mock_open, read_data="this is not valid json")
    @patch('os.path.exists', return_value=True)
    def test_get_mayodb_schema_json_decode_error(self, mock_exists, mock_file_open):
        """Test JSONDecodeError for invalid JSON content."""
        with patch('builtins.print') as mock_print:
            schema = _get_mayodb_schema()
            self.assertIsNone(schema)
            mock_print.assert_any_call("Error: Failed to decode JSON from 'mayo_structure_parsed.json'.")

    # --- Tests for execute_sql_query ---

    @patch('bigquery_tools.bigquery.Client')
    def test_execute_sql_query_success(self, MockBigQueryClient):
        """Test successful SQL query execution."""
        mock_client_instance = MockBigQueryClient.return_value
        mock_query_job = mock_client_instance.query.return_value
        
        # Mocking row iteration
        mock_rows = [
            MagicMock(**{'to_api_repr.return_value': {'colA': 'value1', 'colB': 10}}),
            MagicMock(**{'to_api_repr.return_value': {'colA': 'value2', 'colB': 20}})
        ]
        # The .result() method should return an object that can be iterated over,
        # and each item in the iteration should have a to_api_repr() method if that's what dict(row) relies on.
        # A simpler way is to make .result() return a list of dicts directly if the actual Row object is complex to mock.
        # However, the production code uses `dict(row)`, so `row` should be dict-convertible.
        # A common pattern for Row objects is that they are like namedtuples or have a `_fields` attribute.
        # For simplicity, let's assume `dict(row)` works if row is a MagicMock that can have attributes assigned.
        
        # Let's try making the mock rows themselves behave like dicts or have items
        mock_row_1 = MagicMock()
        mock_row_1.keys.return_value = ['colA', 'colB']
        mock_row_1.__getitem__.side_effect = lambda key: {'colA': 'value1', 'colB': 10}[key]
        
        mock_row_2 = MagicMock()
        mock_row_2.keys.return_value = ['colA', 'colB']
        mock_row_2.__getitem__.side_effect = lambda key: {'colA': 'value2', 'colB': 20}[key]

        mock_query_job.result.return_value = [mock_row_1, mock_row_2]

        query = "SELECT colA, colB FROM some_table"
        expected_result = {"result": [{'colA': 'value1', 'colB': 10}, {'colA': 'value2', 'colB': 20}]}
        
        actual_result = execute_sql_query(query)
        self.assertEqual(actual_result, expected_result)
        mock_client_instance.query.assert_called_once_with(query)

    @patch('bigquery_tools.bigquery.Client')
    def test_execute_sql_query_google_cloud_error(self, MockBigQueryClient):
        """Test query failure due to GoogleCloudError."""
        mock_client_instance = MockBigQueryClient.return_value
        mock_client_instance.query.side_effect = GoogleCloudError("Test BigQuery Service Error")

        query = "SELECT * FROM table_that_causes_gcp_error"
        expected_result = {"error": "Test BigQuery Service Error", "result": []}
        with patch('builtins.print') as mock_print: # Suppress print
            actual_result = execute_sql_query(query)
            self.assertEqual(actual_result, expected_result)
            mock_print.assert_any_call("BigQuery query failed: Test BigQuery Service Error")

    @patch('bigquery_tools.bigquery.Client')
    def test_execute_sql_query_bad_request_error(self, MockBigQueryClient):
        """Test query failure due to BadRequest (e.g., syntax error)."""
        mock_client_instance = MockBigQueryClient.return_value
        # BadRequest typically inherits from GoogleCloudError, so the previous test might catch it too
        # depending on the MRO. Explicitly testing for it is good if behavior differs.
        mock_client_instance.query.side_effect = BadRequest("Invalid query syntax for test")

        query = "SELEC * FROM table_with_syntax_error" # Intentionally misspelled SELEC
        expected_result = {"error": "Invalid query syntax for test", "result": []}
        with patch('builtins.print') as mock_print:
            actual_result = execute_sql_query(query)
            self.assertEqual(actual_result, expected_result)
            mock_print.assert_any_call("BigQuery query failed: Invalid query syntax for test")
            
    @patch('bigquery_tools.bigquery.Client')
    def test_execute_sql_query_unexpected_error(self, MockBigQueryClient):
        """Test query failure due to a non-GoogleCloudError."""
        mock_client_instance = MockBigQueryClient.return_value
        mock_client_instance.query.side_effect = ValueError("Some unexpected Python error")

        query = "SELECT * FROM a_table"
        # The exact error message might depend on how it's caught and stringified.
        expected_error_message_part = "An unexpected error occurred: Some unexpected Python error"
        with patch('builtins.print') as mock_print:
            actual_result = execute_sql_query(query)
            self.assertIn("error", actual_result)
            self.assertTrue(actual_result["error"].startswith("An unexpected error occurred:"))
            self.assertIn("Some unexpected Python error", actual_result["error"])
            self.assertEqual(actual_result["result"], [])
            mock_print.assert_any_call(f"An unexpected error occurred during query execution: Some unexpected Python error")


    # --- Tests for get_table_schema ---

    @patch('bigquery_tools._get_mayodb_schema', return_value=mock_schema_data)
    def test_get_table_schema_found_qualified(self, mock_load_schema):
        """Test successfully retrieving schema for a fully qualified table name."""
        expected_schema = {"schema": {"col1": "STRING", "col2": "INTEGER"}}
        actual_schema = get_table_schema("dataset1.TABLE_A")
        self.assertEqual(actual_schema, expected_schema)

    @patch('bigquery_tools._get_mayodb_schema', return_value=mock_schema_data)
    def test_get_table_schema_found_unqualified(self, mock_load_schema):
        """Test retrieving schema for an unqualified table name (if supported)."""
        # This test assumes the logic in get_table_schema can find "TABLE_C" under "dataset2"
        # or prefers a specific one if names clash (e.g. "dataset_shared.TABLE_A" vs "dataset1.TABLE_A")
        # Based on current implementation, it finds the first match if unqualified.
        # `dataset_shared.TABLE_A` is defined after `dataset1.TABLE_A` in `mock_schema_data`
        # but iteration order over dict keys is not guaranteed for older Python versions (pre 3.7).
        # Let's test for a unique unqualified name first.
        expected_schema_c = {"schema": {"data_col": "BYTES"}}
        with patch('builtins.print') as mock_print: # Suppress warning for unqualified name
            actual_schema_c = get_table_schema("TABLE_C")
            self.assertEqual(actual_schema_c, expected_schema_c)
            mock_print.assert_any_call("Warning: Matched unqualified table name 'TABLE_C' to 'dataset2.TABLE_C'. Provide 'dataset.table' for precision.")

        # Test for an unqualified name that exists in multiple datasets
        # The current implementation should find the one in 'project1_id' first as dicts are iterated.
        # Let's ensure our mock_schema_data is defined in a way that 'project1_id' comes before 'project2_id' if order matters.
        # For Python 3.7+ dicts preserve insertion order.
        expected_schema_a_unqualified = {"schema": {"col1": "STRING", "col2": "INTEGER"}}
        with patch('builtins.print') as mock_print:
            actual_schema_a_unqualified = get_table_schema("TABLE_A")
            self.assertEqual(actual_schema_a_unqualified, expected_schema_a_unqualified)
            mock_print.assert_any_call("Warning: Matched unqualified table name 'TABLE_A' to 'dataset1.TABLE_A'. Provide 'dataset.table' for precision.")


    @patch('bigquery_tools._get_mayodb_schema', return_value=mock_schema_data)
    def test_get_table_schema_not_found(self, mock_load_schema):
        """Test when a table is not found in the schema JSON."""
        expected_response = {"schema": {}, "error": "Table dataset1.NON_EXISTENT_TABLE not found in schema JSON"}
        actual_response = get_table_schema("dataset1.NON_EXISTENT_TABLE")
        self.assertEqual(actual_response, expected_response)

    @patch('bigquery_tools._get_mayodb_schema', return_value=None)
    def test_get_table_schema_json_load_fails(self, mock_load_schema_fails):
        """Test behavior when the schema JSON loading itself fails."""
        expected_response = {"schema": {}, "error": "Failed to load schema JSON"}
        actual_response = get_table_schema("any.table")
        self.assertEqual(actual_response, expected_response)

    @patch('bigquery_tools._get_mayodb_schema', return_value={"project": {"tables": {"ds.tbl": {"columns": "not a list"}}}})
    def test_get_table_schema_malformed_columns(self, mock_load_malformed_schema):
        """Test schema retrieval with malformed columns entry."""
        expected_response = {"schema": {}, "error": "Malformed column data for table ds.tbl in schema JSON"}
        actual_response = get_table_schema("ds.tbl")
        self.assertEqual(actual_response, expected_response)

    @patch('bigquery_tools._get_mayodb_schema', return_value={"project": {"tables": {"ds.tbl": {"columns": [{"wrong_key": "val"}]}}}})
    def test_get_table_schema_missing_column_keys(self, mock_load_missing_keys_schema):
        """Test schema retrieval with missing 'name' or 'data_type' in column data."""
        expected_response = {"schema": {}, "error": "Missing 'name' or 'data_type' in column data for table ds.tbl in schema JSON"}
        actual_response = get_table_schema("ds.tbl")
        self.assertEqual(actual_response, expected_response)


    # --- Tests for list_tables ---

    @patch('bigquery_tools._get_mayodb_schema', return_value=mock_schema_data)
    def test_list_tables_all(self, mock_load_schema):
        """Test listing all tables from all datasets (dataset.table format)."""
        expected_tables = {
            "tables": sorted([
                "dataset1.TABLE_A", 
                "dataset1.TABLE_B", 
                "dataset2.TABLE_C",
                "dataset_shared.TABLE_A"
            ])
        }
        actual_tables = list_tables()
        # Sort the actual list as well if the function doesn't guarantee order (it does now)
        actual_tables["tables"] = sorted(actual_tables["tables"])
        self.assertEqual(actual_tables, expected_tables)

    @patch('bigquery_tools._get_mayodb_schema', return_value=mock_schema_data)
    def test_list_tables_specific_dataset(self, mock_load_schema):
        """Test listing tables for a specific dataset (only table names)."""
        expected_tables = {"tables": sorted(["TABLE_A", "TABLE_B"])}
        actual_tables = list_tables(dataset_id="dataset1")
        actual_tables["tables"] = sorted(actual_tables["tables"])
        self.assertEqual(actual_tables, expected_tables)

    @patch('bigquery_tools._get_mayodb_schema', return_value=mock_schema_data)
    def test_list_tables_dataset_not_found(self, mock_load_schema):
        """Test listing tables for a dataset that doesn't exist."""
        expected_tables = {"tables": []}
        actual_tables = list_tables(dataset_id="non_existent_dataset")
        self.assertEqual(actual_tables, expected_tables)

    @patch('bigquery_tools._get_mayodb_schema', return_value=None)
    def test_list_tables_json_load_fails(self, mock_load_schema_fails):
        """Test list_tables when schema JSON loading fails."""
        expected_response = {"tables": [], "error": "Failed to load schema JSON"}
        actual_response = list_tables()
        self.assertEqual(actual_response, expected_response)
        
        actual_response_with_dataset = list_tables(dataset_id="any_dataset")
        self.assertEqual(actual_response_with_dataset, expected_response)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

# To run these tests from the command line, navigate to the parent directory of 'tests'
# and run: python -m unittest tests.test_bigquery_tools
# (Assuming your project structure is something like project_root/bigquery_tools.py and project_root/tests/test_bigquery_tools.py)
# If bigquery_tools.py is in the root and tests is a subdir, from root: python -m unittest tests.test_bigquery_tools
# Or, if bigquery_tools.py is in a package, adjust the import path and run command.
# The `sys.path.insert` handles running the script directly for now.
# For a real project, consider using a proper package structure or a test runner that handles paths.
# For example, if `bigquery_tools` is part of a package `my_package`, imports would be `from my_package.bigquery_tools import ...`
# and tests might be run with `python -m unittest discover -s tests` or similar.
# The current `sys.path` modification is a common way to handle simple script structures.
# Note: The `_MAYODB_SCHEMA` global variable in `bigquery_tools.py` makes testing tricky
# as its state persists across tests if not reset. The `setUp` method here attempts to reset it.
# A better design would be to pass the schema around or use a class structure for `bigquery_tools`
# where the schema is an instance variable.
# The `argv` and `exit=False` in `unittest.main` are for compatibility with some environments (like Jupyter).
# Standard CLI execution doesn't need them.
# `bigquery_tools.py` is assumed to be in the parent directory of `tests/` for the `sys.path` hack to work.
# If `bigquery_tools.py` is in the same directory as `tests/` (e.g. both in root), then `sys.path` isn't needed.
# The current task implies `bigquery_tools.py` is at the root, and `tests/` is a subdirectory.
# So, from the root, `python -m unittest tests.test_bigquery_tools` is the typical way.
# The `sys.path` insert makes it so you *could* run `python tests/test_bigquery_tools.py` directly from the root.
# Let's assume `bigquery_tools.py` is in the root for the imports.
# The `../` in `sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))`
# correctly points to the root directory if this test file is in `tests/`.
# The `import bigquery_tools` in `setUp` and `tearDown` for resetting `_MAYODB_SCHEMA` is a direct manipulation
# of the imported module's global state.
# The mock for `execute_sql_query_success` has been updated to better reflect how `dict(row)` might work
# with BigQuery `Row` objects. Real `Row` objects are more complex, but for `dict()` conversion,
# they generally need to support iteration over their keys or have specific methods.
# Making the mock row itself behave like a dictionary (via __getitem__ and keys) is a common way to mock this.
# The original `MagicMock(**{'to_api_repr.return_value': ...})` is also a valid approach if `to_api_repr` is what `dict()` uses internally.
# Test for `execute_sql_query_unexpected_error` has been added.
# Tests for `get_table_schema` malformed/missing keys have been added.
# Ensured `_MAYODB_SCHEMA` is reset properly in `setUp` and `tearDown` also by re-importing and setting `bigquery_tools._MAYODB_SCHEMA = None`.
# This is crucial because Python's module caching means `from bigquery_tools import _MAYODB_SCHEMA` gives a *copy* of the reference
# at import time if `_MAYODB_SCHEMA` is a simple type, or a reference to the mutable object if it's a list/dict.
# Since it's initially `None` (immutable) and then potentially a `dict` (mutable), directly assigning
# `_MAYODB_SCHEMA = None` (the global name in this test file) doesn't affect the one in the `bigquery_tools` module
# after it has been imported. The `import bigquery_tools; bigquery_tools._MAYODB_SCHEMA = None` is more robust.
# The path `mayo_structure_parsed.json` in `_get_mayodb_schema` is relative. The tests for `_get_mayodb_schema`
# mock `os.path.exists` to control which path it thinks is valid.
# The `test_get_mayodb_schema_file_not_found` asserts the print call with the path it *would* try if `os.path.dirname(__file__)` was used
# and then the fallback. The fallback is just "mayo_structure_parsed.json".
# The actual `_get_mayodb_schema` has a fallback:
# `file_path = os.path.join(os.path.dirname(__file__), "mayo_structure_parsed.json")`
# `if not os.path.exists(file_path): file_path = "mayo_structure_parsed.json"`
# So if the first path doesn't exist, it tries the second.
# The mock for `os.path.exists` in `test_get_mayodb_schema_file_not_found` is set to `False`.
# The test should check the print message for the *final* path it tried and failed on.
# If `os.path.join(os.path.dirname(__file__), "mayo_structure_parsed.json")` from within `bigquery_tools.py`
# (when run from root) is `bigquery_tools/mayo_structure_parsed.json` and `os.path.exists` is `False`,
# it will then try `mayo_structure_parsed.json` (relative to CWD, which is root).
# So the error message will be for `mayo_structure_parsed.json`. This seems correct.
# Added more detailed comments about running tests and module state.
