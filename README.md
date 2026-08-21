# Dependency Update Agent

An AI-powered dependency analysis system that evaluates whether upgrading a Python dependency is likely to affect a repository.

## What it does

The system:

1. Parses Python dependency requirements.
2. Checks current and latest package versions.
3. Retrieves relevant changelog information using hybrid RAG.
4. Searches the repository using AST-based code analysis.
5. Uses an LLM to assess upgrade impact.
6. Exposes the capabilities as LangChain tools.
7. Uses `create_agent` to orchestrate the analysis.
8. Stores analysis results in SQLite.
9. Evaluates the system against a small test suite.

## Architecture

```text
Repository
    ↓
Dependency Parser
    ↓
Version Analysis
    ↓
Changelog Retrieval
    ├── Dense Retrieval
    └── BM25
           ↓
      Hybrid Results
           ↓
      AST Code Search
           ↓
      Impact Judgment
           ↓
     Dependency Agent
           ↓
         SQLite
