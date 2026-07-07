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

class ContextFinding(BaseModel):
    category: str  # injury, rest_day, scratch, platoon, transaction, manager_comment
    detail: str
    source: str

class Verdict(BaseModel):
    materially_different: bool
    explained_by_context: bool
    should_publish: bool
    rationale: str
