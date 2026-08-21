alter table public.decisions
  add constraint decisions_project_identity_unique unique (id, project_id);

create table public.artifacts (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  signal_id uuid,
  decision_id uuid,
  created_by uuid not null references public.profiles(id) on delete restrict,
  artifact_type text not null,
  title text,
  storage_ref text,
  content_ref text,
  metadata jsonb not null default '{}'::jsonb,
  status text not null default 'draft' check (status in ('draft','active','archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint artifacts_type_not_blank_check check (char_length(btrim(artifact_type)) between 1 and 80),
  constraint artifacts_signal_project_fkey foreign key (signal_id, project_id)
    references public.signals (id, project_id) on delete set null (signal_id),
  constraint artifacts_decision_project_fkey foreign key (decision_id, project_id)
    references public.decisions (id, project_id) on delete set null (decision_id),
  constraint artifacts_project_identity_unique unique (id, project_id)
);

create table public.provenance_events (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  artifact_id uuid,
  signal_id uuid,
  decision_id uuid,
  actor_id uuid references public.profiles(id) on delete set null,
  stage text not null check (stage in ('source','machine_option','human_decision','result')),
  event_type text not null,
  source_kind text,
  source_ref text,
  payload jsonb not null default '{}'::jsonb,
  previous_event_id uuid references public.provenance_events(id) on delete set null,
  created_at timestamptz not null default now(),
  constraint provenance_event_type_not_blank_check check (char_length(btrim(event_type)) between 1 and 120),
  constraint provenance_artifact_project_fkey foreign key (artifact_id, project_id)
    references public.artifacts (id, project_id) on delete set null (artifact_id),
  constraint provenance_signal_project_fkey foreign key (signal_id, project_id)
    references public.signals (id, project_id) on delete set null (signal_id),
  constraint provenance_decision_project_fkey foreign key (decision_id, project_id)
    references public.decisions (id, project_id) on delete set null (decision_id),
  constraint provenance_previous_not_self_check check (previous_event_id is null or previous_event_id <> id)
);

create index artifacts_project_id_idx on public.artifacts(project_id);
create index artifacts_signal_id_idx on public.artifacts(signal_id) where signal_id is not null;
create index artifacts_decision_id_idx on public.artifacts(decision_id) where decision_id is not null;
create index artifacts_created_by_idx on public.artifacts(created_by);
create index artifacts_created_at_idx on public.artifacts(project_id, created_at desc);

create index provenance_project_id_idx on public.provenance_events(project_id);
create index provenance_artifact_id_idx on public.provenance_events(artifact_id) where artifact_id is not null;
create index provenance_signal_id_idx on public.provenance_events(signal_id) where signal_id is not null;
create index provenance_decision_id_idx on public.provenance_events(decision_id) where decision_id is not null;
create index provenance_actor_id_idx on public.provenance_events(actor_id) where actor_id is not null;
create index provenance_previous_event_id_idx on public.provenance_events(previous_event_id) where previous_event_id is not null;
create index provenance_project_created_at_idx on public.provenance_events(project_id, created_at asc);

alter table public.artifacts enable row level security;
alter table public.provenance_events enable row level security;

revoke all on table public.artifacts from anon, authenticated;
revoke all on table public.provenance_events from anon, authenticated;

drop trigger if exists set_artifacts_updated_at on public.artifacts;
create trigger set_artifacts_updated_at
before update on public.artifacts
for each row execute function public.set_updated_at();
