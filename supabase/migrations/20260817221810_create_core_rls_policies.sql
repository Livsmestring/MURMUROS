grant usage on schema public to authenticated;

grant select, insert, update, delete on table public.profiles to authenticated;
grant select, insert, update, delete on table public.projects to authenticated;
grant select, insert, update, delete on table public.signals to authenticated;
grant select, insert, update, delete on table public.decisions to authenticated;

revoke all on table public.profiles from anon;
revoke all on table public.projects from anon;
revoke all on table public.signals from anon;
revoke all on table public.decisions from anon;

create policy profiles_select_own
on public.profiles
for select
to authenticated
using (id = auth.uid());

create policy profiles_insert_own
on public.profiles
for insert
to authenticated
with check (id = auth.uid());

create policy profiles_update_own
on public.profiles
for update
to authenticated
using (id = auth.uid())
with check (id = auth.uid());

create policy profiles_delete_own
on public.profiles
for delete
to authenticated
using (id = auth.uid());

create policy projects_select_owned
on public.projects
for select
to authenticated
using (owner_id = auth.uid());

create policy projects_insert_owned
on public.projects
for insert
to authenticated
with check (owner_id = auth.uid());

create policy projects_update_owned
on public.projects
for update
to authenticated
using (owner_id = auth.uid())
with check (owner_id = auth.uid());

create policy projects_delete_owned
on public.projects
for delete
to authenticated
using (owner_id = auth.uid());

create policy signals_select_owned_project
on public.signals
for select
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = signals.project_id
      and p.owner_id = auth.uid()
  )
);

create policy signals_insert_owned_project
on public.signals
for insert
to authenticated
with check (
  created_by = auth.uid()
  and exists (
    select 1
    from public.projects p
    where p.id = signals.project_id
      and p.owner_id = auth.uid()
  )
);

create policy signals_update_owned_project
on public.signals
for update
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = signals.project_id
      and p.owner_id = auth.uid()
  )
)
with check (
  created_by = auth.uid()
  and exists (
    select 1
    from public.projects p
    where p.id = signals.project_id
      and p.owner_id = auth.uid()
  )
);

create policy signals_delete_owned_project
on public.signals
for delete
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = signals.project_id
      and p.owner_id = auth.uid()
  )
);

create policy decisions_select_owned_project
on public.decisions
for select
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = decisions.project_id
      and p.owner_id = auth.uid()
  )
);

create policy decisions_insert_owned_project
on public.decisions
for insert
to authenticated
with check (
  decided_by = auth.uid()
  and exists (
    select 1
    from public.projects p
    where p.id = decisions.project_id
      and p.owner_id = auth.uid()
  )
  and (
    signal_id is null
    or exists (
      select 1
      from public.signals s
      where s.id = decisions.signal_id
        and s.project_id = decisions.project_id
    )
  )
);

create policy decisions_update_owned_project
on public.decisions
for update
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = decisions.project_id
      and p.owner_id = auth.uid()
  )
)
with check (
  decided_by = auth.uid()
  and exists (
    select 1
    from public.projects p
    where p.id = decisions.project_id
      and p.owner_id = auth.uid()
  )
  and (
    signal_id is null
    or exists (
      select 1
      from public.signals s
      where s.id = decisions.signal_id
        and s.project_id = decisions.project_id
    )
  )
);

create policy decisions_delete_owned_project
on public.decisions
for delete
to authenticated
using (
  exists (
    select 1
    from public.projects p
    where p.id = decisions.project_id
      and p.owner_id = auth.uid()
  )
);
