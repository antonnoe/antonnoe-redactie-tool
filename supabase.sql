-- Redactie-tool — centrale opslag van opmerkingen (optioneel).
-- Eenmalig uitvoeren in de Supabase SQL-editor van het project naar keuze.
-- Zonder deze stap werkt de tool ook: opmerkingen blijven dan lokaal (localStorage)
-- en worden per e-mail/tekstbestand verstuurd.

create table if not exists public.redactie_opmerkingen (
  id uuid primary key default gen_random_uuid(),
  dossier text not null,          -- project_sleutel uit config.json
  blok text not null,             -- stabiele blok-id (sectie::index)
  rol text,                       -- auteur | redactie | eindredacteur | beeldredactie
  type text,                      -- tekst | beeld  (beeldbytes gaan via de export, niet hierheen)
  hoofdstuk text,
  fragment text,
  opmerking text not null,
  created_at timestamptz not null default now()
);

alter table public.redactie_opmerkingen enable row level security;

-- De reviewer heeft alleen de publieke anon-sleutel en mag UITSLUITEND toevoegen.
-- Lezen/wijzigen/verwijderen kan alleen via het Supabase-dashboard of de service-rol.
create policy "anon mag opmerkingen toevoegen" on public.redactie_opmerkingen
  for insert to anon with check (true);
-- bewust GEEN select/update/delete-policy voor anon (privacy: append-only)
