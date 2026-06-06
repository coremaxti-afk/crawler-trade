-- H8 Graph / Shotmap storage schema
-- Approved scope: schema/migration for H8 raw imports only.
-- No features, datasets, modeling, or raw-data mutation.

begin;

create table if not exists match_graph (
    id bigserial primary key,
    sofascore_event_id bigint,
    minute integer,
    momentum_value numeric,
    match_id bigint
);

alter table match_graph add column if not exists point_index integer;
alter table match_graph add column if not exists source_name text not null default 'sofascore';
alter table match_graph add column if not exists artifact_name text not null default 'graph.json';
alter table match_graph add column if not exists raw_file_path text;
alter table match_graph add column if not exists raw_payload_hash text;
alter table match_graph add column if not exists imported_at timestamptz;

alter table match_graph drop column if exists value;

alter table match_graph alter column source_name set default 'sofascore';
alter table match_graph alter column artifact_name set default 'graph.json';

create unique index if not exists uq_match_graph_event_point
    on match_graph (sofascore_event_id, point_index);

create index if not exists ix_match_graph_match_id
    on match_graph (match_id);

create table if not exists match_shotmap (
    id bigserial primary key,
    sofascore_event_id bigint not null,
    shot_index integer not null,
    minute integer,
    added_time integer,
    time_seconds integer,
    team_id bigint,
    team_name text,
    player_id bigint,
    player_name text,
    shot_type text,
    goal_mouth_location text,
    xg numeric,
    xgot numeric,
    player_coordinates_json jsonb,
    goal_mouth_coordinates_json jsonb,
    draw_json jsonb,
    source_name text not null default 'sofascore',
    artifact_name text not null default 'shotmap.json',
    raw_file_path text not null,
    raw_payload_hash text not null,
    imported_at timestamptz not null
);

create unique index if not exists uq_match_shotmap_event_shot
    on match_shotmap (sofascore_event_id, shot_index);

create index if not exists ix_match_shotmap_event
    on match_shotmap (sofascore_event_id);

create table if not exists match_source_status (
    id bigserial primary key,
    sofascore_event_id bigint not null,
    source_name text not null,
    artifact_name text not null,
    status text not null,
    http_status integer,
    decision text,
    reason text,
    raw_file_path text,
    raw_payload_hash text,
    checked_at timestamptz not null
);

create unique index if not exists uq_match_source_status_event_source_artifact
    on match_source_status (sofascore_event_id, source_name, artifact_name);

create index if not exists ix_match_source_status_status
    on match_source_status (source_name, artifact_name, status);

commit;
