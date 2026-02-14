-- Drop the function if it exists to ensure clean recreation
drop function if exists match_papers;

-- Re-create the function with CORRECTED syntax
create or replace function match_papers (
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
returns table (
  id text,
  title text,
  abstract text,
  url text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    papers.id,
    papers.title,
    papers.abstract,
    papers.url,
    1 - (papers.embedding <=> query_embedding) as similarity
  from papers
  where 1 - (papers.embedding <=> query_embedding) > match_threshold
  order by papers.embedding <=> query_embedding
  limit match_count;
end;
$$;
