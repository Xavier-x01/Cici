"""
Stub: evaluate an AI action against core creation goals.

Goals checked:
  1. Alignment    — does the action match the user's real intent?
  2. Robustness   — does it handle edge cases?
  3. Transparency — is the reasoning visible?
  4. Bounded agency — does it stay within scope?
  5. Harm avoidance — is the action reversible / low blast-radius?
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ActionProposal:
    description: str
    intent: str                        # what the user actually asked for
    scope: str                         # what domain/surface this touches
    reversible: bool
    reasoning: Optional[str] = None    # explanation of why this action was chosen


@dataclass
class GoalCheckResult:
    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.failed) == 0

    def report(self) -> str:
        lines = []
        for g in self.passed:
            lines.append(f"  [PASS] {g}")
        for g in self.failed:
            lines.append(f"  [FAIL] {g}")
        lines.append(f"\nResult: {'OK' if self.ok else 'BLOCKED'}")
        return "\n".join(lines)


def check(proposal: ActionProposal) -> GoalCheckResult:
    result = GoalCheckResult()

    # 1. Alignment — action description must reference the stated intent
    if proposal.intent.lower() in proposal.description.lower():
        result.passed.append("alignment")
    else:
        result.failed.append("alignment — action does not clearly map to stated intent")

    # 2. Robustness — stub: always pass; real check would run against test cases
    result.passed.append("robustness (stub — wire to test suite)")

    # 3. Transparency — reasoning must be provided
    if proposal.reasoning:
        result.passed.append("transparency")
    else:
        result.failed.append("transparency — no reasoning provided")

    # 4. Bounded agency — scope must be a single named surface
    if proposal.scope and " " not in proposal.scope.strip():
        result.passed.append("bounded agency")
    else:
        result.failed.append("bounded agency — scope is too broad or unspecified")

    # 5. Harm avoidance — irreversible actions are blocked by default
    if proposal.reversible:
        result.passed.append("harm avoidance")
    else:
        result.failed.append("harm avoidance — action is irreversible; requires explicit approval")

    return result


if __name__ == "__main__":
    example = ActionProposal(
        description="Update the user's memory profile with new preferences",
        intent="update memory",
        scope="governed-state/memory",
        reversible=True,
        reasoning="User explicitly asked to store new preferences in the memory layer.",
    )

    result = check(example)
    print(result.report())
