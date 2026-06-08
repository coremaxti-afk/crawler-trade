-- Football-Data storage schema
-- Approved scope: controlled Phase 1 migration for Football-Data odds.
-- No features, datasets, modeling, crawlers, or full-season import.

begin;

create table if not exists football_data_csv_files (
    id bigserial primary key,
    competition_code text not null,
    season text not null,
    source_name text not null default 'football-data',
    source_url text,
    source_file text not null,
    source_hash text not null,
    downloaded_at timestamptz,
    registered_at timestamptz not null default now(),
    row_count integer,
    notes text
);

create unique index if not exists uq_football_data_csv_files_source_hash
    on football_data_csv_files (source_hash);

create index if not exists ix_football_data_csv_files_source_hash
    on football_data_csv_files (source_hash);

create index if not exists ix_football_data_csv_files_competition_season
    on football_data_csv_files (competition_code, season);

create index if not exists ix_football_data_csv_files_source_file
    on football_data_csv_files (source_file);

create table if not exists football_data_staging_rows (
    id bigserial primary key,
    csv_file_id bigint not null references football_data_csv_files(id) on delete restrict,
    source_hash text not null,
    row_number integer not null,
    raw_row_json jsonb not null,
    division text,
    match_date timestamp without time zone,
    home_team_raw text,
    away_team_raw text,
    home_goals integer,
    away_goals integer,
    result_raw text,
    created_at timestamptz not null default now()
);

create unique index if not exists uq_football_data_staging_rows_source_row
    on football_data_staging_rows (source_hash, row_number);

create index if not exists ix_football_data_staging_rows_match_date
    on football_data_staging_rows (match_date);

create index if not exists ix_football_data_staging_rows_home_away_raw
    on football_data_staging_rows (home_team_raw, away_team_raw);

create index if not exists ix_football_data_staging_rows_csv_file_id
    on football_data_staging_rows (csv_file_id);

create table if not exists football_data_match_mapping (
    id bigserial primary key,
    staging_row_id bigint not null references football_data_staging_rows(id) on delete restrict,
    source_hash text not null,
    row_number integer not null,
    sofascore_event_id bigint,
    match_id bigint references matches_master(match_id) on delete restrict,
    mapping_status text not null,
    mapping_method text,
    home_team_normalized text,
    away_team_normalized text,
    score_check_status text,
    ambiguity_flag boolean not null default false,
    conflict_reason text,
    mapped_at timestamptz not null default now()
);

create unique index if not exists uq_football_data_match_mapping_source_row
    on football_data_match_mapping (source_hash, row_number);

create index if not exists ix_football_data_match_mapping_sofascore_event_id
    on football_data_match_mapping (sofascore_event_id);

create index if not exists ix_football_data_match_mapping_match_id
    on football_data_match_mapping (match_id);

create index if not exists ix_football_data_match_mapping_status
    on football_data_match_mapping (mapping_status);

create index if not exists ix_football_data_match_mapping_source_row
    on football_data_match_mapping (source_hash, row_number);

create table if not exists football_data_odds (
    id bigserial primary key,
    staging_row_id bigint not null references football_data_staging_rows(id) on delete restrict,
    mapping_id bigint not null references football_data_match_mapping(id) on delete restrict,
    match_id bigint not null references matches_master(match_id) on delete restrict,
    sofascore_event_id bigint not null,
    source_hash text not null,
    source_file text not null,
    source_url text,
    row_number integer not null,
    market text not null,
    selection text not null,
    handicap_line text,
    handicap_line_key text not null default '',
    odds_type text not null,
    bookmaker_or_aggregator text not null,
    odds_value numeric not null,
    source_column text not null,
    source_column_semantics text,
    is_closing boolean not null default false,
    is_opening_like boolean not null default false,
    is_average boolean not null default false,
    is_maximum boolean not null default false,
    imported_at timestamptz not null default now()
);

create unique index if not exists uq_football_data_odds_grain
    on football_data_odds (
        sofascore_event_id,
        market,
        selection,
        handicap_line_key,
        odds_type,
        bookmaker_or_aggregator,
        source_hash
    );

create index if not exists ix_football_data_odds_sofascore_event_id
    on football_data_odds (sofascore_event_id);

create index if not exists ix_football_data_odds_match_id
    on football_data_odds (match_id);

create index if not exists ix_football_data_odds_market_selection
    on football_data_odds (market, selection);

create index if not exists ix_football_data_odds_odds_type
    on football_data_odds (odds_type);

create index if not exists ix_football_data_odds_bookmaker
    on football_data_odds (bookmaker_or_aggregator);

create index if not exists ix_football_data_odds_source_hash
    on football_data_odds (source_hash);

create index if not exists ix_football_data_odds_market_odds_type
    on football_data_odds (market, odds_type);

commit;
