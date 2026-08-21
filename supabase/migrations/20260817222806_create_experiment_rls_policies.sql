grant select, insert, update, delete on table public.experiments to authenticated;
grant select, insert, update, delete on table public.experiment_variants to authenticated;

revoke all on table public.experiments from anon;
revoke all on table public.experiment_variants from anon;

create policy experiments_select_owned_project
on public.experiments
for select
to authenticated
using (
  exists (
    select 1 from public.projects p
    where p.id = experiments.project_id
      and p.owner_id = auth.uid()
  )
);

create policy experiments_insert_owned_project
on public.experiments
for insert
to authenticated
with check (
  created_by = auth.uid()
  and exists (
    select 1 from public.projects p
    where p.id = experiments.project_id
      and p.owner_id = auth.uid()
  )
  and (
    signal_id is null or exists (
      select 1 from public.signals s
      where s.id = experiments.signal_id
        and s.project_id = experiments.project_id
    )
  )
  and (
    decision_id is null or exists (
      select 1 from public.decisions d
      where d.id = experiments.decision_id
        and d.project_id = experiments.project_id
    )
  )
  and (
    next_experiment_id is null or exists (
      select 1 from public.experiments e2
      where e2.id = experiments.next_experiment_id
        and e2.project_id = experiments.project_id
    )
  )
  and (
    winner_variant_id is null or exists (
      select 1 from public.experiment_variants v
      where v.id = experiments.winner_variant_id
        and v.project_id = experiments.project_id
        and v.experiment_id = experiments.id
    )
  )
);

create policy experiments_update_owned_project
on public.experiments
for update
to authenticated
using (
  exists (
    select 1 from public.projects p
    where p.id = experiments.project_id
      and p.owner_id = auth.uid()
  )
)
with check (
  created_by = auth.uid()
  and exists (
    select 1 from public.projects p
    where p.id = experiments.project_id
      and p.owner_id = auth.uid()
  )
  and (
    signal_id is null or exists (
      select 1 from public.signals s
      where s.id = experiments.signal_id
        and s.project_id = experiments.project_id
    )
  )
  and (
    decision_id is null or exists (
      select 1 from public.decisions d
      where d.id = experiments.decision_id
        and d.project_id = experiments.project_id
    )
  )
  and (
    next_experiment_id is null or exists (
      select 1 from public.experiments e2
      where e2.id = experiments.next_experiment_id
        and e2.project_id = experiments.project_id
    )
  )
  and (
    winner_variant_id is null or exists (
      select 1 from public.experiment_variants v
      where v.id = experiments.winner_variant_id
        and v.project_id = experiments.project_id
        and v.experiment_id = experiments.id
    )
  )
);

create policy experiments_delete_owned_project
on public.experiments
for delete
to authenticated
using (
  exists (
    select 1 from public.projects p
    where p.id = experiments.project_id
      and p.owner_id = auth.uid()
  )
);

create policy experiment_variants_select_owned_project
on public.experiment_variants
for select
to authenticated
using (
  exists (
    select 1 from public.projects p
    where p.id = experiment_variants.project_id
      and p.owner_id = auth.uid()
  )
);

create policy experiment_variants_insert_owned_project
on public.experiment_variants
for insert
to authenticated
with check (
  created_by = auth.uid()
  and exists (
    select 1 from public.projects p
    where p.id = experiment_variants.project_id
      and p.owner_id = auth.uid()
  )
  and exists (
    select 1 from public.experiments e
    where e.id = experiment_variants.experiment_id
      and e.project_id = experiment_variants.project_id
  )
  and (
    artifact_id is null or exists (
      select 1 from public.artifacts a
      where a.id = experiment_variants.artifact_id
        and a.project_id = experiment_variants.project_id
    )
  )
);

create policy experiment_variants_update_owned_project
on public.experiment_variants
for update
to authenticated
using (
  exists (
    select 1 from public.projects p
    where p.id = experiment_variants.project_id
      and p.owner_id = auth.uid()
  )
)
with check (
  created_by = auth.uid()
  and exists (
    select 1 from public.projects p
    where p.id = experiment_variants.project_id
      and p.owner_id = auth.uid()
  )
  and exists (
    select 1 from public.experiments e
    where e.id = experiment_variants.experiment_id
      and e.project_id = experiment_variants.project_id
  )
  and (
    artifact_id is null or exists (
      select 1 from public.artifacts a
      where a.id = experiment_variants.artifact_id
        and a.project_id = experiment_variants.project_id
    )
  )
);

create policy experiment_variants_delete_owned_project
on public.experiment_variants
for delete
to authenticated
using (
  exists (
    select 1 from public.projects p
    where p.id = experiment_variants.project_id
      and p.owner_id = auth.uid()
  )
);
