from typing import Dict, List, Any

# Consistent list of tables for simulation
SIMULATED_TABLES = ["capitals_data", "schema_info", "order_summary", "customer_details"]

def execute_sql_query(query: str) -> Dict[str, Any]:
    """
    Simulates executing a SQL query against BigQuery.
    Returns different canned results based on keywords in the query.
    """
    print(f"Simulating SQL query execution: {query}")
    query_lower = query.lower()

    if "capitals_data" in query_lower or "capital" in query_lower or "france" in query_lower:
        if "france" in query_lower:
            return {"result": [{"country": "France", "capital": "Paris"}]}
        return {"result": [{"country": "France", "capital": "Paris"}, {"country": "Germany", "capital": "Berlin"}]}
    elif "schema_info" in query_lower or "schema" in query_lower:
        if "customer_details" in query_lower:
             return {"result": [{"table_name": "customer_details", "columns": ["id", "name", "email", "signup_date"]}]}
        return {"result": [{"table_name": "customer_details", "columns": ["id", "name", "email", "signup_date"]}, {"table_name": "order_summary", "columns": ["order_id", "customer_id", "order_date", "total_amount"]}]}
    elif "order_summary" in query_lower or "orders" in query_lower:
        return {"result": [{"order_id": "123", "customer_id": "cust_A", "order_date": "2023-01-15", "total_amount": 100.50}, {"order_id": "124", "customer_id": "cust_B", "order_date": "2023-01-16", "total_amount": 75.20}]}
    elif "customer_details" in query_lower or "customers" in query_lower:
         return {"result": [{"id": "cust_A", "name": "John Doe", "email": "john@example.com"}, {"id": "cust_B", "name": "Jane Smith", "email": "jane@example.com"}]}
    # Default if no specific keywords match, but a table is mentioned
    elif any(table_name in query_lower for table_name in SIMULATED_TABLES):
        return {"result": [{"info": "Generic data from specified table."}]}
    
    return {"result": []} # Empty result if no relevant keywords or tables found

def get_table_schema(table_name: str) -> Dict[str, Any]:
    """
    Simulates retrieving the schema for a BigQuery table.
    Returns different canned schemas based on the table name.
    """
    print(f"Simulating schema retrieval for table: {table_name}")
    if table_name == "capitals_data":
        return {"schema": {"country": "STRING", "capital": "STRING"}}
    elif table_name == "schema_info": # A meta-table for describing other schemas
        return {"schema": {"table_name": "STRING", "columns": "ARRAY<STRING>"}}
    elif table_name == "order_summary":
        return {"schema": {"order_id": "STRING", "customer_id": "STRING", "order_date": "DATE", "total_amount": "FLOAT"}}
    elif table_name == "customer_details":
        return {"schema": {"id": "STRING", "name": "STRING", "email": "STRING", "signup_date": "DATE"}}
    return {"schema": {}} # Empty schema if table not recognized

def list_tables(dataset_name: str = "default_dataset") -> Dict[str, List[str]]:
    """
    Simulates listing tables in a BigQuery dataset.
    Returns a consistent list of simulated tables.
    """
    print(f"Simulating listing tables for dataset: {dataset_name}")
    return {"tables": SIMULATED_TABLES}

if __name__ == '__main__':
    print("\n--- Testing execute_sql_query ---")
    print(f"Query for 'capital of France': {execute_sql_query('SELECT capital FROM capitals_data WHERE country = \'France\';')}")
    print(f"Query for 'customer schema': {execute_sql_query('SELECT columns FROM schema_info WHERE table_name = \'customer_details\';')}")
    print(f"Query for 'orders': {execute_sql_query('SELECT * FROM order_summary LIMIT 2;')}")
    print(f"Query for 'unknown table': {execute_sql_query('SELECT * FROM unknown_table;')}")

    print("\n--- Testing get_table_schema ---")
    print(f"Schema for 'customer_details': {get_table_schema('customer_details')}")
    print(f"Schema for 'unknown_table': {get_table_schema('unknown_table')}")

    print("\n--- Testing list_tables ---")
    print(f"Tables in default_dataset: {list_tables()}")
    print(f"Tables in sales_data: {list_tables('sales_data')}")
