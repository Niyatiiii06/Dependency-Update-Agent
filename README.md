# Dependency Update Agent

An AI-powered dependency analysis system that evaluates whether upgrading a Python dependency is likely to affect a repository.

The system combines dependency parsing, version analysis, hybrid RAG, AST-based code search, tool-calling agents, structured impact judgment, SQLite persistence, and evaluation.

## What It Does

Given a Python repository and a dependency update, the system:

1. Parses the repository's dependency requirements.
2. Compares the current and latest package versions.
3. Retrieves relevant changelog and release-note information.
4. Uses dense and BM25 retrieval for hybrid search.
5. Searches the repository using Python AST analysis.
6. Compares changelog evidence with actual code usage.
7. Uses an LLM to determine upgrade impact.
8. Exposes analysis capabilities as LangChain tools.
9. Uses `create_agent` to orchestrate the analysis.
10. Stores structured analysis results in SQLite.
11. Evaluates the system against a small test set.

## Architecture

```text
                    Python Repository
                           |
                           v
                  Dependency Parser
                           |
                           v
                   Version Analysis
                    /            \
                   /              \
                  v                v
        Current Version       Latest Version
                                   |
                                   v
                         Changelog / Releases
                                   |
                         +---------+---------+
                         |                   |
                         v                   v
                 Dense Retrieval          BM25
                         |                   |
                         +---------+---------+
                                   |
                                   v
                            Hybrid Retrieval
                                   |
                                   v
                           Relevant Evidence
                                   |
                    +--------------+--------------+
                    |                             |
                    v                             v
             AST Code Search              Changelog Evidence
                    |                             |
                    +--------------+--------------+
                                   |
                                   v
                           Impact Judgment
                                   |
                                   v
                       Structured ImpactDecision
                                   |
                                   v
                             Dependency Agent
                                   |
                                   v
                                SQLite
                                   |
                                   v
                              Evaluation
```

## Example

Consider:

```text
pandas 2.1.4 → 3.0.5
```

The system may retrieve a breaking change such as:

```text
DataFrame.append() and Series.append() were removed.
```

The AST code search can then find:

```python
df.append(...)
```

inside the target repository.

The judgment layer combines both pieces of evidence:

```text
Changelog:
DataFrame.append() was removed.

Repository:
df.append() is used.

Result:
Affected = True
Impact = High
```

The system can then recommend migrating the affected code before upgrading.

## Project Structure

```text
dependency-update/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── dependency/
│   ├── __init__.py
│   ├── parser.py
│   ├── version.py
│   ├── latest.py
│   └── checker.py
│
├── ingestion/
│   ├── __init__.py
│   └── changelog_loader.py
│
├── search/
│   ├── __init__.py
│   ├── code_search.py
│   └── hybrid_search.py
│
├── judgment/
│   ├── __init__.py
│   └── judge.py
│
├── tools/
│   ├── __init__.py
│   ├── dependency_tools.py
│   ├── search_tools.py
│   └── judgment_tools.py
│
├── agents/
│   ├── __init__.py
│   └── dependency_agent.py
│
├── analysis/
│   ├── __init__.py
│   └── dependency_impact.py
│
├── storage/
│   ├── __init__.py
│   └── database.py
│
├── evaluation/
│   ├── __init__.py
│   ├── cases.py
│   └── run_eval.py
│
└── sample_project/
    ├── requirements.txt
    ├── app.py
    └── sample_changelog.txt
```

## Retrieval Pipeline

The changelog retrieval system uses two complementary approaches.

### Dense Retrieval

Changelog chunks are embedded and stored in ChromaDB. Semantic similarity is used to find conceptually relevant information.

### BM25 Retrieval

BM25 provides keyword-based retrieval. This is useful when the query contains exact package names, API names, or terminology from release notes.

### Hybrid Retrieval

The dense and BM25 results are combined to improve the chance of retrieving both semantically relevant and exact-match evidence.

```text
Query
  |
  +----> Dense Retrieval
  |
  +----> BM25 Retrieval
             |
             v
       Hybrid Results
```

