---
plan_id: plan-14773b69
created: 2026-06-25T15:37:31.799153100+00:00
request: "(.venv) PS C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki> streamlit run streamlit_app.py
2026-06-25 17:31:57.989 Uvicorn server started on 0.0.0.0:8501
                                 
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.66:8501

2026-06-25 17:32:25.128 Uncaught app execution
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
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\main.py\", line 37, in run
    render_bet_report()
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\tabs\bet_report.py\", line 86, in render_bet_report
    r for r in get_full_bets_info()
               ^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\core\bets.py\", line 90, in get_full_bets_info
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
2026-06-25 17:32:37.068 Uncaught app execution
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
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\main.py\", line 40, in run
    render_bets_table()
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\tabs\table.py\", line 25, in render_table
    records = get_full_bets_info()
              ^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\core\bets.py\", line 90, in get_full_bets_info
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
2026-06-25 17:32:41.871 Uncaught app execution
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
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\main.py\", line 43, in run
    render_live_tab()
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\tabs\live_center.py\", line 105, in render_live_tab
    records = get_full_bets_info()
              ^^^^^^^^^^^^^^^^^^^^
  File \"C:\Users\michal-bazan\OneDrive - MMC\Documents\__OTHER\ms26-obstawianki\app\core\bets.py\", line 90, in get_full_bets_info
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
httpx.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)"
status: approved
---

You *did* get DEMO_MODE back, but the crash now shows a **different code path still calling Supabase directly**:

- The failing call is in **`app/core/bets.py -> get_full_bets_info()`**
- And it’s being used by tabs:
  - `app/tabs/bet_report.py`
  - `app/tabs/table.py`
  - `app/tabs/live_center.py`

So DEMO_MODE currently protects the **new DAL (`app/data/*`)**, but these tabs are still using **legacy core layer (`app/core/*`)** that talks to Supabase unconditionally. That’s why you still see the SSL error.

Also: from your command output, it looks like you **did not set** `DEMO_MODE=1` in that run (you didn’t show it). But even if you do set it, you’d still crash when you open tabs that call `app/core/bets.py`, unless we gate those too.

---

## What needs to happen
We need DEMO_MODE to cover **all** networked Supabase calls used by the UI, including the legacy `app/core/*` functions still referenced by some tabs.

You have two viable approaches:

### Approach A (best architecture): migrate remaining tabs off `app/core/*` to `app/data/*`
- Update `bet_report.py`, `table.py`, `live_center.py` to use DAL functions (or add new DAL functions that provide the same “full bets info” shape they expect).
- Pros: consistent architecture, one place for demo gating.
- Cons: slightly more refactor work.

### Approach B (fastest unblocking): add DEMO_MODE gating inside `app/core/bets.py` (and any other core modules used)
- Wrap Supabase calls with `if demo_mode_enabled(): ...` and return fixture-based equivalents.
- Pros: minimal change to get you unstuck quickly.
- Cons: demo logic now exists in both `core` and `data` (less clean).

Given you want “professionally maintainable”, I’d do **A**, but if you want it working in 10 minutes, **B**.

---

## Quick sanity check (important)
Before we change code, confirm whether you actually ran with DEMO_MODE enabled:

Run this before `streamlit run`:

```powershell
$env:DEMO_MODE="1"
$env:DEMO_MODE
streamlit run streamlit_app.py
```

If it still crashes when you open “Mój raport / Tabela / Centrum - Na żywo”, that confirms the `core/bets.py` path is the blocker (which matches your stacktrace).

---

## Proposed task plan (no execution yet)

### Step 1 — Inventory all UI tabs still using `app/core/*` (legacy Supabase calls)
**Accomplishes:** identifies every remaining “direct Supabase” call that must be demo-safe.  
**Resources:** grep for `from app.core` and `app.core.` imports in `app/tabs/*.py`.

### Step 2 — Focus on the concrete failure: `app/core/bets.py:get_full_bets_info`
**Accomplishes:** understand what data shape it returns so we can provide a demo version.  
**Resources:** read `app/core/bets.py` + the three tabs that call it.

### Step 3A — (Preferred) Replace tab usage to DAL (or add equivalent DAL function)
**Accomplishes:** all UI data access goes through `app/data/*` so DEMO_MODE works globally.  
**Resources:** edit `app/tabs/bet_report.py`, `app/tabs/table.py`, `app/tabs/live_center.py`, and possibly add `app/data/reports.py` (or extend `app/data/bets.py`) to expose “full bets info”.

### Step 3B — (Fast alternative) Gate `app/core/bets.py` with DEMO_MODE
**Accomplishes:** stops SSL crashes without touching tab code.  
**Resources:** edit `app/core/bets.py` to use `demo_mode_enabled()` + fixtures when DEMO_MODE.

### Step 4 — Verification
**Accomplishes:** proves no Supabase network calls happen in demo mode.
- Run:
  - `DEMO_MODE=1 streamlit run streamlit_app.py`
  - Click through all 4 menu items
- Grep for remaining `.execute()` / `get_supabase()` usage reachable from UI in demo mode.

---

If you tell me which approach you want:
- **A (clean refactor)** or **B (fast unblock)**

…I’ll execute it step-by-step and get Streamlit running on the corporate laptop without SSL errors.

---
**Plan ready for review.**
You can discuss or refine this plan, then approve or reject it.
