# NEXUS AI
### Enterprise Agentic AI Platform for Autonomous Workflow Automation & Intelligent Decision-Making

NEXUS AI is a Streamlit-based portfolio project demonstrating a multi-agent workflow pattern for enterprise knowledge work. It combines task planning, lightweight knowledge retrieval, data profiling, draft generation and a quality-review stage.

**Developed by Mohamed Riyaz S.**  
Integrated M.Tech CSE | Business Analytics — VIT Chennai

## Features

- Five-stage specialist-agent workflow: Planner, Researcher, Analyst, Execution and Quality.
- Demo mode that works without an API key.
- Optional live LLM mode using the OpenAI API.
- Session-scoped knowledge uploads: PDF, TXT, Markdown and CSV.
- Lightweight keyword-based context retrieval from uploaded sources.
- CSV profiling, missing-value checks, duplicate checks and numeric visualizations.
- Workflow templates for customer feedback, policy review, market research and incident summaries.
- Downloadable Markdown workflow report.
- Human-review reminders and responsible-AI limitations.

## Run locally

```bash
git clone https://github.com/YOUR-USERNAME/nexus-ai-agentic-platform.git
cd nexus-ai-agentic-platform
python -m venv .venv
```

Activate the environment:

**Windows**
```powershell
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install and launch:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in your terminal (usually `http://localhost:8501`).

## Enable live LLM mode

1. Create an API key with your chosen provider supported by the OpenAI Python SDK.
2. Set the environment variable `OPENAI_API_KEY`.
3. Restart the app and choose **Live LLM mode** in the sidebar.

Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your_api_key"
streamlit run app.py
```

Do not commit API keys, `.env` files or Streamlit secrets to GitHub.

## Deploy on Render

This repository includes `render.yaml`.

1. Push the project folder to a new GitHub repository.
2. In Render, choose **New + → Blueprint**.
3. Connect the GitHub repository and deploy the detected service.
4. For live LLM mode, add `OPENAI_API_KEY` under the Render service's Environment settings.
5. Open the public `onrender.com` URL and test the dashboard in Demo mode first.

The Render service can start without an API key; Demo mode remains available. Live LLM usage may incur provider charges.

## Architecture

```text
User request
    |
    v
Planner Agent
    |
    v
Research Agent <--- Uploaded knowledge sources
    |
    v
Analyst Agent
    |
    v
Execution Agent
    |
    v
Quality Agent
    |
    v
Human review / downloadable report
```

## Technology stack

- Python
- Streamlit
- OpenAI Python SDK (optional live mode)
- Pandas
- Plotly
- pypdf

## Important implementation notes

This is a portfolio demonstration, not a production enterprise agent platform. Demo mode uses illustrative outputs. Live mode calls an LLM sequentially for each agent stage. Document retrieval currently uses lightweight keyword matching rather than a production vector database. Uploaded files remain in the current Streamlit session and are not stored in a persistent document repository. The app does not execute external actions.

For production use, add authentication, authorization, persistent vector storage, audit logging, evaluation datasets, rate limiting, secret management, source-level citations, monitoring and explicit approval gates for every consequential action.

## Responsible use

- Do not upload confidential, personal, regulated or sensitive information.
- Verify AI-generated content before relying on it.
- Keep API keys in environment variables or a secrets manager.
- Do not treat model output as legal, financial, medical or security advice.
- Human approval must precede consequential business actions.

## License

MIT License. See `LICENSE`.
