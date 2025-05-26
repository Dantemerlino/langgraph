from typing import Dict, List, Any
import json
import os
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError

# Global variable to cache the parsed JSON schema
_MAYODB_SCHEMA = None

def _get_mayodb_schema() -> Dict[str, Any]:
    """
    Loads the MayoDB schema from mayo_structure_parsed.json.
    Caches the schema in _MAYODB_SCHEMA after the first load.
    Includes error handling for file operations and JSON parsing.
    """
    global _MAYODB_SCHEMA
    if _MAYODB_SCHEMA is not None:
        return _MAYODB_SCHEMA

    try:
        # Assuming mayo_structure_parsed.json is in the same directory as this script
        # Or provide an absolute path if it's located elsewhere.
        file_path = os.path.join(os.path.dirname(__file__), "mayo_structure_parsed.json")
        if not os.path.exists(file_path):
             # Fallback for environments where __file__ might not be defined or points elsewhere
            file_path = "mayo_structure_parsed.json"

        with open(file_path, 'r') as f:
            _MAYODB_SCHEMA = json.load(f)
        return _MAYODB_SCHEMA
    except FileNotFoundError:
        print(f"Error: The schema file 'mayo_structure_parsed.json' was not found at {file_path}.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from 'mayo_structure_parsed.json'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the schema: {e}")
        return None


# Consistent list of tables for simulation - This will be replaced by actual BQ calls or JSON parsing
SIMULATED_TABLES = ["capitals_data", "schema_info", "order_summary", "customer_details"] # Keep for now, may be removed later

def execute_sql_query(query: str) -> Dict[str, Any]:
    """
    Executes a SQL query against BigQuery.
    """
    client = bigquery.Client()
    try:
        query_job = client.query(query)
        results = query_job.result()  # Waits for the job to complete
        formatted_results = [dict(row) for row in results]
        return {"result": formatted_results}
    except GoogleCloudError as e:
        print(f"BigQuery query failed: {e}")
        return {"error": str(e), "result": []}
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred during query execution: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}", "result": []}

def get_table_schema(table_name: str) -> Dict[str, Any]:
    """
    Retrieves the schema for a table from the loaded mayo_structure_parsed.json.
    """
    parsed_json = _get_mayodb_schema()
    if parsed_json is None:
        return {"schema": {}, "error": "Failed to load schema JSON"}

    # table_name might be dataset.table or just table.
    # The JSON structure is project -> tables -> dataset.table.
    # We need to find the table across all projects if no project is specified.
    
    found_table_data = None
    for project_id, project_data in parsed_json.items():
        if "tables" in project_data:
            # Scenario 1: table_name is fully qualified like "dataset_id.table_id"
            if '.' in table_name and table_name in project_data["tables"]:
                found_table_data = project_data["tables"][table_name]
                break
            # Scenario 2: table_name is just "table_id", try to find it in any dataset
            # This is less precise and might lead to ambiguity if multiple tables have the same name in different datasets.
            # For this implementation, we'll prioritize fully qualified names.
            # If you need to support unqualified table names, you might need to iterate
            # and if multiple are found, decide on a strategy (e.g., return first, or error).
            elif '.' not in table_name:
                for fq_table_name, table_data in project_data["tables"].items():
                    if fq_table_name.endswith('.' + table_name):
                        found_table_data = table_data
                        # To avoid ambiguity, let's print a warning if we find an unqualified name.
                        # A more robust solution might involve knowing the current dataset context.
                        print(f"Warning: Matched unqualified table name '{table_name}' to '{fq_table_name}'. Provide 'dataset.table' for precision.")
                        break # Found a match
                if found_table_data:
                    break # Exit project loop as well

    if found_table_data and "columns" in found_table_data:
        try:
            db_schema = {col['name']: col['data_type'] for col in found_table_data['columns']}
            return {"schema": db_schema}
        except TypeError: # If col is not a dict or 'name'/'data_type' are missing
            return {"schema": {}, "error": f"Malformed column data for table {table_name} in schema JSON"}
        except KeyError: # If 'name' or 'data_type' key is missing in a column entry
             return {"schema": {}, "error": f"Missing 'name' or 'data_type' in column data for table {table_name} in schema JSON"}

    return {"schema": {}, "error": f"Table {table_name} not found in schema JSON"}


