---
plan_id: plan-ea7af589
created: 2026-06-26T09:46:20.489582700+00:00
request: "I have two svg crests I can save somewhere to also test UI locally, tell me how to proceed"
status: approved
---

You’re very close — it’s just a folder name typo.

Streamlit serves static files only from:

- `.streamlit/static/...`  (not `statis`)

### Fix
From repo root (PowerShell):

```powershell
# create correct folder
mkdir -Force .streamlit\static\crests | Out-Null

# move the files from the wrong folder to the correct one
Move-Item -Force .streamlit\statis\crests\* .streamlit\static\crests\
```

### Verify the files are served
Start Streamlit, then open the SVG directly:

```powershell
streamlit run streamlit_app.py
```

Browser:
- `http://localhost:8501/app/static/crests/yourfile.svg`

### Use these in your data
Set `home_crest` / `away_crest` to:

- `/app/static/crests/<filename>.svg`

If you tell me the exact filenames you put there (or paste `dir .streamlit\static\crests`), I’ll give you the exact two URLs to use.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
