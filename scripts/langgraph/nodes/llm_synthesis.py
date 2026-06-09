from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from state import SessionState


def llm_synthesis_node(state: SessionState) -> dict:
    errors = list(state.get("errors", []))
    report = state.get("report", "")
    run_date = state.get("run_date", "unknown")

    lane_lines = []
    for ls in state.get("lane_statuses", []):
        blockers = ls.get("open_blockers", [])
        lane_lines.append(f"  {ls['lane']}: {len(blockers)} open loop(s)")
        for b in blockers[:2]:
            lane_lines.append(f"    - {b}")
    lanes_text = "\n".join(lane_lines) or "  No lane data."

    prompt = (
        f"You are Cici, Xavier's AI assistant for the BrewMind project. "
        f"Today is {run_date}.\n\n"
        "Below is the session status report. Write exactly 3 short, actionable bullet points "
        "as a 'Today's Focus' section. Each bullet covers a different domain: governance, "
        "work lanes, or memory/pipeline. Be specific and direct. No preamble.\n\n"
        f"Session Report:\n{report}\n\n"
        f"Work Lane Summary:\n{lanes_text}\n\n"
        "Write only the 3 bullets."
    )

    try:
        llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
        response = llm.invoke([HumanMessage(content=prompt)])
        summary = response.content
    except Exception as e:
        errors.append(f"llm_synthesis: {e}")
        summary = ""

    # Append the summary to the existing report so the final report field is complete
    current_report = state.get("report", "")
    if summary:
        updated_report = current_report + f"\n---\n\n### Today's Focus\n\n{summary}\n"
    else:
        updated_report = current_report

    return {"llm_summary": summary, "report": updated_report, "errors": errors}
