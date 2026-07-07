import os
import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from app.models import OptimizationResult

def connect():
    return psycopg.connect(os.environ['DATABASE_URL'], row_factory=dict_row)

def store_result(result: OptimizationResult) -> None:
    with connect() as conn:
        conn.execute(
            """insert into optimization_results
                   (game_id, team, game_date, announced_lineup, optimized_lineup,
                    announced_expected_runs, optimized_expected_runs, improvement,
                    optimizer_version)
               values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               on conflict (game_id, team, optimizer_version) do update set
                   announced_lineup = excluded.announced_lineup,
                   optimized_lineup = excluded.optimized_lineup,
                   announced_expected_runs = excluded.announced_expected_runs,
                   optimized_expected_runs = excluded.optimized_expected_runs,
                   improvement = excluded.improvement""",
            (result.game_id, result.team, result.game_date,
             Jsonb(result.announced_lineup), Jsonb(result.optimized_lineup),
             result.announced_expected_runs, result.optimized_expected_runs,
             result.improvement, result.optimizer_version))

def fetch_result(game_id: str, team: str) -> OptimizationResult | None:
    with connect() as conn:
        row = conn.execute(
            """select * from optimization_results
               where game_id = %s and team = %s
               order by created_at desc limit 1""",
            (game_id, team)).fetchone()
    return OptimizationResult(**row) if row else None
