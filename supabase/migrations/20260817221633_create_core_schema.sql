create extension if not exists pgcrypto;

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  handle text unique,
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.projects (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.profiles(id) on delete cascade,
  name text not null,
  slug text not null,
  description text,
  status text not null default 'active' check (status in ('active','archived','paused')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (owner_id, slug)
);

create table public.signals (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  created_by uuid not null references public.profiles(id) on delete restrict,
  signal_type text not null,
  title text,
  content jsonb not null default '{}'::jsonb,
  source_ref text,
  status text not null default 'draft' check (status in ('draft','active','archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.decisions (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  signal_id uuid references public.signals(id) on delete set null,
  decided_by uuid not null references public.profiles(id) on delete restrict,
  decision text not null,
  rationale text,
  outcome jsonb not null default '{}'::jsonb,
  status text not null default 'pending' check (status in ('pending','approved','rejected','superseded')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index projects_owner_id_idx on public.projects(owner_id);
create index signals_project_id_idx on public.signals(project_id);
create index signals_created_by_idx on public.signals(created_by);
create index decisions_project_id_idx on public.decisions(project_id);
create index decisions_signal_id_idx on public.decisions(signal_id);
create index decisions_decided_by_idx on public.decisions(decided_by);

alter table public.profiles enable row level security;
alter table public.projects enable row level security;
alter table public.signals enable row level security;
alter table public.decisions enable row level security;

revoke all on table public.profiles from anon, authenticated;
revoke all on table public.projects from anon, authenticated;
revoke all on table public.signals from anon, authenticated;
revoke all on table public.decisions from anon, authenticated;
