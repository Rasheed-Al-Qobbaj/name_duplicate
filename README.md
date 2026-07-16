# Name Duplicate Excel Add-in

## What this project does
This repository contains a local Excel add-in with two AI-powered tools for Arabic names:

1. **Duplicate detection**: finds likely duplicate names in your selected Excel column.
2. **Gender prediction**: predicts `Male`, `Female`, or `Unknown` for selected Arabic first names.

The add-in UI is served from a local web server, and it calls a local Flask backend:
- UI pages: `taskpane.html`, `gender_taskpane.html`
- Backend API: `backend.py`
- Excel add-in manifest: `manifest.xml`

---

## Prerequisites
- Python 3.10+ (recommended)
- Microsoft Excel with Office Add-ins support (Microsoft 365)
- Internet access for first model download

Python packages:
- Install from `requirements.txt`
- For gender prediction, also install `llama-cpp-python` (used by `gender_names.py`)

---

## Run locally
From the repository root:

```bash
cd /home/runner/work/name_duplicate/name_duplicate
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pip install llama-cpp-python
python run_servers.py
```

This starts:
- Flask backend on `http://localhost:5000`
- Static file server on `http://localhost:8000`

Windows convenience script:
- `run_app.bat` (activates `.venv` and runs `run_servers.py`)

---

## Use it inside Excel
1. Start both local servers (`python run_servers.py`).
2. In Excel, open **Insert > Add-ins > My Add-ins > Upload My Add-in**.
3. Upload `/home/runner/work/name_duplicate/name_duplicate/manifest.xml`.
4. Open the custom tab from the manifest (currently branded as **Tamer AI**).
5. Use either button:
   - **Check Duplicates**: select a names column, then analyze.
   - **Predict Gender**: select a names column, predict, then choose destination column and write results.

Notes:
- The manifest points to `http://localhost:8000/...`, so local servers must be running.
- API calls are sent to `http://localhost:5000`.

---

## Remove existing Tamer branding
To fully de-brand the project, update the following:

### 1) Manifest metadata and ribbon labels (`manifest.xml`)
Replace Tamer-specific values such as:
- `<ProviderName>Tamer Institute</ProviderName>`
- `<DisplayName DefaultValue="Tamer AI Tools" />`
- `<bt:String id="TabLabel" DefaultValue="Tamer AI" />`
- Any other label/tooltip text you want renamed

### 2) Task pane UI text and theme (`taskpane.html`, `gender_taskpane.html`)
Change:
- `<title>...Tamer...</title>`
- Logo alt text (`alt="Tamer Logo"`)
- Color variable names/values (`--tamer-red`, `--tamer-red-hover`) if desired

### 3) Branding assets
- Replace `logo.png` with your own logo (keep the same filename or update all references).

### 4) Optional launcher text (`run_app.bat`)
- Update the console message string if you want branding removed there too.

Helpful check:
```bash
grep -Rin "Tamer" /home/runner/work/name_duplicate/name_duplicate
```