## Code Intelligence

The project reuses an AST-based Python code search system.

It uses Python's `ast` module to identify:

* Function definitions
* Method definitions
* Function calls
* Method calls
* Imports
* Callers

This allows the system to connect dependency changes with actual code usage.

For example:

```text
Changelog:
DataFrame.append() removed

        +

AST:
df.append() found in sample_project/app.py

        ↓

Potential compatibility issue
```

## Agent Architecture

The Dependency Update Agent is built with LangChain's `create_agent`.

The agent has access to tools for:

```text
Dependency version checking
        |
        v
Changelog search
        |
        v
Repository code search
        |
        v
Impact assessment
```

The agent can choose when to call these tools instead of requiring the entire workflow to be hard-coded.

## Structured Judgment

The impact layer returns a structured result containing:

```text
affected
impact
reason
recommendation
```

The structured output allows the result to be used programmatically and stored in SQLite.

Example:

```text
Affected: True
Impact: High

Reason:
The changelog states that DataFrame.append() was removed,
and the repository uses df.append().

Recommendation:
Migrate to pandas.concat() before upgrading.
```

## Storage

SQLite stores completed dependency analyses.

The current schema stores:

```text
package
current_version
target_version
affected
impact
reason
recommendation
```

This allows analysis results to be retrieved later instead of existing only in the console output.

## Evaluation

The project includes a small evaluation suite with five manually constructed cases.

Current result:

```text
5 / 5 cases passed
100% accuracy
```

The evaluation includes scenarios such as:

```text
Removed API + API used
Removed API + API not used
Unused indexing API
Unused groupby API
Nonexistent API
```

The 100% result applies only to this current five-case evaluation set. It should not be interpreted as real-world production accuracy.

## Installation

Clone the repository and create a virtual environment.

Install the dependencies:

```bash
uv pip install -r requirements.txt
```

Create a `.env` file containing the required API key:

```text
MISTRAL_API_KEY=your_api_key
```

Do not commit `.env` or API keys to GitHub.

## Running the Agent

Run:

```bash
python main.py
```

Example request:

```text
Analyze the pandas dependency update from 2.1.4 to 3.0.5 in sample_project.
Check breaking changes, search for affected APIs, and determine the impact.
```

## Running the Evaluation

Run:

```bash
python -m evaluation.run_eval
```

Expected output:

```text
Passed: 5/5
Accuracy: 100%
```

## Scope

The current implementation intentionally focuses on Python projects.

Supported dependency workflow:

```text
requirements.txt
```

The project does not currently target Node.js dependency ecosystems such as:

```text
package.json
package-lock.json
yarn.lock
pnpm-lock.yaml
```

## Limitations

This is a production-oriented prototype rather than a fully hardened production service.

Current limitations include:

* Small evaluation dataset
* Prepared changelog input
* Limited dependency-file support
* No automatic pull-request creation
* No deployment infrastructure
* No authentication layer
* No large-scale observability system

## Future Improvements

Possible future improvements include:

* Reciprocal Rank Fusion for more principled hybrid retrieval
* Cross-encoder reranking
* Better version-aware changelog retrieval
* Larger automated evaluation datasets
* Automatic changelog ingestion
* GitHub repository integration
* Automatic branch and pull-request creation
* FastAPI interface
* Production monitoring and observability
* Support for additional dependency ecosystems

## Tech Stack

```text
Python
LangChain
Mistral
ChromaDB
BM25
Python AST
Pydantic
SQLite
PyPI API
```

## Key Learning Outcomes

This project demonstrates practical experience with:

```text
RAG
Hybrid Retrieval
Sparse Retrieval
Dense Retrieval
Vector Databases
AST Code Analysis
Tool Calling
LLM Agents
Structured Output
Agentic Workflows
SQLite
Evaluation
```

The main goal is not simply to answer questions about dependencies, but to connect **external dependency-change evidence with the actual codebase** and determine whether an upgrade is likely to affect the project.
