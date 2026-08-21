alter table public.experiments
  add constraint experiments_running_requires_started_at_check
  check (status <> 'running' or started_at is not null),
  add constraint experiments_completed_requires_started_at_check
  check (status <> 'completed' or started_at is not null),
  add constraint experiments_completed_requires_completed_at_check
  check (status <> 'completed' or completed_at is not null),
  add constraint experiments_noncompleted_completed_at_check
  check (status = 'completed' or completed_at is null),
  add constraint experiments_winner_requires_completed_check
  check (winner_variant_id is null or status = 'completed'),
  add constraint experiments_learning_requires_completed_check
  check (learning is null or status = 'completed');

create or replace function public.validate_experiment_winner()
returns trigger
language plpgsql
security invoker
set search_path = pg_catalog, public
as $$
declare
  winner_ok boolean;
begin
  if new.winner_variant_id is null then
    return new;
  end if;

  select exists (
    select 1
    from public.experiment_variants v
    where v.id = new.winner_variant_id
      and v.experiment_id = new.id
      and v.project_id = new.project_id
      and v.is_winner = true
  ) into winner_ok;

  if not winner_ok then
    raise exception 'winner_variant_id must reference a winning variant in the same experiment';
  end if;

  return new;
end;
$$;

revoke all on function public.validate_experiment_winner() from public, anon, authenticated;

drop trigger if exists validate_experiment_winner_on_experiments on public.experiments;
create constraint trigger validate_experiment_winner_on_experiments
after insert or update of winner_variant_id, status, project_id
on public.experiments
deferrable initially deferred
for each row execute function public.validate_experiment_winner();

create or replace function public.sync_experiment_winner()
returns trigger
language plpgsql
security invoker
set search_path = pg_catalog, public
as $$
begin
  if tg_op = 'DELETE' then
    return old;
  end if;

  if new.is_winner = true then
    update public.experiment_variants
      set is_winner = false
    where experiment_id = new.experiment_id
      and id <> new.id
      and is_winner = true;
  end if;

  return new;
end;
$$;

revoke all on function public.sync_experiment_winner() from public, anon, authenticated;

drop trigger if exists sync_experiment_winner_on_variants on public.experiment_variants;
create trigger sync_experiment_winner_on_variants
before insert or update of is_winner
on public.experiment_variants
for each row execute function public.sync_experiment_winner();
