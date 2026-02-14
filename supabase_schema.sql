-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
create table if not exists papers (
  id text primary key,
  title text,
  abstract text,
  url text,
  authors text[],
  categories text[],
  published timestamp,
  embedding vector(384)
);

-- Create a table for user interactions
create table if not exists user_interactions (
  id uuid default gen_random_uuid() primary key,
  user_id text not null,
  paper_id text references papers(id),
  interaction_type text not null, -- 'star', 'ignore', 'click'
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- Create a function to search for documents
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
  return query;
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
