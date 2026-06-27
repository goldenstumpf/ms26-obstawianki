# ms26-obstawianki
Program do zbierania, punktowania i raportowania obstawianek na imprezach sportowych.

## Uruchomienie lokalne

W katalogu repozytorium:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# (Opcjonalnie) dev tooling (lint + tests)
pip install -r requirements-dev.txt

# UI (Streamlit)
streamlit run streamlit_app.py

# Worker (Railway-like)
python -m app.worker.worker
```

## DEMO_MODE (lokalny development bez Supabase)

Na laptopach firmowych (proxy / SSL inspection) połączenia do Supabase mogą się wywalać na:
`SSL: CERTIFICATE_VERIFY_FAILED`.

Wtedy uruchom UI w trybie demo (bez żadnych wywołań do Supabase — dane są czytane/zapisywane lokalnie w `demo_db/` jako JSON):

```powershell
$env:DEMO_MODE = "1"
streamlit run streamlit_app.py
```

Loginy testowe:
- `alice` / `1111`
- `bob` / `2222`
- `charlie` / `3333`

## Wymagane zmienne środowiskowe / sekrety

### Tryb produkcyjny (Supabase)
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `FOOTBALL_API_KEY`

### Tryb DEMO_MODE
- Nie wymaga `SUPABASE_URL` ani `SUPABASE_KEY` (brak połączeń sieciowych do Supabase).
- Nadal możesz potrzebować `FOOTBALL_API_KEY` jeśli w UI/worker uruchamiasz funkcje pobierające mecze z zewnętrznego API.

Lokalnie możesz użyć pliku `.env` (wtedy zainstaluj `python-dotenv`, jest w `requirements.txt`).

## Deploy

### Streamlit Cloud
- **Main file path**: `streamlit_app.py`
- Ustaw sekrety (tryb produkcyjny): `SUPABASE_URL`, `SUPABASE_KEY`, `FOOTBALL_API_KEY`
- (Opcjonalnie) DEMO_MODE: ustaw `DEMO_MODE=1` tylko do testów / bez Supabase.

### Railway (worker)
- Start command: `python -m app.worker.worker`
- Ustaw te same zmienne środowiskowe co wyżej.
- (Opcjonalnie) DEMO_MODE: ustaw `DEMO_MODE=1` jeśli chcesz uruchamiać worker bez Supabase (np. lokalnie).

## Importy / struktura

Kod jest traktowany jako pakiet Python `app`.
W całym repo używamy importów kanonicznych w stylu `from app...`.
Dzięki temu UI i worker działają spójnie niezależnie od katalogu roboczego.
