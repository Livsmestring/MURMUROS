create or replace function public.set_updated_at()
returns trigger
language plpgsql
security invoker
set search_path = pg_catalog, public
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

revoke all on function public.set_updated_at() from public, anon, authenticated;

drop trigger if exists set_profiles_updated_at on public.profiles;
create trigger set_profiles_updated_at
before update on public.profiles
for each row execute function public.set_updated_at();

drop trigger if exists set_projects_updated_at on public.projects;
create trigger set_projects_updated_at
before update on public.projects
for each row execute function public.set_updated_at();

drop trigger if exists set_signals_updated_at on public.signals;
create trigger set_signals_updated_at
before update on public.signals
for each row execute function public.set_updated_at();

drop trigger if exists set_decisions_updated_at on public.decisions;
create trigger set_decisions_updated_at
before update on public.decisions
for each row execute function public.set_updated_at();

alter table public.profiles
  add constraint profiles_handle_format_check
  check (
    handle is null
    or (
      handle = lower(handle)
      and handle = btrim(handle)
      and char_length(handle) between 3 and 40
      and handle ~ '^[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?$'
    )
  );

create unique index profiles_handle_lower_uidx
  on public.profiles (lower(handle))
  where handle is not null;

alter table public.projects
  add constraint projects_name_not_blank_check
  check (char_length(btrim(name)) between 1 and 120),
  add constraint projects_slug_format_check
  check (
    slug = lower(slug)
    and slug = btrim(slug)
    and char_length(slug) between 1 and 80
    and slug ~ '^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$'
  );

alter table public.signals
  add constraint signals_type_not_blank_check
  check (char_length(btrim(signal_type)) between 1 and 80),
  add constraint signals_project_identity_unique unique (id, project_id);

alter table public.decisions
  add constraint decisions_text_not_blank_check
  check (char_length(btrim(decision)) >= 1);

alter table public.decisions
  drop constraint if exists decisions_signal_id_fkey;

alter table public.decisions
  add constraint decisions_signal_project_fkey
  foreign key (signal_id, project_id)
  references public.signals (id, project_id)
  on delete set null (signal_id);
