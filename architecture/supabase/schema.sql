-- Supabase: Auth + Database для ТН ВЭД

create table if not exists public.calc_history (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  code text not null,
  product_text text,
  value numeric,
  weight numeric,
  currency text default 'KZT',
  country text default 'OTHER',
  duty numeric,
  fee numeric,
  vat numeric,
  total numeric,
  measures text,
  created_at timestamptz default now()
);

create table if not exists public.favorites (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  code text not null,
  name text,
  created_at timestamptz default now(),
  unique(user_id, code)
);

alter table public.calc_history enable row level security;
alter table public.favorites enable row level security;

create policy "Users see own history"
  on public.calc_history for all
  using (auth.uid() = user_id);

create policy "Users manage own favorites"
  on public.favorites for all
  using (auth.uid() = user_id);

create index if not exists calc_history_user_idx
  on public.calc_history(user_id, created_at desc);
