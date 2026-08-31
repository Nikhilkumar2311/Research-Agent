import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter 
from langchain_core.messages import HumanMessage, SystemMessage
from state import AgentState

# Load API keys from .env file
load_dotenv()

# Initialize the dynamic Free Models Router
llm = ChatOpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openrouter/free",
    temperature=0.7
)

def raw_html_search(query: str) -> str:
    """
    A pure-Python fallback search that safely executes a web search 
    without relying on unstable local wrapper packages.
    """
    try:
        # Encode the text string for the web URL
        safe_query = urllib.parse.quote_plus(query)
        # Using a reliable free, unauthenticated search API fallback (Text-only)
        url = f"https://duckduckgo.com{safe_query}"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Extract snippets from the raw duckduckgo HTML structure simply
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        snippets = [links.text.strip() for links in soup.find_all('a', class_='result__snippet')][:5]
        
        if snippets:
            return "\n\n".join(snippets)
        return "No snippets found in html. Falling back."
    except Exception as e:
        return f"Web search link retrieval timed out or failed. ({str(e)})"


def search_node(state: AgentState) -> dict:
    """
    Node 1: Acts as our researcher. It fetches live, real-time context data.
    """
    print("\n--- STARTING RESEARCH NODE ---")
    topic = state["topic"]
    revision_count = state.get("revision_count", 0)
    critique = state.get("critique", "")
    
    print(f"=== Searching the live web for: '{topic}'... ===")
    
    # Execute our pure-python search function
    search_query = topic
    if revision_count > 0 and critique:
        search_query = f"{topic} missing details updates"
        
    web_results = raw_html_search(search_query)

    # Feed search results into the LLM
    if revision_count > 0:
        prompt = f"""You are an advanced AI researcher. The previous newsletter draft on '{topic}' was rejected by the editor.
        Editor Feedback: {critique}
        
        Fresh Web Search Results:
        {web_results}
        
        Synthesize these search results and extract concrete facts, statistics, and answers that address the editor's complaints."""
    else:
        prompt = f"""You are an advanced AI researcher. Review these live web search results about '{topic}':
        
        Web Search Results:
        {web_results}
        
        Synthesize this information into a dense, highly informative factual summary. Focus on recent breakthroughs, definitions, and technical insights."""

    messages = [
        SystemMessage(content="You are a meticulous research analyst. Combine raw web data into clean, structured factual summaries."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return {
        "research_notes": response.content,
        "revision_count": revision_count + 1
    }


def writer_node(state: AgentState) -> dict:
    """
    Node 2: Takes the gathered research notes and writes a beautifully structured, 
    highly engaging newsletter.
    """
    print("\n--- STARTING WRITER NODE ---")
    topic = state["topic"]
    notes = state["research_notes"]
    
    prompt = f"""You are an expert tech newsletter copywriter. Write an engaging, highly professional newsletter.
    
    Topic: {topic}
    Factual Research Summary to Use: {notes}
    
    Structure your newsletter with:
    1. A catchy, clickable Subject Line / Headline
    2. An introductory hook
    3. A deep dive section breaking down technical facts simply
    4. A 'Why it matters' takeaway section.
    
    Write the complete text of the newsletter now. Do not talk to the user, just provide the article text."""

    messages = [
        SystemMessage(content="You are a professional tech journalist. You never write fluff; you present facts elegantly."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return {"draft": response.content}


def editor_node(state: AgentState) -> dict:
    """
    Node 3: Quality assurance agent. It reads the draft and decides whether to approve or loop back.
    """
    print("\n--- STARTING EDITOR NODE ---")
    topic = state["topic"]
    draft = state["draft"]
    
    prompt = f"""You are a strict Editor-in-Chief. Evaluate the following newsletter draft written about '{topic}'.
    
    Newsletter Draft:
    -----------
    {draft}
    -----------
    
    Critique requirements:
    1. Is it deeply detailed? If it is missing hard facts or deep insights, criticize it.
    2. Is the tone right?
    
    CRITICAL RULE: If the newsletter is excellent, detailed, and ready to publish, end your critique with the exact token word: APPROVED.
    If it needs improvements, list your detailed complaints and do NOT say APPROVED."""

    messages = [
        SystemMessage(content="You are an uncompromising editor. Your job is to enforce absolute quality."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return {"critique": response.content}
