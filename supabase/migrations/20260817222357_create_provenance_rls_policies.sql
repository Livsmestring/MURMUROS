grant select, insert, update, delete on table public.artifacts to authenticated;
grant select, insert, update, delete on table public.provenance_events to authenticated;

revoke all on table public.artifacts from anon;
revoke all on table public.provenance_events from anon;

create policy artifacts_select_owned_project
on public.artifacts
for select
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = artifacts.project_id
      and p.owner_id = auth.uid()
  )
);

create policy artifacts_insert_owned_project
on public.artifacts
for insert
to authenticated
with check (
  created_by = auth.uid()
  and exists (
    select 1
    from public.projects p
    where p.id = artifacts.project_id
      and p.owner_id = auth.uid()
  )
  and (
    signal_id is null
    or exists (
      select 1
      from public.signals s
      where s.id = artifacts.signal_id
        and s.project_id = artifacts.project_id
    )
  )
  and (
    decision_id is null
    or exists (
      select 1
      from public.decisions d
      where d.id = artifacts.decision_id
        and d.project_id = artifacts.project_id
    )
  )
);

create policy artifacts_update_owned_project
on public.artifacts
for update
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = artifacts.project_id
      and p.owner_id = auth.uid()
  )
)
with check (
  created_by = auth.uid()
  and exists (
    select 1
    from public.projects p
    where p.id = artifacts.project_id
      and p.owner_id = auth.uid()
  )
  and (
    signal_id is null
    or exists (
      select 1
      from public.signals s
      where s.id = artifacts.signal_id
        and s.project_id = artifacts.project_id
    )
  )
  and (
    decision_id is null
    or exists (
      select 1
      from public.decisions d
      where d.id = artifacts.decision_id
        and d.project_id = artifacts.project_id
    )
  )
);

create policy artifacts_delete_owned_project
on public.artifacts
for delete
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = artifacts.project_id
      and p.owner_id = auth.uid()
  )
);

create policy provenance_select_owned_project
on public.provenance_events
for select
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = provenance_events.project_id
      and p.owner_id = auth.uid()
  )
);

create policy provenance_insert_owned_project
on public.provenance_events
for insert
to authenticated
with check (
  (actor_id is null or actor_id = auth.uid())
  and exists (
    select 1
    from public.projects p
    where p.id = provenance_events.project_id
      and p.owner_id = auth.uid()
  )
  and (
    artifact_id is null
    or exists (
      select 1
      from public.artifacts a
      where a.id = provenance_events.artifact_id
        and a.project_id = provenance_events.project_id
    )
  )
  and (
    signal_id is null
    or exists (
      select 1
      from public.signals s
      where s.id = provenance_events.signal_id
        and s.project_id = provenance_events.project_id
    )
  )
  and (
    decision_id is null
    or exists (
      select 1
      from public.decisions d
      where d.id = provenance_events.decision_id
        and d.project_id = provenance_events.project_id
    )
  )
  and (
    previous_event_id is null
    or exists (
      select 1
      from public.provenance_events pe
      where pe.id = provenance_events.previous_event_id
        and pe.project_id = provenance_events.project_id
    )
  )
);

create policy provenance_update_owned_project
on public.provenance_events
for update
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = provenance_events.project_id
      and p.owner_id = auth.uid()
  )
)
with check (
  (actor_id is null or actor_id = auth.uid())
  and exists (
    select 1
    from public.projects p
    where p.id = provenance_events.project_id
      and p.owner_id = auth.uid()
  )
  and (
    artifact_id is null
    or exists (
      select 1
      from public.artifacts a
      where a.id = provenance_events.artifact_id
        and a.project_id = provenance_events.project_id
    )
  )
  and (
    signal_id is null
    or exists (
      select 1
      from public.signals s
      where s.id = provenance_events.signal_id
        and s.project_id = provenance_events.project_id
    )
  )
  and (
    decision_id is null
    or exists (
      select 1
      from public.decisions d
      where d.id = provenance_events.decision_id
        and d.project_id = provenance_events.project_id
    )
  )
  and (
    previous_event_id is null
    or exists (
      select 1
      from public.provenance_events pe
      where pe.id = provenance_events.previous_event_id
        and pe.project_id = provenance_events.project_id
    )
  )
);

create policy provenance_delete_owned_project
on public.provenance_events
for delete
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = provenance_events.project_id
      and p.owner_id = auth.uid()
  )
);
