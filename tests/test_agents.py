import pytest
from unittest.mock import patch

# Assuming agents.py and states.py are in the parent directory or PYTHONPATH is set up
# For local testing, if tests/ is a subdir of the project root:
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents import (
    generate_questions_agent,
    retrieve_data_agent,
    generate_answer_agent,
    cannot_answer_agent
)
from states import UserInputState, QuestionState, DataState, AnswerState

# --- Tests for generate_questions_agent ---

def test_generate_questions_capital_france():
    state = UserInputState(user_input="What is the capital of France?")
    result = generate_questions_agent(state)
    assert isinstance(result, QuestionState)
    assert "What is the capital of France?" in result.questions

def test_generate_questions_schema_customers():
    state = UserInputState(user_input="Tell me the schema for customers.")
    result = generate_questions_agent(state)
    assert isinstance(result, QuestionState)
    assert "What is the schema of the customer_details table?" in result.questions

def test_generate_questions_how_does_x_work():
    state = UserInputState(user_input="How does gravity work?")
    result = generate_questions_agent(state)
    assert isinstance(result, QuestionState)
    assert "How does gravity work?" in result.questions
    
def test_generate_questions_orders_and_customers():
    state = UserInputState(user_input="Info on orders and customer details")
    result = generate_questions_agent(state)
    assert isinstance(result, QuestionState)
    # Depending on specific keyword logic, check for relevant questions
    assert any("orders" in q.lower() for q in result.questions)
    assert any("customer" in q.lower() for q in result.questions)

def test_generate_questions_default_no_keywords():
    state = UserInputState(user_input="Some random topic.")
    result = generate_questions_agent(state)
    assert isinstance(result, QuestionState)
    assert "Can you provide general information about: some random topic.?" in result.questions
    assert len(result.questions) == 1


# --- Tests for retrieve_data_agent ---

@pytest.fixture
def sample_question_state():
    return QuestionState(questions=["What is the capital of France?", "Describe customer_details schema."])

@patch('agents.list_tables')
@patch('agents.get_table_schema')
@patch('agents.execute_sql_query')
def test_retrieve_data_can_answer_one_question(mock_execute_sql, mock_get_schema, mock_list_tables, sample_question_state):
    # Mock BQ tool responses
    mock_list_tables.return_value = {"tables": ["capitals_data", "customer_details", "schema_info"]}
    # First question (capital) gets data
    # Second question (schema) also gets data via schema_info
    def side_effect_execute_sql(query):
        if "capitals_data" in query:
            return {"result": [{"country": "France", "capital": "Paris"}]}
        if "schema_info" in query and "customer_details" in query:
             return {"result": [{"table_name": "customer_details", "columns": ["id", "name", "email"]}]}
        return {"result": []}
    mock_execute_sql.side_effect = side_effect_execute_sql
    
    mock_get_schema.return_value = {"schema": {"country": "STRING", "capital": "STRING"}} # Not directly used by `can_answer` logic if execute_sql has results

    result_state = retrieve_data_agent(sample_question_state)
    
    assert isinstance(result_state, DataState)
    assert result_state.can_answer is True
    assert len(result_state.retrieved_data) == 2
    assert result_state.retrieved_data[0]["data"] == [{"country": "France", "capital": "Paris"}]
    assert result_state.retrieved_data[1]["data"] == [{"table_name": "customer_details", "columns": ["id", "name", "email"]}]

@patch('agents.list_tables')
@patch('agents.get_table_schema')
@patch('agents.execute_sql_query')
def test_retrieve_data_cannot_answer_any_question(mock_execute_sql, mock_get_schema, mock_list_tables):
    mock_list_tables.return_value = {"tables": ["generic_table"]}
    mock_execute_sql.return_value = {"result": []} # No data from any query
    mock_get_schema.return_value = {"schema": {"some_col": "STRING"}}

    questions = QuestionState(questions=["An unanswerable query about dogs?", "Another irrelevant topic?"])
    result_state = retrieve_data_agent(questions)

    assert isinstance(result_state, DataState)
    assert result_state.can_answer is False
    assert len(result_state.retrieved_data) == 2
    assert result_state.retrieved_data[0]["data"] == "No specific data found from simulation."
    assert result_state.retrieved_data[1]["data"] == "No specific data found from simulation."

@patch('agents.list_tables')
@patch('agents.get_table_schema')
@patch('agents.execute_sql_query')
def test_retrieve_data_no_tables_found(mock_execute_sql, mock_get_schema, mock_list_tables):
    # This test requires modifying how list_tables is called or its return if it can be empty for the agent
    # The agent currently doesn't explicitly handle an empty list from list_tables() before trying to use tables.
    # For now, assume list_tables always returns something, or the agent would need a guard.
    # Let's test the path where execute_sql_query is the one failing to find data.
    mock_list_tables.return_value = {"tables": ["capitals_data"]} # Has tables
    mock_execute_sql.return_value = {"result": []} # But queries yield no data
    mock_get_schema.return_value = {"schema": {"country": "STRING"}}
    
    questions = QuestionState(questions=["What is Z?"]) # A question that won't match keywords in execute_sql
    result_state = retrieve_data_agent(questions)
    
    assert result_state.can_answer is False
    assert "No specific data found from simulation." in result_state.retrieved_data[0]["data"]


# --- Tests for generate_answer_agent ---

def test_generate_answer_can_answer_with_data():
    retrieved_items = [
        {"question": "Q1", "query_attempted": "...", "data": [{"info": "Paris"}]},
        {"question": "Q2", "query_attempted": "...", "data": "No specific data found from simulation."}
    ]
    state = DataState(retrieved_data=retrieved_items, can_answer=True)
    result = generate_answer_agent(state)
    assert isinstance(result, AnswerState)
    assert "Based on the retrieved data:" in result.answer
    assert "For 'Q1': {'info': 'Paris'}..." in result.answer
    assert "Q2" not in result.answer # Because it had no specific data

def test_generate_answer_can_answer_no_specific_data():
    retrieved_items = [
        {"question": "Q1", "query_attempted": "...", "data": "No specific data found from simulation."},
        {"question": "Q2", "query_attempted": "...", "data": "No specific data found from simulation."}
    ]
    state = DataState(retrieved_data=retrieved_items, can_answer=True) # can_answer might be true if queries ran but found nothing specific
    result = generate_answer_agent(state)
    assert isinstance(result, AnswerState)
    assert "I found some information, but couldn't summarize it clearly." in result.answer

def test_generate_answer_cannot_answer():
    state = DataState(retrieved_data="Some reason for not answering", can_answer=False)
    result = generate_answer_agent(state)
    assert isinstance(result, AnswerState)
    assert "I could not find enough specific information to answer the questions." in result.answer


# --- Tests for cannot_answer_agent ---

def test_cannot_answer_agent_generic():
    state = DataState(retrieved_data="Some data that led to can_answer=False", can_answer=False)
    result = cannot_answer_agent(state)
    assert isinstance(result, AnswerState)
    assert "Sorry, I cannot answer the question with the available data." in result.answer

def test_cannot_answer_agent_with_no_specific_data_reason():
    retrieved_items = [
        {"question": "Q1", "query_attempted": "...", "data": "No specific data found from simulation."},
    ]
    state = DataState(retrieved_data=retrieved_items, can_answer=False)
    result = cannot_answer_agent(state)
    assert isinstance(result, AnswerState)
    assert "simulated environment did not yield specific results" in result.answer
