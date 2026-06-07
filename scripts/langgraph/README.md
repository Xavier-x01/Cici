# Cici Session Ritual Orchestrator

LangGraph state machine that runs session-start, proposal review, and memory audit as a single conditional graph.

## Install

```bash
pip install -r scripts/langgraph/requirements.txt
```

## Run

```bash
# Full session report (Markdown to stdout)
python3 scripts/langgraph/cli.py

# Dump state as JSON (useful for debugging)
python3 scripts/langgraph/cli.py --dry-run

# Explicit repo root
python3 scripts/langgraph/cli.py --repo-root /path/to/Cici
```

## Graph

```
load_context → run_dossier → [conditional]
  proposals > 0  → proposal_review → synthesize
  stub surfaces  → memory_audit   → synthesize
  clean state    →                   synthesize
```

## Structure

```
scripts/langgraph/
├── cli.py               # entry point
├── graph.py             # StateGraph assembly
├── state.py             # SessionState TypedDict
├── routing.py           # route_branches() — pure function
├── requirements.txt
└── nodes/
    ├── load_context.py      # reads proposals/queue/ and open-loops.md
    ├── run_dossier.py       # calls generate-dossier.py functions
    ├── proposal_review.py   # schema + conflict checks
    ├── memory_audit.py      # Tier C leak scan, overdue proposal check
    └── synthesize_report.py # assembles final Markdown report
```

## Extending

- **Add an LLM node:** import `ChatAnthropic` from `langchain_anthropic`, create a node after `synthesize`, gate with `--llm` flag.
- **Run both branches:** change `route_branches` to return a `Send` list for parallel execution.
- **Persistent checkpoints:** swap `MemorySaver()` for `SqliteSaver("session.db")` in `graph.py`.
