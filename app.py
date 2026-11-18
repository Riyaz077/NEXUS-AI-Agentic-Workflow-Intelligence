import os
import io
import json
import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

st.set_page_config(
    page_title="NEXUS AI | Agentic Intelligence",
    page_icon="assets/nexus_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --nexus-cyan:#25D5F2; --nexus-blue:#5A8DEE; --nexus-bg:#081626; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(circle at 80% 0%, #122C49 0%, #081626 42%, #071321 100%); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0B1C30,#071321); border-right:1px solid #1B3653; }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; }
.hero { padding:28px 30px; border:1px solid #234765; border-radius:18px;
        background:linear-gradient(120deg,rgba(18,54,83,.95),rgba(8,25,43,.92));
        box-shadow:0 14px 40px rgba(0,0,0,.18); }
.hero-kicker { color:#27D8F4; font-weight:700; letter-spacing:2px; font-size:12px; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:38px; font-weight:700; color:#F4FAFF; margin:6px 0; }
.hero-sub { color:#A9C5E0; font-size:15px; max-width:850px; }
.metric-card { padding:16px 18px; border:1px solid #24425F; border-radius:13px;
               background:rgba(13,34,55,.82); min-height:105px; }
.metric-label { color:#8FAFCB; font-size:12px; text-transform:uppercase; letter-spacing:1px; }
.metric-value { color:#F4FAFF; font-size:27px; font-weight:700; margin-top:7px; }
.metric-note { color:#28D5F0; font-size:11px; margin-top:2px; }
.panel { padding:18px; border:1px solid #24425F; border-radius:14px; background:rgba(10,29,48,.75); }
.agent { border:1px solid #24425F; border-radius:12px; padding:14px; background:rgba(14,39,62,.72); }
.agent-name { color:#EAF6FF; font-weight:700; }
.agent-role { color:#8FB2D0; font-size:12px; }
.small-muted { color:#8FAFCB; font-size:12px; }
div.stButton > button { border-radius:9px; border:1px solid #2D7898; }
div.stButton > button[kind="primary"] { background:linear-gradient(90deg,#087FA8,#16B9D5); border:0; }
.footer { margin-top:48px; padding:34px 18px 24px; text-align:center; border-top:1px solid #1D3852; }
/* NEXUS AI Premium Footer */
.footer {
    position: relative;
    margin-top: 55px;
    padding: 38px 25px 22px;
    text-align: center;
    border: 1px solid rgba(37, 213, 242, 0.16);
    border-radius: 16px;
    background: linear-gradient(
        145deg,
        rgba(15, 39, 62, 0.95),
        rgba(5, 19, 34, 0.98)
    );
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.20);
    overflow: hidden;
}

.footer::before {
    content: "";
    position: absolute;
    top: 0;
    left: 12%;
    width: 76%;
    height: 2px;
    background: linear-gradient(
        90deg,
        transparent,
        #25D5F2,
        #5A8DEE,
        #25D5F2,
        transparent
    );
}

.footer-title {
    color: #25D5F2;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.3px;
    line-height: 1.7;
    margin-bottom: 25px;
}

.footer-meta {
    color: #91B8D9;
    font-size: 14px;
    margin: 9px 0;
}

.footer-name {
    color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin: 9px 0;
    text-shadow: 0 0 18px rgba(37, 213, 242, 0.16);
}

.footer-link {
    display: inline-block;
    margin-top: 12px;
    padding: 9px 20px;
    border: 1px solid rgba(37, 213, 242, 0.4);
    border-radius: 25px;
    color: #25D5F2 !important;
    font-size: 12px;
    font-weight: 600;
    text-decoration: none !important;
    transition: all 0.3s ease;
}

.footer-divider {
    width: 85%;
    height: 1px;
    margin: 30px auto 18px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(37, 213, 242, 0.65),
        rgba(90, 141, 238, 0.65),
        transparent
    );
}

.footer-copy {
    color: #789AB9;
    font-size: 11px;
    letter-spacing: 0.4px;
    padding-top: 2px;
}
.stTabs [data-baseweb="tab"] { color:#A8C5DE; }
.stTabs [aria-selected="true"] { color:#25D5F2 !important; }



/* NEXUS AI — Refined Premium Navigation */

div[data-testid="stSegmentedControl"] {
    width: 100% !important;
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;

    padding: 7px !important;
    gap: 6px !important;
    margin-top: 5px;

    background: linear-gradient(
        110deg,
        #0D2034,
        #0A192A
    ) !important;

    border: 1px solid rgba(104, 151, 185, 0.19) !important;
    border-radius: 12px !important;

    box-shadow: 0 6px 20px rgba(0,0,0,0.14);
}

/* Content-based tab sizing */
div[data-testid="stSegmentedControl"] button {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: max-content !important;
    min-height: 75px !important;

    padding: 12px 22px !important;

    display: flex !important;
    justify-content: center !important;
    align-items: center !important;

    background: transparent !important;
    color: #A6BBD0 !important;

    border: 1px solid transparent !important;
    border-radius: 8px !important;

    font-size: 13px !important;
    font-weight: 550 !important;

    white-space: nowrap !important;
    transition: all 0.22s ease !important;
}

/* Hover */
div[data-testid="stSegmentedControl"] button:hover {
    background: rgba(37, 213, 242, 0.055) !important;
    color: #35D8F3 !important;
    border-color: rgba(37, 213, 242, 0.16) !important;
}

/* Selected tab */
div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
    background: linear-gradient(
        135deg,
        #123D56,
        #10405A
    ) !important;

    color: #36D9F4 !important;

    border: 1px solid rgba(37, 213, 242, 0.42) !important;

    font-weight: 650 !important;

    box-shadow: 0 3px 12px rgba(0,190,225,0.10);
}

/* Responsive horizontal scrolling */
div[data-testid="stSegmentedControl"] {
    overflow-x: auto !important;
}

div[data-testid="stSegmentedControl"] button:focus-visible {
    outline: 2px solid #25D5F2;
    outline-offset: 2px;
}




</style>
""", unsafe_allow_html=True)

AGENTS = [
    ("Planner Agent", "Breaks a request into clear, ordered tasks", "◈"),
    ("Research Agent", "Finds context from your uploaded knowledge base", "⌕"),
    ("Analyst Agent", "Structures evidence and identifies patterns", "⌁"),
    ("Execution Agent", "Produces the requested business deliverable", "↗"),
    ("Quality Agent", "Checks completeness, consistency and risks", "✓"),
]

def get_api_key():
    try:
        return st.secrets.get("OPENAI_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
    except Exception:
        return os.getenv("OPENAI_API_KEY", "")

def llm_enabled():
    return bool(get_api_key()) and OpenAI is not None

def ask_llm(system_prompt, user_prompt, model="gpt-4o-mini"):
    client = OpenAI(api_key=get_api_key())
    response = client.chat.completions.create(
        model=model,
        temperature=0.25,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""

def demo_agent_output(agent, request, context):
    examples = {
        "Planner Agent": f"""**Objective:** {request}

1. Clarify the business outcome and success criteria.
2. Gather relevant context from the knowledge base and supplied data.
3. Analyze the evidence and identify key findings.
4. Prepare an actionable deliverable.
5. Review the output for accuracy, assumptions and missing information.

**Execution plan:** Research → Analyze → Synthesize → Review.""",
        "Research Agent": f"""The knowledge retrieval stage has been completed in demonstration mode.

**Available context:** {context[:1100] if context else "No documents uploaded yet. The workflow will proceed using the request itself."}

**Research note:** In live mode, connect approved enterprise sources and retrieve relevant passages with source-level traceability.""",
        "Analyst Agent": """**Analysis framework**
- Separate verified facts from assumptions.
- Identify relevant entities, constraints, dependencies and risks.
- Compare options against the stated objective.
- Prioritize recommendations by impact, effort and confidence.

**Evidence status:** Demonstration analysis. Connect a model and source documents for evidence-grounded analysis.""",
        "Execution Agent": f"""## Draft deliverable

**Request:** {request}

**Recommended approach**
1. Start with a clearly scoped pilot and measurable success criteria.
2. Assign an owner to each action and define approval checkpoints.
3. Track operational impact, exceptions and user feedback.
4. Expand only after quality and risk checks pass.

**Next action:** Validate the assumptions with a domain owner before operational use.""",
        "Quality Agent": """**Quality review**
- Objective and proposed steps are aligned.
- Assumptions are identified rather than presented as facts.
- Human review is required before external or consequential actions.
- No live external action was executed in this demonstration.
- Validate figures, sources and domain-specific requirements before use.

**Review status:** Passed demonstration checklist with human verification required."""
    }
    return examples.get(agent, "No output generated.")

def retrieve_context(query, docs):
    if not docs:
        return ""
    q_terms = {x.lower() for x in query.split() if len(x) > 2}
    ranked = []
    for name, text in docs:
        paragraphs = [p.strip() for p in text.splitlines() if len(p.strip()) > 35]
        for p in paragraphs:
            terms = {x.lower().strip(".,:;!?()[]{}") for x in p.split()}
            score = len(q_terms & terms)
            if score:
                ranked.append((score, name, p))
    ranked.sort(reverse=True, key=lambda x: x[0])
    return "\n\n".join([f"[Source: {name}] {p}" for _, name, p in ranked[:6]])

def extract_text(upload):
    name = upload.name.lower()
    raw = upload.getvalue()
    if name.endswith(".txt") or name.endswith(".md"):
        return raw.decode("utf-8", errors="ignore")
    if name.endswith(".csv"):
        try:
            return pd.read_csv(io.BytesIO(raw)).head(100).to_string(index=False)
        except Exception:
            return ""
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw))
            return "\n".join((page.extract_text() or "") for page in reader.pages[:30])
        except Exception:
            return "[PDF extraction unavailable. Install pypdf and retry.]"
    return ""

def metric(label, value, note):
    st.markdown(f"""<div class="metric-card"><div class="metric-label">{label}</div>
    <div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>""", unsafe_allow_html=True)

if "runs" not in st.session_state:
    st.session_state.runs = []
if "documents" not in st.session_state:
    st.session_state.documents = []
if "latest_outputs" not in st.session_state:
    st.session_state.latest_outputs = {}

# ---------- Sidebar ----------
with st.sidebar:
    st.image("assets/nexus_logo.png", width=85)
    st.markdown("## NEXUS AI")
    st.caption("ENTERPRISE AGENTIC INTELLIGENCE")
    st.markdown("---")
    st.markdown("**Runtime configuration**")
    mode = st.selectbox("Execution mode", ["Demo mode", "Live LLM mode"], index=0)
    model_name = st.selectbox("LLM model", ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4o"], index=0)
    if mode == "Live LLM mode":
        if llm_enabled():
            st.success("API key detected")
        else:
            st.warning("Add OPENAI_API_KEY in Render environment variables to enable live mode.")
    st.markdown("---")
    st.caption("Human approval is required before consequential actions.")

# ---------- Header ----------

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="hero-kicker">AUTONOMOUS WORKFLOW INTELLIGENCE</div>
  <div class="hero-title">NEXUS AI</div>
  <div class="hero-sub">
    An enterprise agentic AI workspace that plans tasks, retrieves knowledge,
    analyzes information, creates deliverables and reviews outputs through coordinated specialist agents.
  </div>
</div>
""", unsafe_allow_html=True)


# ---------- Premium Workspace Navigation ----------

st.html("""
<div style="
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 25px;
    margin-bottom: 12px;
">
    <div style="
        width: 3px;
        height: 16px;
        border-radius: 5px;
        background: #25D5F2;
        box-shadow: 0 0 10px rgba(37,213,242,0.4);
    "></div>

    <span style="
        color: #A9C5DE;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.8px;
    ">
        WORKSPACE NAVIGATION
    </span>

    <div style="
        flex: 1;
        height: 1px;
        background: linear-gradient(
            90deg,
            rgba(70,120,155,0.35),
            transparent
        );
    "></div>
</div>
""")

page = st.segmented_control(
    "Workspace",
    options=[
        "Overview",
        "Agent Workspace",
        "Knowledge Hub",
        "Data Intelligence",
        "Workflow Lab",
        "Evaluation & Logs"
    ],
    default="Overview",
    label_visibility="collapsed",
    key="workspace_navigation",
    width="stretch"
)

st.write("")



# ---------- Pages ----------
if page == "Overview":
    st.subheader("Platform Overview")
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric("Specialist agents", "05", "Coordinated workflow")
    with c2: metric("Knowledge sources", str(len(st.session_state.documents)).zfill(2), "Uploaded this session")
    with c3: metric("Workflow runs", str(len(st.session_state.runs)).zfill(2), "Current session")
    with c4: metric("Execution mode", "LIVE" if mode == "Live LLM mode" and llm_enabled() else "DEMO", "Runtime status")
    st.write("")
    left,right = st.columns([1.25,1])
    with left:
        st.markdown("### Multi-agent orchestration")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        for i,(name,role,ico) in enumerate(AGENTS):
            st.markdown(f'<div class="agent"><span class="agent-name">{ico} &nbsp;{name}</span><br><span class="agent-role">{role}</span></div>', unsafe_allow_html=True)
            if i < len(AGENTS)-1:
                st.markdown("<div style='text-align:center;color:#28CDEB;padding:3px'>↓</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("### Core capabilities")
        for title,desc in [
            ("Agent orchestration","Specialized agents coordinate a multi-step task."),
            ("Enterprise RAG","Retrieve relevant information from uploaded PDF, TXT, MD and CSV files."),
            ("Data intelligence","Explore CSV data, profile columns and generate quick visual analysis."),
            ("Human-in-the-loop","Review outputs before using them in consequential workflows."),
            ("Quality assurance","Run a structured review for completeness, risks and assumptions."),
        ]:
            st.markdown(f"**{title}**")
            st.caption(desc)
        st.info("Demo mode uses transparent illustrative outputs. Configure an API key to run live LLM-powered agent stages.")
    st.markdown("### Suggested use cases")
    usecols = st.columns(3)
    for col,(t,d) in zip(usecols,[
        ("Business research","Prepare structured market or competitor research briefs."),
        ("Knowledge assistant","Ask questions against internal policy and project documents."),
        ("Decision support","Turn a business question into an analysis and action plan."),
    ]):
        with col:
            st.markdown(f'<div class="panel"><b>{t}</b><p class="small-muted">{d}</p></div>', unsafe_allow_html=True)

elif page == "Agent Workspace":
    st.subheader("Agent Workspace")
    st.caption("Submit a business request and let the specialist-agent pipeline create a reviewed draft.")
    request = st.text_area("What would you like the agents to accomplish?",
        placeholder="Example: Analyze the uploaded customer feedback and prepare an executive summary with the top issues, evidence and recommended actions.",
        height=130)
    context = retrieve_context(request, st.session_state.documents) if request else ""
    if st.session_state.documents:
        st.caption(f"Knowledge retrieval is available across {len(st.session_state.documents)} uploaded source(s).")
    run = st.button("Run agent workflow", type="primary", disabled=not request.strip(), use_container_width=True)
    if run:
        if mode == "Live LLM mode" and not llm_enabled():
            st.error("Live mode requires the openai package and OPENAI_API_KEY. Add the key in Render environment variables or switch to Demo mode.")
        else:
            outputs = {}
            progress = st.progress(0, text="Initializing agent team...")
            prompts = {
                "Planner Agent": "You are a careful enterprise workflow planner. Create a concise step-by-step plan. Do not claim to have taken actions.",
                "Research Agent": "You are an enterprise research agent. Use only supplied context and clearly state when evidence is missing. Do not invent sources.",
                "Analyst Agent": "You are an analytical agent. Separate facts, assumptions, risks and recommendations. Be concise and evidence-aware.",
                "Execution Agent": "You are an enterprise execution agent. Produce the requested draft deliverable. Never claim external actions were completed.",
                "Quality Agent": "You are a strict quality reviewer. Check factual grounding, completeness, risks and need for human approval. Provide a final review.",
            }
            prior = ""
            try:
                for idx,(agent,_,_) in enumerate(AGENTS):
                    progress.progress((idx+1)/len(AGENTS), text=f"{agent} working...")
                    if mode == "Live LLM mode":
                        user_prompt = f"Business request:\n{request}\n\nRetrieved context:\n{context or 'No source documents retrieved.'}\n\nPrevious agent outputs:\n{prior[-9000:]}"
                        out = ask_llm(prompts[agent], user_prompt, model_name)
                    else:
                        out = demo_agent_output(agent, request, context)
                    outputs[agent] = out
                    prior += f"\n\n### {agent}\n{out}"
                progress.empty()
                st.session_state.latest_outputs = outputs
                st.session_state.runs.insert(0, {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "request": request[:120],
                    "mode": "Live" if mode == "Live LLM mode" else "Demo",
                    "status": "Completed"
                })
                st.success("Workflow completed. Review each agent's output before using it.")
            except Exception as e:
                progress.empty()
                st.error(f"Workflow failed: {e}")
    if st.session_state.latest_outputs:
        st.markdown("### Workflow results")
        for agent,_,_ in AGENTS:
            with st.expander(agent, expanded=(agent == "Execution Agent")):
                st.markdown(st.session_state.latest_outputs.get(agent, "No output."))
        full = "\n\n".join([f"# {a}\n{o}" for a,o in st.session_state.latest_outputs.items()])
        st.download_button("Download workflow report", full, file_name="nexus_ai_workflow_report.md", mime="text/markdown")

elif page == "Knowledge Hub":
    st.subheader("Enterprise Knowledge Hub")
    st.caption("Upload reference documents to make them available as context for the agent workflow.")
    uploads = st.file_uploader("Add knowledge sources", type=["pdf","txt","md","csv"], accept_multiple_files=True)
    if uploads:
        added = 0
        existing = {n for n,_ in st.session_state.documents}
        for up in uploads:
            if up.name not in existing:
                txt = extract_text(up)
                if txt.strip():
                    st.session_state.documents.append((up.name, txt))
                    added += 1
        if added:
            st.success(f"Added {added} source(s) to this session.")
    st.markdown("### Indexed sources")
    if st.session_state.documents:
        for name,txt in st.session_state.documents:
            with st.expander(f"{name} · {len(txt):,} characters"):
                st.text(txt[:2500] + ("..." if len(txt)>2500 else ""))
        if st.button("Clear knowledge sources"):
            st.session_state.documents = []
            st.rerun()
    else:
        st.info("No sources uploaded yet. Add PDFs, text, Markdown or CSV files to begin.")
    st.warning("Uploaded files are held in the current app session and are not permanently stored. Avoid uploading confidential or sensitive data.")

elif page == "Data Intelligence":
    st.subheader("Data Intelligence")
    st.caption("Upload a CSV file for exploratory profiling and visual analysis.")
    csv_file = st.file_uploader("Upload dataset", type=["csv"], key="data_csv")
    if csv_file:
        try:
            df = pd.read_csv(csv_file)
            st.markdown("### Dataset snapshot")
            a,b,c,d = st.columns(4)
            with a: metric("Rows", f"{len(df):,}", "Records")
            with b: metric("Columns", str(len(df.columns)), "Features")
            with c: metric("Missing cells", f"{int(df.isna().sum().sum()):,}", "Across dataset")
            with d: metric("Duplicate rows", f"{int(df.duplicated().sum()):,}", "Exact duplicates")
            st.dataframe(df.head(100), use_container_width=True)
            st.markdown("### Column profile")
            profile = pd.DataFrame({
                "Column": df.columns,
                "Data type": [str(x) for x in df.dtypes],
                "Missing": [int(df[x].isna().sum()) for x in df.columns],
                "Unique values": [int(df[x].nunique(dropna=True)) for x in df.columns],
            })
            st.dataframe(profile, use_container_width=True, hide_index=True)
            numeric = df.select_dtypes(include="number").columns.tolist()
            if numeric:
                st.markdown("### Numeric distribution")
                selected = st.selectbox("Choose a numeric feature", numeric)
                fig = px.histogram(df, x=selected, marginal="box", template="plotly_dark",
                                   title=f"Distribution of {selected}")
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("### Descriptive statistics")
                st.dataframe(df[numeric].describe().T, use_container_width=True)
        except Exception as e:
            st.error(f"Could not read the CSV: {e}")
    else:
        st.info("Upload a CSV dataset to explore its structure, quality and numeric distributions.")

elif page == "Workflow Lab":
    st.subheader("Workflow Lab")
    st.caption("Explore practical agentic workflow patterns. These are planning templates; no external system is modified.")
    templates = {
        "Customer feedback intelligence": "Analyze customer feedback, cluster recurring themes, identify urgent issues and draft a prioritized improvement plan.",
        "Policy and compliance assistant": "Review the supplied policy documents, answer a question with supporting excerpts and flag ambiguities for human review.",
        "Market research brief": "Create a market research brief with scope, key questions, evidence requirements, competitor comparison and strategic implications.",
        "Operations incident summary": "Summarize an operations incident, build a timeline from supplied evidence, identify impact and propose follow-up actions.",
    }
    selected = st.selectbox("Choose a workflow template", list(templates.keys()))
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f"**{selected}**")
    st.write(templates[selected])
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Use this in Agent Workspace", type="primary"):
        st.session_state.workflow_template = templates[selected]
        st.success("Template ready. Copy it into the Agent Workspace request field.")
        st.code(templates[selected])

elif page == "Evaluation & Logs":
    st.subheader("Evaluation & Run History")
    if st.session_state.runs:
        st.dataframe(pd.DataFrame(st.session_state.runs), use_container_width=True, hide_index=True)
    else:
        st.info("No workflow runs in this session yet.")
    st.markdown("### Responsible AI checklist")
    checks = [
        "Retrieved evidence is relevant to the user request.",
        "Claims are traceable to provided sources where applicable.",
        "Assumptions and uncertainty are clearly labelled.",
        "A human reviews outputs before consequential decisions.",
        "No credentials or confidential data are exposed in logs.",
        "Agent outputs are evaluated for quality and failure cases.",
    ]
    for item in checks:
        st.checkbox(item, key="check_"+str(checks.index(item)))
    st.markdown("### Current system limitations")
    st.markdown("""
    - Demo mode produces illustrative workflow outputs, not genuine model reasoning.
    - Live mode uses an LLM API but does not guarantee factual accuracy.
    - Retrieval in this starter implementation uses lightweight keyword matching, not a production vector database.
    - No external business action, email, payment, account change or system command is executed.
    - Uploaded documents are session-scoped and are not persisted as a managed enterprise knowledge store.
    """)


# ---------- NEXUS AI Premium Footer ----------

import html

public_url = os.getenv("NEXUS_PUBLIC_URL", "").strip()

if public_url.startswith("https://"):
    public_link_html = f"""
        <a class="footer-link"
           href="{html.escape(public_url, quote=True)}"
           target="_blank"
           rel="noopener noreferrer">
           ↗ &nbsp; OPEN PUBLIC LIVE DEMO
        </a>
    """
else:
    public_link_html = """
        <div class="footer-meta">
            Public live-demo link will appear after deployment.
        </div>
    """

footer_html = f"""
<div class="footer">

    <div class="footer-title">
        NEXUS AI — Enterprise Agentic AI Platform
        for Autonomous Workflow Automation
        &amp; Intelligent Decision-Making
    </div>

    <div class="footer-meta">
        DESIGNED &amp; DEVELOPED BY
    </div>

    <div class="footer-name">
        Mohamed Riyaz S.
    </div>

    <div class="footer-meta">
        Integrated M.Tech CSE | Business Analytics
    </div>

    <div class="footer-meta">
        VIT Chennai
    </div>

    {public_link_html}

    <div class="footer-divider"></div>

    <div class="footer-copy">
        © 2026 Mohamed Riyaz S. | All Rights Reserved.
    </div>

</div>
"""

st.html(footer_html)

