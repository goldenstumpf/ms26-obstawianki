---
plan_id: plan-1dbc0fd1
created: 2026-06-25T15:28:27.284190100+00:00
request: "(.venv) PS C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki> streamlit run streamlit_app.py
2026-06-25 16:42:41.306 Uvicorn server started on 0.0.0.0:8501

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.66:8501

2026-06-25 16:43:10.568 Uncaught app execution
Traceback (most recent call last):
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 101, in map_httpcore_exceptions
    yield
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 250, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection_pool.py\", line 256, in handle_request
    raise exc from None
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection_pool.py\", line 236, in handle_request
    response = connection.handle_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection.py\", line 101, in handle_request
    raise exc
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection.py\", line 78, in handle_request
    stream = self._connect(request)
             ^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection.py\", line 156, in _connect
    stream = stream.start_tls(**kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_backends\sync.py\", line 154, in start_tls
    with map_exceptions(exc_map):
         ^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\AppData\Local\Programs\Python\Python312\Lib\contextlib.py\", line 158, in __exit__
    self.gen.throw(value)
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_exceptions.py\", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\streamlit\runtime\scriptrunner\exec_code.py\", line 129, in exec_func_with_error_handling
    result = func()
             ^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py\", line 789, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\streamlit_app.py\", line 17, in <module>
    run()
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\main.py\", line 20, in run
    render_login()
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\tabs\login.py\", line 14, in render_login
    if authenticate_user(nick, pin):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\data\users.py\", line 41, in authenticate_user
    stored = get_user_pin(username)
             ^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\data\users.py\", line 25, in get_user_pin
    .execute()
     ^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\postgrest\_sync\request_builder.py\", line 90, in execute
    r = send_with_retry(self.request)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\postgrest\_sync\request_builder.py\", line 51, in send_with_retry
    resp = req.send(headers)
           ^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\postgrest\base_request_builder.py\", line 90, in send
    return self.session.request(
           ^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 825, in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 914, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 1014, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 249, in handle_request
    with map_httpcore_exceptions():
         ^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\AppData\Local\Programs\Python\Python312\Lib\contextlib.py\", line 158, in __exit__
    self.gen.throw(value)
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 118, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)
2026-06-25 16:43:23.272 Uncaught app execution
Traceback (most recent call last):
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 101, in map_httpcore_exceptions
    yield
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 250, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection_pool.py\", line 256, in handle_request
    raise exc from None
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection_pool.py\", line 236, in handle_request
    response = connection.handle_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection.py\", line 101, in handle_request
    raise exc
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection.py\", line 78, in handle_request
    stream = self._connect(request)
             ^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_sync\connection.py\", line 156, in _connect
    stream = stream.start_tls(**kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_backends\sync.py\", line 154, in start_tls
    with map_exceptions(exc_map):
         ^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\AppData\Local\Programs\Python\Python312\Lib\contextlib.py\", line 158, in __exit__
    self.gen.throw(value)
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpcore\_exceptions.py\", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\streamlit\runtime\scriptrunner\exec_code.py\", line 129, in exec_func_with_error_handling
    result = func()
             ^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py\", line 789, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\streamlit_app.py\", line 17, in <module>
    run()
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\main.py\", line 20, in run
    render_login()
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\tabs\login.py\", line 14, in render_login
    if authenticate_user(nick, pin):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\data\users.py\", line 41, in authenticate_user
    stored = get_user_pin(username)
             ^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\data\users.py\", line 25, in get_user_pin
    .execute()
     ^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\postgrest\_sync\request_builder.py\", line 90, in execute
    r = send_with_retry(self.request)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\postgrest\_sync\request_builder.py\", line 51, in send_with_retry
    resp = req.send(headers)
           ^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\postgrest\base_request_builder.py\", line 90, in send
    return self.session.request(
           ^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 825, in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 914, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_client.py\", line 1014, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 249, in handle_request
    with map_httpcore_exceptions():
         ^^^^^^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\AppData\Local\Programs\Python\Python312\Lib\contextlib.py\", line 158, in __exit__
    self.gen.throw(value)
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\.venv\Lib\site-packages\httpx\_transports\default.py\", line 118, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)
  Stopping..."
status: approved
---

Yep — on a corporate laptop that SSL error is extremely common (TLS interception / custom root CA). The **cleanest dev UX** is to bring back a **DEMO_MODE** so Streamlit can run without touching Supabase.

I’ll propose a plan that brings DEMO_MODE back **without re-introducing import/path hacks**, and keeps production behavior unchanged.

## Task plan: Reintroduce DEMO_MODE (safe, minimal, toggleable)

### Step 1 — Inventory where Supabase is called during UI startup/login
**What it accomplishes:** ensure demo mode prevents *all* network calls that currently crash (starting from login).
**Resources:** `app/tabs/login.py`, `app/data/users.py`, `app/data/matches.py`, `app/data/bets.py`, any services called at app start.
**Expected outcome:** a clear list of functions that must have a demo branch.

### Step 2 — Recreate demo toggle + fixtures modules (small, stable data)
**What it accomplishes:** restores the previously working “local fixtures instead of Supabase”.
**Resources:** create:
- `app/data/demo.py` with `demo_mode_enabled()` reading `DEMO_MODE` env var
- `app/data/fixtures.py` with `demo_users()`, `demo_matches()`, `demo_bets()`
**Expected outcome:** the modules exist and are importable.

### Step 3 — Add demo branches back into DAL (only in app/data/*)
**What it accomplishes:** centralizes the demo logic so UI code doesn’t care; it just uses DAL.
**Resources:** edit
- `app/data/users.py` → `get_user_pin()`, `list_users()`
- `app/data/matches.py` → `list_matches()`, `list_live_matches()`, `get_next_match()`
- `app/data/bets.py` → `list_bets()`, `list_active_bets()`, `upsert_bets_for_user()` (simulate writes)
**Expected outcome:** when `DEMO_MODE=1`, **no Supabase client is called**, so no SSL crash.

### Step 4 — Restore docs + developer workflow
**What it accomplishes:** makes it obvious how to run locally on corporate machines.
**Resources:** `README.md`, `app/data/__init__.py`
**Expected outcome:** README includes DEMO_MODE instructions again (PowerShell example).

### Step 5 — Verification (must prove it works)
**What it accomplishes:** ensure demo mode truly avoids network + app starts.
**Checks:**
- `DEMO_MODE=1 streamlit run streamlit_app.py` starts and you can log in using fixture users (e.g., `alice/1111`).
- `grep` confirms demo imports exist only where expected (DAL + fixtures).
- `python -c "import streamlit_app"` and `python -c "import app.worker.worker"` still import.

### Step 6 — Optional hardening (recommended)
**What it accomplishes:** prevent accidental demo mode in production.
- Ensure demo mode is **opt-in** only (`DEMO_MODE=1`).
- Add a warning banner in Streamlit when demo mode is active.

---

If you confirm, I’ll execute this plan and you’ll be able to run:

```powershell
$env:DEMO_MODE="1"
streamlit run streamlit_app.py
```

…and work on UI without fighting corporate SSL.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
