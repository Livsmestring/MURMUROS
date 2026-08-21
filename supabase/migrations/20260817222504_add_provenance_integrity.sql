alter table public.provenance_events
  add constraint provenance_project_identity_unique unique (id, project_id);

alter table public.provenance_events
  drop constraint if exists provenance_events_previous_event_id_fkey;

alter table public.provenance_events
  add constraint provenance_previous_event_project_fkey
  foreign key (previous_event_id, project_id)
  references public.provenance_events (id, project_id)
  on delete restrict;

create index provenance_project_stage_created_idx
  on public.provenance_events(project_id, stage, created_at asc);

create or replace function public.prevent_provenance_mutation()
returns trigger
language plpgsql
security invoker
set search_path = pg_catalog, public
as $$
begin
  raise exception 'provenance_events is append-only';
end;
$$;

revoke all on function public.prevent_provenance_mutation() from public, anon, authenticated;

drop trigger if exists prevent_provenance_update on public.provenance_events;
create trigger prevent_provenance_update
before update on public.provenance_events
for each row execute function public.prevent_provenance_mutation();

drop trigger if exists prevent_provenance_delete on public.provenance_events;
create trigger prevent_provenance_delete
before delete on public.provenance_events
for each row execute function public.prevent_provenance_mutation();

revoke update, delete on table public.provenance_events from authenticated;

drop policy if exists provenance_update_owned_project on public.provenance_events;
drop policy if exists provenance_delete_owned_project on public.provenance_events;
