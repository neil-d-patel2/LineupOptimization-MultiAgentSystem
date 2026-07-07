from datetime import date, datetime
from pydantic import BaseModel

class OptimizationResult(BaseModel):
    game_id: str
    team: str
    game_date: date
    announced_lineup: list[str]
    optimized_lineup: list[str]
    announced_expected_runs: float
    optimized_expected_runs: float
    improvement: float
    optimizer_version: str
    created_at: datetime | None = None

    # shared by the reasoning and writing prompts — both must describe the result identically
    def summary(self) -> str:
        return (f'Game {self.game_id}, {self.team}, {self.game_date} (optimizer {self.optimizer_version}):\n'
                f'- Announced lineup: {self.announced_lineup}\n'
                f'- Optimized lineup: {self.optimized_lineup}\n'
                f'- Expected runs announced: {self.announced_expected_runs:.3f}\n'
                f'- Expected runs optimized: {self.optimized_expected_runs:.3f}\n'
                f'- Expected improvement: {self.improvement:.3f} runs/game')

class ContextFinding(BaseModel):
    category: str  # injury, rest_day, scratch, platoon, transaction, manager_comment
    detail: str
    source: str

def findings_block(context: list[ContextFinding]) -> str:
    return '\n'.join(f'- [{f.category}] {f.detail} ({f.source})' for f in context) or '- none found'

class Verdict(BaseModel):
    materially_different: bool
    explained_by_context: bool
    should_publish: bool
    rationale: str