def list_tables(dataset_id: str = None) -> Dict[str, List[str]]:
    """
    Lists tables from the mayo_structure_parsed.json.
    If dataset_id is provided, filters tables by that dataset (returning only table names).
    Otherwise, lists all tables from all datasets (returning 'dataset.table' identifiers).
    """
    parsed_json = _get_mayodb_schema()
    if parsed_json is None:
        return {"tables": [], "error": "Failed to load schema JSON"}

    all_tables = []
    for project_data in parsed_json.values(): # Iterate through projects
        if "tables" in project_data:
            for fq_table_name in project_data["tables"].keys(): # fq_table_name is "dataset.table"
                current_dataset_id, _, current_table_name = fq_table_name.partition('.')
                if dataset_id:
                    if current_dataset_id == dataset_id:
                        all_tables.append(current_table_name) # Add only table name
                else:
                    all_tables.append(fq_table_name) # Add "dataset.table"
    
    return {"tables": sorted(list(set(all_tables)))}

if __name__ == '__main__':
    # Ensure the schema is loaded once at the beginning if tests are run
    print("\n--- IMPORTANT ---")
    print("The following test calls will execute REAL BigQuery queries if this script is run directly.")
    print("Ensure you have:")
    print("1. Authenticated with Google Cloud (e.g., via `gcloud auth application-default login`).")
    print("2. The correct Google Cloud project set in your environment for BigQuery.")
    print("3. Necessary IAM permissions to query the specified tables.")
    print("4. The `mayo_structure_parsed.json` file in the same directory as this script, or adjust path in `_get_mayodb_schema`.")
    print("Query costs may apply.")
    print("-----------------\n")

    # Ensure the schema is loaded once at the beginning if tests are run,
    # as list_tables and get_table_schema depend on it.
    _get_mayodb_schema()

    print("\n--- Testing execute_sql_query ---")
    query1 = "SELECT DATE_DK, DAY_NAME FROM `ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.DIM_DATE` LIMIT 2"
    print(f"Executing query: {query1}")
    print(f"Result: {execute_sql_query(query1)}")

    query2 = "SELECT PATIENT_DK, ENCOUNTER_FPK FROM `ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.FACT_ENCOUNTERS` WHERE SITE_CODE = 'RST' LIMIT 1"
    print(f"\nExecuting query: {query2}")
    print(f"Result: {execute_sql_query(query2)}")

    print("\n--- Testing get_table_schema ---")
    table_name_qualified = "phi_udpwh_etl_us_p.DIM_DATE" 
    # Based on the JSON, the table name is "phi_udpwh_etl_us_p.DIM_DATE" under project "ml-mps-adl-intudp-phi-p-d5cb"
    # The get_table_schema function expects "dataset.table" or "table"
    print(f"Testing schema for qualified table: {table_name_qualified}")
    print(f"Result: {get_table_schema(table_name_qualified)}")

    table_name_unqualified = "DIM_DATE"
    print(f"\nTesting schema for unqualified table: {table_name_unqualified}")
    print(f"Result: {get_table_schema(table_name_unqualified)}")
    
    table_name_project_qualified = "ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.DIM_DATE"
    print(f"\nTesting schema for project.dataset.table: {table_name_project_qualified}")
    print(f"Result: {get_table_schema(table_name_project_qualified)}")


    non_existent_table = "non_existent_dataset.NON_EXISTENT_TABLE"
    print(f"\nTesting schema for non-existent table: {non_existent_table}")
    print(f"Result: {get_table_schema(non_existent_table)}")

    print("\n--- Testing list_tables ---")
    print("Testing list_tables() for all tables (format: dataset.table):")
    print(f"Result: {list_tables()}")

    dataset_to_list = "phi_udpwh_etl_us_p"
    print(f"\nTesting list_tables(dataset_id='{dataset_to_list}') (format: table):")
    print(f"Result: {list_tables(dataset_id=dataset_to_list)}")

    non_existent_dataset = "non_existent_dataset"
    print(f"\nTesting list_tables(dataset_id='{non_existent_dataset}'):")
    print(f"Result: {list_tables(dataset_id=non_existent_dataset)}")
    
    # Keep the notes about interaction requirements
    print("\n--- Important Notes for BigQuery Interaction (repeated for visibility) ---")
    print("1. Google Cloud Authentication: Ensure you have authenticated with Google Cloud.")
    print("   Run `gcloud auth application-default login` in your terminal.")
    print("2. Project Configuration: The BigQuery client library typically infers the project from")
    print("   the environment (e.g., `gcloud config set project YOUR_PROJECT_ID`).")
    print("   Ensure this is set to a project where the queried tables reside or that queries")
    print("   use fully qualified table names like `project_id.dataset_id.table_id`.")
    print("3. Permissions: The authenticated user/service account must have BigQuery Data Viewer")
    print("   and BigQuery Job User roles (or equivalent permissions) for the target project/dataset.")
    print("4. `mayo_structure_parsed.json`: This file must be present in the same directory as")
    print("   `bigquery_tools.py` (or adjust path in `_get_mayodb_schema`) and contain the correct")
    print("   structure for `get_table_schema` and `list_tables` to function as intended.")
