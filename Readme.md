# 🤖 Autonomous AI Research & Newsletter Agent

An advanced, stateful multi-agent system built using **LangGraph** and **LangChain** that automates the process of researching the live web, writing deeply engaging technical articles, and autonomously editing them based on quality criteria loops.

---

## 📐 Architecture Blueprint

The system uses a cyclical graph architecture containing 3 core nodes and a state-driven conditional edge router:

```text
[START]
   │
   ▼
┌─────────────────────────┐
│     Research Node       │ ◄─────────────────────────┐
│ (Python Scraper + LLM)  │                           │
└──────────┬──────────────┘                           │
           │                                          │
           ▼                                          │ (If "NEEDS WORK")
┌─────────────────────────┐                           │
│      Writer Node        │                           │
│  (Newsletter Drafting)  │                           │
└──────────┬──────────────┘                           │
           │                                          │
           ▼                                          │
┌─────────────────────────┐                           │
│      Editor Node        │                           │
│  (Quality Assurance)    │                           │
└──────────┬──────────────┘                           │
           │                                          │
           ▼                                          │
┌─────────────────────────┐                           │
│  Conditional Router     ├───────────────────────────┘
│  (should_continue?)     │
└──────────┬──────────────┘
           │
           │ (If "APPROVED" or Max Revisions Hit)
           ▼
        [END]
```

### How it Works:

1. **Research Node:** Takes a user topic, utilizes a pure-Python scraping pipeline via DuckDuckGo and `BeautifulSoup` to fetch live data streams, and creates an aggregated context report.
2. **Writer Node:** Processes the factual context reports into an elegantly structured markdown newsletter format.
3. **Editor Node:** Critiques the generated newsletter against strict factual guidelines. If it's shallow, it locks an improvement notice into the shared state and kicks off a correction cycle.
4. **Conditional Edge:** Automatically monitors revision count limits (max 3 tries) or checks if the editor declared the token `APPROVED` to gracefully conclude the graph execution stream.

---

## 🛠️ Tech Stack & Tooling

- **Orchestration:** LangGraph (StateGraph, Nodes, Conditional Edges)
- **Framework:** LangChain Core / Community
- **LLM Connectivity:** OpenRouter API Wrapper (`openrouter/free` fallback cluster)
- **Data Scraping:** Pure Python `urllib` & `BeautifulSoup4`

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Nikhilkumar2311/Research-Agent.git
cd Research-Agent
```

### 2. Set up a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root folder:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5. Run the Agent

```bash
python main.py
```
