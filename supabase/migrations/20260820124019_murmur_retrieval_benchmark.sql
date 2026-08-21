create extension if not exists vector with schema extensions;

create table if not exists public.murmur_retrieval_benchmark_records (
  id text primary key,
  domain text not null,
  title text not null,
  content text not null,
  status text not null check (status in ('draft', 'approved', 'retired')),
  version text not null,
  source text not null,
  embedding_model text,
  embedding extensions.vector(512),
  fts tsvector generated always as (
    setweight(to_tsvector('norwegian', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('norwegian', coalesce(domain, '')), 'B') ||
    setweight(to_tsvector('norwegian', coalesce(content, '')), 'C') ||
    setweight(to_tsvector('simple', coalesce(id, '')), 'A')
  ) stored,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.murmur_retrieval_benchmark_records enable row level security;

revoke all on table public.murmur_retrieval_benchmark_records from anon, authenticated;
grant select, insert, update, delete on table public.murmur_retrieval_benchmark_records to service_role;

create index if not exists murmur_retrieval_benchmark_fts_idx
  on public.murmur_retrieval_benchmark_records using gin (fts);

-- At 40 records an exact scan is preferable. Add HNSW only after the corpus grows
-- enough to justify approximate search and measure recall before/after.

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
  select
    r.id,
    r.domain,
    r.title,
    r.content,
    r.source,
    r.version,
    ts_rank_cd(r.fts, websearch_to_tsquery('norwegian', search_text)) as score
  from public.murmur_retrieval_benchmark_records r
  where r.status = 'approved'
    and r.fts @@ websearch_to_tsquery('norwegian', search_text)
  order by score desc, r.id
  limit least(greatest(match_count, 1), 50)
$$;

create or replace function public.murmur_benchmark_vector_search(
  query_embedding extensions.vector(512),
  match_count integer default 5
)
returns table (
  id text,
  domain text,
  title text,
  content text,
  source text,
  version text,
  score double precision
)
language sql
stable
security invoker
set search_path = ''
as $$
  select
    r.id,
    r.domain,
    r.title,
    r.content,
    r.source,
    r.version,
    1 - (r.embedding OPERATOR(extensions.<=>) query_embedding) as score
  from public.murmur_retrieval_benchmark_records r
  where r.status = 'approved'
    and r.embedding is not null
  order by r.embedding OPERATOR(extensions.<=>) query_embedding, r.id
  limit least(greatest(match_count, 1), 50)
$$;

revoke all on function public.murmur_benchmark_keyword_search(text, integer) from public, anon, authenticated;
revoke all on function public.murmur_benchmark_vector_search(extensions.vector, integer) from public, anon, authenticated;
grant execute on function public.murmur_benchmark_keyword_search(text, integer) to service_role;
grant execute on function public.murmur_benchmark_vector_search(extensions.vector, integer) to service_role;

comment on table public.murmur_retrieval_benchmark_records is
  'Isolated MurMur retrieval benchmark corpus; not a production knowledge source.';
