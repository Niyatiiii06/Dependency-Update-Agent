import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from agents.dependency_agent import dependency_agent
from storage.database import get_analyses, init_db

st.set_page_config(page_title="Dependency Update Agent", layout="wide")
init_db()

st.title("🔍 Dependency Update Agent")
st.caption(
    "AI-powered dependency impact analysis using Hybrid RAG, "
    "Python AST code search, and agentic reasoning."
)

with st.sidebar:
    st.header("Run Analysis")

    repo_path = st.text_input("Repository path", "sample_project")
    package = st.text_input("Package", "pandas")
    current = st.text_input("Current version", "2.1.4")
    target = st.text_input("Target version", "3.0.5")

    analyze = st.button("🚀 Analyze", type="primary", use_container_width=True)

if analyze:
    if not repo_path or not package:
        st.error("Repository path and package are required.")
    else:
        query = (
            f"Analyze the {package} dependency update from "
            f"{current} to {target} in {repo_path}. "
            f"Check breaking changes, search for affected APIs, "
            f"and determine the impact."
        )

        with st.spinner("Analyzing..."):
            try:
                result = dependency_agent.invoke({
                    "messages": [
                        {"role": "user", "content": query}
                    ]
                })

                st.session_state["result"] = result["messages"][-1].content
                st.session_state["error"] = None

            except Exception as e:
                st.session_state["result"] = None
                st.session_state["error"] = str(e)

if st.session_state.get("error"):
    st.error(st.session_state["error"])

if st.session_state.get("result"):
    result_text = st.session_state["result"]

    st.subheader("📊 Analysis Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Version", current)

    with col2:
        st.metric("Target Version", target)

    with col3:
        if (
            "impact = high" in result_text.lower()
            or "**high**" in result_text.lower()
        ):
            st.error("🔴 HIGH RISK")
        elif (
            "impact = medium" in result_text.lower()
            or "**medium**" in result_text.lower()
        ):
            st.warning("🟠 MEDIUM RISK")
        else:
            st.success("🟢 LOW RISK")

    if (
        "affected=true" in result_text.lower()
        or "affected: true" in result_text.lower()
    ):
        st.error("⚠️ This upgrade affects the repository")
    elif (
        "affected=false" in result_text.lower()
        or "affected: false" in result_text.lower()
    ):
        st.success("✅ No relevant impact detected")

    st.subheader("🔍 Detailed Analysis")
    st.markdown(result_text)


# ==========================================================
# HISTORY TABLE
# ==========================================================

try:
    records = get_analyses()

    if records:
        columns = [
            "id",
            "package",
            "current_version",
            "target_version",
            "affected",
            "impact",
            "reason",
            "recommendation",
        ]

        df = pd.DataFrame(records, columns=columns)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No analyses yet.")

except Exception as e:
    st.warning(f"Couldn't load history: {e}")


st.divider()

st.caption(
    "LangChain • Mistral • ChromaDB • BM25 • Python AST • SQLite"
)