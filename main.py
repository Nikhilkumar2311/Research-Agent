from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import search_node, writer_node, editor_node
from edges import should_continue

# 1. Initialize the StateGraph with our blueprint state schema
workflow = StateGraph(AgentState)

# 2. Add our nodes to the graph 
# The first argument is a nickname string, the second is the actual Python function
workflow.add_node("researcher", search_node)
workflow.add_node("writer", writer_node)
workflow.add_node("editor", editor_node)

# 3. Connect the nodes with Edges
# Set the starting point of the agent execution stream
workflow.set_entry_point("researcher")

# Linear edge: Once research is done, always hand off to the writer
workflow.add_edge("researcher", "writer")

# Linear edge: Once the writer finishes the draft, always hand off to the editor
workflow.add_edge("writer", "editor")

# 4. Add the Conditional Edge (The Logic Loop)
# After the 'editor' node runs, it calls the 'should_continue' function.
# 'should_continue' will look at the state and return either "end" or "continue".
# We map those strings to the actual targets: END or the "researcher" node.
workflow.add_conditional_edges(
    "editor",
    should_continue,
    {
        "end": END,                 # If the function returns "end", go to the built-in END node
        "continue": "researcher"    # If the function returns "continue", loop back to the researcher
    }
)

# 5. Compile the graph into a runnable LangChain Application
app = workflow.compile()

# 6. Execute and test our agent!
if __name__ == "__main__":
    print("====AI Newsletter Agent Initialized!====")
    
    # Prompt the user for an input topic
    user_topic = input("Enter a newsletter topic (e.g., Quantum Computing Breakthroughs): ")
    
    # Initialize our graph state with the starting topic and a revision counter set to 0
    initial_state = {
        "topic": user_topic,
        "revision_count": 0,
        "research_notes": "",
        "draft": "",
        "critique": ""
    }
    
    # Run the compiled agent graph
    print("\n====Executing Agent Workflow. Please wait...====")
    final_output = app.invoke(initial_state)
    
    # Print the final result once the loop terminates successfully
    print("\n==================================================")
    print("====FINAL APPROVED NEWSLETTER GENERATED SUCCESSFULLY:====")
    print("==================================================\n")
    print(final_output["draft"])
    print("\n==================================================")
