-- Optimization results produced by the offline pipeline.
-- One row per (game, team, optimizer version) so results stay reproducible
-- across optimizer upgrades.

create table if not exists optimization_results (
    id bigint generated always as identity primary key,
    game_id text not null,
    team text not null,
    game_date date not null,
    announced_lineup jsonb not null,   -- ordered list of player names, slots 1-9
    optimized_lineup jsonb not null,
    announced_expected_runs double precision not null,
    optimized_expected_runs double precision not null,
    improvement double precision not null,
    optimizer_version text not null,
    created_at timestamptz not null default now(),
    unique (game_id, team, optimizer_version)
);

create index if not exists optimization_results_date_team
    on optimization_results (game_date, team);
