create or replace function public.murmur_benchmark_keyword_search(
  search_text text,
  match_count integer default 5
)
returns table (
  id text,
  domain text,
  title text,
  content text,
  source text,
  version text,
  score real
)
language sql
stable
security invoker
set search_path = ''
as $$
  with lexical_query as (
    -- Natural questions should match any meaningful Norwegian lexeme rather
    -- than requiring every word. Field weights still determine final rank.
    select replace(
      plainto_tsquery('norwegian', search_text)::text,
      ' & ',
      ' | '
    )::tsquery as value
  )
  select
    r.id,
    r.domain,
    r.title,
    r.content,
    r.source,
    r.version,
    ts_rank_cd(r.fts, q.value, 32) as score
  from public.murmur_retrieval_benchmark_records r
  cross join lexical_query q
  where r.status = 'approved'
    and r.fts @@ q.value
  order by score desc, r.id
  limit least(greatest(match_count, 1), 50)
$$;

revoke all on function public.murmur_benchmark_keyword_search(text, integer) from public, anon, authenticated;
grant execute on function public.murmur_benchmark_keyword_search(text, integer) to service_role;
