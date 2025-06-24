# 🤖 Autonomous AI Marketing Agent for SMBs

An intelligent, multi-agent system designed to automate key marketing tasks for local small-to-medium-sized businesses. This project leverages a hierarchical agent architecture to delegate tasks, use external tools, and generate creative, on-brand marketing content.

### ✨ Key Features

* **Multi-Agent Architecture:** A high-level **Manager Agent** analyzes user goals and delegates tasks to specialized agents, creating a scalable and organized system.
* **Specialist Agents:**
    * **"Spark" (Social Media Agent):** Creatively generates social media posts, complete with captions and detailed image descriptions.
    * **"Echo" (Reputation Agent):** Empathetically analyzes and drafts professional responses to customer reviews.
* **Autonomous Tool Use:** Agents can autonomously decide to use external tools (like a web search) to gather real-time information and enrich their outputs.
* **Dynamic & Customizable:** The agent system can be configured for any business by simply editing the business profile in the user-friendly web interface.
* **Interactive Web UI:** Built with Streamlit for a clean, responsive, and easy-to-use experience.

### 🏗️ System Architecture

The project follows a hierarchical, manager-worker agent model:

```
[ User Input (Goal + Business Profile) ]
               |
               v
      +--------------------+
      |   Manager Agent    |  (Analyzes Goal & Delegates)
      +--------------------+
               |
      +--------+---------+
      |                  |
      v                  v
+--------------+   +---------------+
| Social Media |   |  Reputation   |
| Agent (Spark)|   | Agent (Echo)  |
+--------------+   +---------------+
      |                  |
      v                  v
+--------------+   +---------------+
|   Toolbox    |   |    Toolbox    |  (Web Search,   (Get Reviews API)
|              |   | Social Post)  |
+--------------+   +---------------+
      |                  |
      v                  v
[ Final Output ]   [ Final Output ]
```

### 🛠️ Tech Stack

* **Backend:** Python 3.11+
* **LLM:** Alibaba Cloud Qwen (`qwen-max`) via the Dashscope API
* **Core Logic:**
    * `openai` Python Client (for its standardized API interface)
    * Agentic Design (ReAct-style loop for reasoning and acting)
* **Web Interface:** Streamlit
* **Tools:** Tavily Search API (for AI-optimized web searches)
* **Environment Management:** `uv`

### 🚀 Setup and Installation

Follow these steps to get the project running locally.

**1. Clone the Repository**
```bash
git clone [Your-GitHub-Repository-URL]
cd smb-marketing-agent
```

**2. Create and Activate Virtual Environment**
This project uses `uv` for fast environment management.
```bash
# Install uv if you haven't already
pip install uv

# Create the virtual environment
uv venv

# Activate it (for PowerShell)
.\.venv\Scripts\Activate.ps1
```

**3. Install Dependencies**
`uv` will install all required packages from the `requirements.txt` file.
```bash
uv pip install -r requirements.txt
```

**4. Set Up Environment Variables**
You will need API keys for the Qwen LLM and the Tavily Search tool.

* Create a copy of `.env.example` and rename it to `.env`.
* Open the `.env` file and add your secret keys:

```ini
# Get from Alibaba Cloud Model Studio dashboard
QWEN_API_KEY="your_qwen_api_key_here"

# Get from tavily.com dashboard
TAVILY_API_KEY="your_tavily_api_key_here"
```

### ▶️ How to Run

Once the setup is complete, run the Streamlit web application from the project's root directory:

```bash
streamlit run src/app.py
```

Your web browser should automatically open with the interactive UI.
