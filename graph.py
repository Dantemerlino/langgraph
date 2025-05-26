from typing import TypedDict, List, Any
from langgraph.graph import StateGraph, END

# Import agent functions and state models
from agents import generate_questions_agent, retrieve_data_agent, generate_answer_agent, cannot_answer_agent
from states import UserInputState, QuestionState, DataState, AnswerState

# Define the aggregate State TypedDict for the graph
class State(TypedDict):
    user_input: str
    questions: List[str]
    retrieved_data: Any
    can_answer: bool
    answer: str

class Workflow(StateGraph):
    def __init__(self):
        super().__init__(State)

        self.add_node("question_generator", generate_questions_agent)
        self.add_node("data_retriever", retrieve_data_agent)
        self.add_node("answer_generator", generate_answer_agent)
        self.add_node("cannot_answer_node", cannot_answer_agent)

        self.set_entry_point("question_generator")
        self.add_edge("question_generator", "data_retriever")
        self.add_conditional_edges(
            "data_retriever",
            self.should_generate_answer,
            {
                "generate_answer": "answer_generator",
                "cannot_answer": "cannot_answer_node"
            }
        )
        self.add_edge("answer_generator", END)
        self.add_edge("cannot_answer_node", END)

    def should_generate_answer(self, state: State) -> str:
        """
        Determines the next step based on whether the agent can answer.
        """
        print(f"DEBUG: graph.py should_generate_answer: current can_answer state is {state.get('can_answer')}")
        if state.get("can_answer"):
            return "generate_answer"
        else:
            return "cannot_answer"

app = Workflow().compile()

if __name__ == "__main__":
    print("Graph compiled. 'app' instance is ready.")
    
    # Define a list of sample inputs to test different paths
    sample_inputs = [
        "What is the capital of France and its schema?",
        "Tell me about orders from last week and also what is the schema of the customers table?",
        "How does the internet work?",
        "What are the details for customer Smith and their recent orders?",
        "Explain black holes." # Should likely result in "cannot answer"
    ]

    for i, user_input_string in enumerate(sample_inputs):
        print(f"\n===== Test Case {i+1} =====")
        initial_state = {"user_input": user_input_string}

        print(f"--- Initial User Input ---")
        print(user_input_string)
        print("\n------------------------\n")

        print("--- Streaming Events (DEBUG agent outputs will appear during stream) ---")
        final_output_from_invoke = None
        try:
            # Stream events to see intermediate steps and agent DEBUG logs
            for event_count, event in enumerate(app.stream(initial_state, {"recursion_limit": 5})):
                # The event dictionary's keys are node names
                for node_name, output_data in event.items():
                    print(f"--- Event {event_count + 1}: Node '{node_name}' Output ---")
                    # The 'output_data' here is what the node *returned*, 
                    # which is a partial state (e.g., QuestionState, DataState).
                    if hasattr(output_data, 'model_dump_json'):
                        print(f"Output (JSON): {output_data.model_dump_json(indent=2)}")
                    else:
                        print(f"Output: {output_data}")
                    print("-------------------------")
            
            # Get the final state using invoke
            final_output_from_invoke = app.invoke(initial_state, {"recursion_limit": 5})

        except Exception as e:
            print(f"Error during graph execution for input: '{user_input_string}'")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            print("-------------------------")
            continue # Move to next test case

        print("\n--- Final Output ---")
        if final_output_from_invoke and final_output_from_invoke.get("answer"):
            print(f"User Input: {user_input_string}")
            print(f"Final Answer: {final_output_from_invoke['answer']}")
            if "Sorry, I cannot answer" in final_output_from_invoke['answer'] or \
               "could not find enough specific information" in final_output_from_invoke['answer']:
                print("Outcome: Agent determined it could not answer fully.")
            else:
                print("Outcome: Agent provided an answer.")
        else:
            print(f"User Input: {user_input_string}")
            print(f"No definitive answer in final output. Full final state: {final_output_from_invoke}")
            print("Outcome: Agent may not have reached a final answer state.")
        print("=======================\n")
