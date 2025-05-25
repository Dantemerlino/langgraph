from states import UserInputState, QuestionState, DataState, AnswerState
from bigquery_tools import execute_sql_query, get_table_schema, list_tables # Import BQ tools
from typing import List, Any # For type hinting
import re # For keyword extraction

def generate_questions_agent(state: UserInputState) -> QuestionState:
    """
    Generates questions based on user input using simple keyword matching.
    """
    print(f"DEBUG: generate_questions_agent received input: {state.user_input}")
    user_input_lower = state.user_input.lower()
    questions = []

    if "capital" in user_input_lower:
        if "france" in user_input_lower:
            questions.append("What is the capital of France?")
        else:
            questions.append("What are some known capitals?")
    
    if "schema" in user_input_lower:
        if "customer" in user_input_lower:
            questions.append("What is the schema of the customer_details table?")
        elif "order" in user_input_lower:
            questions.append("What is the schema of the order_summary table?")
        else:
            questions.append("Can you list schemas for available tables?")

    if "how does" in user_input_lower and "work" in user_input_lower:
        # Find the topic between "how does" and "work"
        match = re.search(r"how does (.*) work", user_input_lower)
        if match and match.group(1):
            questions.append(f"How does {match.group(1).strip()} work?")
        else:
            questions.append("Explain a general concept.")


    if "order" in user_input_lower and "what" in user_input_lower: # e.g. "what are the orders"
        questions.append("Show me some recent orders.")
    
    if "customer" in user_input_lower and ("who" in user_input_lower or "details" in user_input_lower) :
         questions.append("Show me some customer details.")

    if not questions: # Default question if no keywords match
        questions.append(f"Can you provide general information about: {state.user_input}?")
    
    # Limit to 2 questions for simplicity
    final_questions = questions[:2]
    print(f"DEBUG: generate_questions_agent produced questions: {final_questions}")
    return QuestionState(questions=final_questions)

def retrieve_data_agent(state: QuestionState) -> DataState:
    """
    Retrieves data based on the generated questions.
    Uses updated bigquery_tools.py for more dynamic simulation.
    `can_answer` is true if any simulated query returns a non-empty result.
    """
    print(f"DEBUG: retrieve_data_agent received questions: {state.questions}")
    
    retrieved_data_for_all_questions = []
    any_question_answered_with_data = False

    # Get simulated table list to help form more "realistic" simulated queries
    available_tables = list_tables().get("tables", [])

    for q_text in state.questions:
        q_text_lower = q_text.lower()
        # Attempt to make a slightly more relevant simulated query
        # This is still very basic and for simulation purposes.
        simulated_query = f"SELECT * FROM placeholder_table WHERE content CONTAINS '{q_text_lower[:30]}...'" # Default query
        
        # Try to pick a table based on question keywords
        if "capital" in q_text_lower and "capitals_data" in available_tables:
            simulated_query = f"SELECT * FROM capitals_data WHERE question_hint = '{q_text_lower}'"
        elif "schema" in q_text_lower and "schema_info" in available_tables:
            if "customer" in q_text_lower:
                 simulated_query = f"SELECT columns FROM schema_info WHERE table_name = 'customer_details'"
            elif "order" in q_text_lower:
                 simulated_query = f"SELECT columns FROM schema_info WHERE table_name = 'order_summary'"
            else:
                simulated_query = f"SELECT * FROM schema_info"
        elif ("order" in q_text_lower or "orders" in q_text_lower) and "order_summary" in available_tables:
            simulated_query = f"SELECT * FROM order_summary LIMIT 2"
        elif ("customer" in q_text_lower or "customers" in q_text_lower) and "customer_details" in available_tables:
            simulated_query = f"SELECT * FROM customer_details LIMIT 2"

        print(f"DEBUG: retrieve_data_agent attempting simulated query: '{simulated_query}' for question: '{q_text}'")
        query_result_dict = execute_sql_query(simulated_query)
        actual_data_from_query = query_result_dict.get("result", [])
        
        current_question_data = {
            "question": q_text,
            "query_attempted": simulated_query,
            "data": actual_data_from_query if actual_data_from_query else "No specific data found from simulation."
        }
        retrieved_data_for_all_questions.append(current_question_data)

        if actual_data_from_query: # Check if the list is not empty
            any_question_answered_with_data = True
            print(f"DEBUG: retrieve_data_agent: Found data for question '{q_text}'")
        else:
            print(f"DEBUG: retrieve_data_agent: No data found for question '{q_text}' from query '{simulated_query}'")


    if any_question_answered_with_data:
        print("DEBUG: retrieve_data_agent determined can_answer = True")
        return DataState(retrieved_data=retrieved_data_for_all_questions, can_answer=True)
    else:
        print("DEBUG: retrieve_data_agent determined can_answer = False")
        return DataState(retrieved_data=retrieved_data_for_all_questions, can_answer=False)


def generate_answer_agent(state: DataState) -> AnswerState:
    """
    Generates an answer based on the retrieved data.
    Tries to incorporate some of the retrieved data into the answer.
    """
    print(f"DEBUG: generate_answer_agent received DataState with can_answer={state.can_answer}")
    if state.can_answer and state.retrieved_data:
        # Try to find the first piece of actual data to include
        summary_parts = []
        for item in state.retrieved_data:
            if isinstance(item, dict) and item.get("data") and item["data"] != "No specific data found from simulation.":
                # Take the first element of the data list if it's a list, or the data itself
                first_data_point = item["data"]
                if isinstance(first_data_point, list) and first_data_point:
                    summary_parts.append(f"For '{item['question']}': {str(first_data_point[0])[:100]}...")
                elif not isinstance(first_data_point, list):
                     summary_parts.append(f"For '{item['question']}': {str(first_data_point)[:100]}...")
        
        if summary_parts:
            answer = "Based on the retrieved data: " + " | ".join(summary_parts)
        else:
            answer = "I found some information, but couldn't summarize it clearly. The data has been retrieved."
        
        print(f"DEBUG: generate_answer_agent produced answer: {answer}")
        return AnswerState(answer=answer)
    else:
        final_answer = "I could not find enough specific information to answer the questions."
        print(f"DEBUG: generate_answer_agent produced answer: {final_answer}")
        return AnswerState(answer=final_answer)

def cannot_answer_agent(state: DataState) -> AnswerState:
    """
    Generates a specific message when the agent cannot answer.
    """
    print("DEBUG: cannot_answer_agent was called.")
    # The state.retrieved_data might contain info on why it couldn't answer
    reason = "available data"
    if state.retrieved_data and isinstance(state.retrieved_data, list):
        # Check if all items report no specific data
        all_no_data = True
        for item_data in state.retrieved_data:
            if isinstance(item_data, dict) and item_data.get("data") and item_data.get("data") != "No specific data found from simulation.":
                all_no_data = False
                break
        if all_no_data:
            reason = "simulated environment did not yield specific results for the queries"

    final_answer = f"Sorry, I cannot answer the question with the {reason}."
    print(f"DEBUG: cannot_answer_agent produced answer: {final_answer}")
    return AnswerState(answer=final_answer)
