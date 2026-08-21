create table public.experiments (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  created_by uuid not null references public.profiles(id) on delete restrict,
  signal_id uuid,
  decision_id uuid,
  title text not null,
  hypothesis text,
  test_variable text not null,
  locked_variables jsonb not null default '[]'::jsonb,
  status text not null default 'draft' check (status in ('draft','running','completed','cancelled','archived')),
  learning text,
  next_experiment_id uuid,
  metadata jsonb not null default '{}'::jsonb,
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint experiments_title_not_blank_check check (char_length(btrim(title)) between 1 and 160),
  constraint experiments_test_variable_not_blank_check check (char_length(btrim(test_variable)) between 1 and 160),
  constraint experiments_time_order_check check (completed_at is null or started_at is null or completed_at >= started_at),
  constraint experiments_signal_project_fkey foreign key (signal_id, project_id)
    references public.signals (id, project_id) on delete set null (signal_id),
  constraint experiments_decision_project_fkey foreign key (decision_id, project_id)
    references public.decisions (id, project_id) on delete set null (decision_id),
  constraint experiments_project_identity_unique unique (id, project_id)
);

create table public.experiment_variants (
  id uuid primary key default gen_random_uuid(),
  experiment_id uuid not null,
  project_id uuid not null,
  created_by uuid not null references public.profiles(id) on delete restrict,
  label text not null,
  ordinal smallint not null,
  variable_value jsonb not null default '{}'::jsonb,
  artifact_id uuid,
  result jsonb not null default '{}'::jsonb,
  score numeric,
  is_winner boolean not null default false,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint experiment_variants_label_not_blank_check check (char_length(btrim(label)) between 1 and 40),
  constraint experiment_variants_ordinal_positive_check check (ordinal > 0),
  constraint experiment_variants_experiment_project_fkey foreign key (experiment_id, project_id)
    references public.experiments (id, project_id) on delete cascade,
  constraint experiment_variants_artifact_project_fkey foreign key (artifact_id, project_id)
    references public.artifacts (id, project_id) on delete set null (artifact_id),
  constraint experiment_variants_unique_label unique (experiment_id, label),
  constraint experiment_variants_unique_ordinal unique (experiment_id, ordinal),
  constraint experiment_variants_project_identity_unique unique (id, project_id)
);

alter table public.experiments
  add column winner_variant_id uuid,
  add constraint experiments_winner_variant_project_fkey
    foreign key (winner_variant_id, project_id)
    references public.experiment_variants (id, project_id)
    on delete set null (winner_variant_id),
  add constraint experiments_next_not_self_check
    check (next_experiment_id is null or next_experiment_id <> id),
  add constraint experiments_next_experiment_project_fkey
    foreign key (next_experiment_id, project_id)
    references public.experiments (id, project_id)
    on delete set null (next_experiment_id);

create unique index experiment_variants_one_winner_per_experiment_uidx
  on public.experiment_variants(experiment_id)
  where is_winner;

create index experiments_project_status_idx on public.experiments(project_id, status);
create index experiments_created_by_idx on public.experiments(created_by);
create index experiments_signal_id_idx on public.experiments(signal_id) where signal_id is not null;
create index experiments_decision_id_idx on public.experiments(decision_id) where decision_id is not null;
create index experiments_next_experiment_id_idx on public.experiments(next_experiment_id) where next_experiment_id is not null;
create index experiments_created_at_idx on public.experiments(project_id, created_at desc);

create index experiment_variants_experiment_id_idx on public.experiment_variants(experiment_id);
create index experiment_variants_project_id_idx on public.experiment_variants(project_id);
create index experiment_variants_artifact_id_idx on public.experiment_variants(artifact_id) where artifact_id is not null;

alter table public.experiments enable row level security;
alter table public.experiment_variants enable row level security;

revoke all on table public.experiments from anon, authenticated;
revoke all on table public.experiment_variants from anon, authenticated;

drop trigger if exists set_experiments_updated_at on public.experiments;
create trigger set_experiments_updated_at
before update on public.experiments
for each row execute function public.set_updated_at();

drop trigger if exists set_experiment_variants_updated_at on public.experiment_variants;
create trigger set_experiment_variants_updated_at
before update on public.experiment_variants
for each row execute function public.set_updated_at();
