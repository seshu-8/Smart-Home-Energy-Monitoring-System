# 🚀 GitHub Upload Guide
## Smart Home Energy Monitoring System

> A step-by-step guide to upload your project to GitHub professionally —
> from zero (no Git knowledge) to a polished, placement-ready repository.

---

## 📋 Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [One-Time Git Setup](#2-one-time-git-setup)
3. [Create the GitHub Repository](#3-create-the-github-repository)
4. [Prepare Your Project Folder](#4-prepare-your-project-folder)
5. [Initialize Git & First Commit](#5-initialize-git--first-commit)
6. [Connect to GitHub & Push](#6-connect-to-github--push)
7. [Configure Your Repository Page](#7-configure-your-repository-page)
8. [Structured Commit History](#8-structured-commit-history-make-it-look-professional)
9. [Add Screenshots to README](#9-add-screenshots-to-readme)
10. [.gitignore File](#10-gitignore-file)
11. [Ongoing Update Workflow](#11-ongoing-update-workflow)
12. [Repository Checklist](#12-final-repository-checklist)
13. [Common Errors & Fixes](#13-common-errors--fixes)

---

## 1. Prerequisites

### Install Git
- **Windows:** Download from https://git-scm.com/download/win → run installer → keep all defaults
- **Verify install:**
  ```bash
  git --version
  # Expected: git version 2.x.x
  ```

### Create a GitHub Account
- Go to https://github.com → Sign Up
- Use a **professional username** (your real name or close to it)
  - ✅ Good: `seshuu-dev`, `sesh-iotdev`, `seshu-codes`
  - ❌ Avoid: `coolgamer99`, `xXxhacker`, `user123456`

---

## 2. One-Time Git Setup

Run these commands **once** after installing Git. Open Command Prompt or Git Bash:

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your@email.com"
git config --global core.editor "notepad"
git config --global init.defaultBranch main
```

Verify:
```bash
git config --list
```

---

## 3. Create the GitHub Repository

### Step-by-step on GitHub website:

1. Log in to **github.com**
2. Click the **+** icon (top right) → **New repository**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | **Repository name** | `Smart-Home-Energy-Monitoring-System` |
   | **Description** | `IoT-based real-time home energy monitor using ESP32, ACS712 current sensor, and ThingSpeak cloud. Includes Python simulation, interactive dashboard, CSV logging, and PDF reports.` |
   | **Visibility** | ✅ Public (recruiters must be able to see it) |
   | **Initialize this repository** | ❌ Do NOT check (you'll push from local) |
   | **Add .gitignore** | ❌ None (we create our own) |
   | **Choose a license** | MIT License ✅ |

4. Click **Create repository**
5. Copy the URL shown — it looks like:
   ```
   https://github.com/YOUR_USERNAME/Smart-Home-Energy-Monitoring-System.git
   ```

---

## 4. Prepare Your Project Folder

Your local folder should look exactly like this before uploading:

```
Smart-Home-Energy-Monitoring-System/
│
├── arduino_code/
│   └── energy_monitor.ino
│
├── python_simulation/
│   ├── __init__.py
│   ├── sensor_simulator.py
│   ├── energy_calculator.py
│   ├── alert_engine.py
│   ├── data_logger.py
│   ├── report_generator.py
│   └── dashboard_updater.py
│
├── dashboard/
│   └── index.html
│
├── data/
│   └── energy_log.csv
│
├── reports/
│   └── energy_report.pdf
│
├── circuit_diagram/
│   └── wiring_guide.txt
│
├── docs/
│   ├── project_explanation.md
│   └── interview_prep.md
│
├── images/               ← Add your screenshots here
│
├── main.py
├── requirements.txt
├── .gitignore            ← Create this (see Section 10)
└── README.md
```

### Quick folder creation (Windows Command Prompt):
```cmd
cd Desktop
mkdir Smart-Home-Energy-Monitoring-System
cd Smart-Home-Energy-Monitoring-System
mkdir arduino_code python_simulation dashboard data reports circuit_diagram docs images outputs
```

---

## 5. Initialize Git & First Commit

Open Command Prompt **inside your project folder**:

```bash
# Navigate into the project
cd Desktop\Smart-Home-Energy-Monitoring-System

# Initialize Git
git init

# Check what files Git sees
git status

# Stage ALL files
git add .

# Verify what's staged
git status

# Create your first commit
git commit -m "Initial commit: Smart Home Energy Monitoring System — complete IoT project"
```

**Expected output after commit:**
```
[main (root-commit) a1b2c3d] Initial commit: Smart Home Energy Monitoring System
 16 files changed, 1250 insertions(+)
 create mode 100644 README.md
 create mode 100644 main.py
 ...
```

---

## 6. Connect to GitHub & Push

```bash
# Connect your local repo to GitHub (paste YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/Smart-Home-Energy-Monitoring-System.git

# Verify the connection
git remote -v
# Expected:
# origin  https://github.com/YOUR_USERNAME/Smart-Home-Energy-Monitoring-System.git (fetch)
# origin  https://github.com/YOUR_USERNAME/Smart-Home-Energy-Monitoring-System.git (push)

# Push to GitHub
git push -u origin main
```

**You'll be asked for credentials:**
- Username: your GitHub username
- Password: use a **Personal Access Token** (NOT your GitHub password)

### Creating a Personal Access Token (PAT):
1. GitHub → Profile icon → **Settings**
2. Scroll down → **Developer settings** (left sidebar, bottom)
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Note: `Smart-Home-Project-Token`
6. Expiration: 90 days
7. Scopes: check ✅ **repo** (all repo permissions)
8. Click **Generate token**
9. **Copy the token immediately** — you won't see it again
10. Use this token as your "password" when Git asks

---

## 7. Configure Your Repository Page

After pushing, go to your repo page on GitHub and set these up:

### Add Topics (Tags)
1. On repo page → click ⚙️ gear icon next to **About**
2. Add these topics one by one:
   ```
   iot
   esp32
   energy-monitoring
   python
   arduino
   thingspeak
   smart-home
   sensor
   embedded-systems
   matplotlib
   dashboard
   iot-project
   student-project
   ```
3. Click **Save changes**

### Pin to Profile
1. Go to your GitHub **Profile page**
2. Click **Customize your pins**
3. Select `Smart-Home-Energy-Monitoring-System`
4. This makes it appear prominently on your profile

### Add Website Link (optional)
If you deploy the HTML dashboard to GitHub Pages (see below), add the link in the About section.

### Enable GitHub Pages for the Dashboard
1. Repo → **Settings** → **Pages** (left sidebar)
2. Source: **Deploy from a branch**
3. Branch: `main` → folder: `/dashboard`
4. Click **Save**
5. After ~2 minutes, your dashboard is live at:
   `https://YOUR_USERNAME.github.io/Smart-Home-Energy-Monitoring-System/`

---

## 8. Structured Commit History (Make It Look Professional)

A good commit history shows that you built the project thoughtfully, not in one dump. Here's a strategy using separate commits per feature:

```bash
# ── COMMIT 1: Project scaffold ──────────────────────────────
git add README.md requirements.txt .gitignore
git commit -m "docs: add README, requirements, and project structure"

# ── COMMIT 2: Sensor layer ──────────────────────────────────
git add python_simulation/sensor_simulator.py
git commit -m "feat(sensor): add ACS712 + ZMPT101B virtual sensor simulator

- 4 appliance profiles: normal, high, overload, mixed
- Gaussian noise (±2%) mimicking real ADC behavior
- Voltage sag under high load (line impedance model)"

# ── COMMIT 3: Calculation engine ────────────────────────────
git add python_simulation/energy_calculator.py
git commit -m "feat(calc): add energy calculator module

- Real power: P = V × I × PF (PF=0.9)
- Incremental energy accumulation in Wh
- Cost estimation at ₹7/kWh (Hyderabad TSSPDCL rate)
- Daily/monthly projection from average power"

# ── COMMIT 4: Alert system ──────────────────────────────────
git add python_simulation/alert_engine.py
git commit -m "feat(alerts): add threshold-based alert engine

- NORMAL / HIGH / OVERLOAD status levels
- HIGH at >3000W, OVERLOAD at >6000W
- Mirrors ESP32 buzzer + relay behavior"

# ── COMMIT 5: Data logging ──────────────────────────────────
git add python_simulation/data_logger.py
git commit -m "feat(logging): add CSV data logger

- Timestamped append-mode logging
- Auto-creates file with headers on first run
- 8-column schema: timestamp, V, I, P, E, cost, alert"

# ── COMMIT 6: Report generation ─────────────────────────────
git add python_simulation/report_generator.py reports/
git commit -m "feat(report): add PDF report generator with matplotlib charts

- 6-panel dashboard: voltage, current, power bars, energy, pie, summary
- Dark theme (#0f1923 background) for professional look
- Alert-colored bar chart (green/red/amber)"

# ── COMMIT 7: Cloud integration ─────────────────────────────
git add python_simulation/dashboard_updater.py
git commit -m "feat(cloud): add ThingSpeak dashboard updater

- HTTP push to ThingSpeak IoT cloud
- Rate-limited to 15s (free tier compliance)
- Graceful offline fallback"

# ── COMMIT 8: Main orchestrator ─────────────────────────────
git add main.py python_simulation/__init__.py
git commit -m "feat: add main.py simulation orchestrator

- Configurable mode, interval, sample count
- Chains all modules: sensor → calc → alert → log → cloud
- Clean console output with status indicators"

# ── COMMIT 9: HTML dashboard ────────────────────────────────
git add dashboard/
git commit -m "feat(dashboard): add interactive HTML energy dashboard

- Real-time simulation with Chart.js
- 4 modes: normal, high, overload, mixed
- Live KPI cards: V, I, P, E, cost, alert status
- Donut alert distribution + daily/monthly projections"

# ── COMMIT 10: Arduino firmware ─────────────────────────────
git add arduino_code/
git commit -m "feat(hardware): add ESP32 Arduino firmware

- ACS712 RMS current reading (500 samples/cycle)
- ZMPT101B RMS voltage reading
- OLED display with SSD1306
- Buzzer + LED alerts, relay overload protection
- ThingSpeak Wi-Fi upload every 15s"

# ── COMMIT 11: Circuit documentation ────────────────────────
git add circuit_diagram/
git commit -m "docs(hardware): add complete wiring guide and circuit diagram

- Pin-by-pin connection table for all components
- ASCII circuit diagram
- Safety warnings for mains voltage handling"

# ── COMMIT 12: Sample data ──────────────────────────────────
git add data/
git commit -m "data: add sample CSV log from simulation run

- 30 samples, mixed mode
- Demonstrates NORMAL, HIGH, OVERLOAD readings
- Real output from python main.py execution"

# ── COMMIT 13: Documentation ────────────────────────────────
git add docs/
git commit -m "docs: add project explanation and interview preparation

- Full technical + simple explanation
- Industry use cases (smart homes, buildings, factories)
- 10 Q&A covering RMS, ACS712, power factor, MQTT, scaling"

# ── COMMIT 14: Screenshots (after you take them) ─────────────
git add images/
git commit -m "docs: add project screenshots for README

- Terminal output, CSV log, PDF report
- Dashboard in all 4 modes
- GitHub repository preview"
```

### Why this matters
Recruiters and professors who open your GitHub will see 14 meaningful commits spanning different modules. This proves you **built incrementally**, understand software structure, and practice real development habits — not just copy-paste.

---

## 9. Add Screenshots to README

### Screenshots to take:

| Filename | What to capture | How |
|---|---|---|
| `images/01_terminal_output.png` | Run `python main.py` — capture full console | Snipping Tool / Win+Shift+S |
| `images/02_csv_log.png` | Open `data/energy_log.csv` in Excel | Screenshot spreadsheet |
| `images/03_pdf_report.png` | Open `reports/energy_report.pdf` | Screenshot the charts page |
| `images/04_dashboard_normal.png` | Open `dashboard/index.html` → Normal mode | Screenshot browser |
| `images/05_dashboard_high.png` | Click "High Load" button | Screenshot red bars |
| `images/06_dashboard_overload.png` | Click "Overload" button | Screenshot amber alerts |
| `images/07_folder_structure.png` | Open project in VS Code | Screenshot file explorer |
| `images/08_github_repo.png` | Your GitHub repo page | Screenshot after upload |

### Add images to README:
In `README.md`, under a `## Screenshots` section:
```markdown
## Screenshots

### Terminal Output (Simulation Running)
![Terminal Output](images/01_terminal_output.png)

### Energy Dashboard — Normal Mode
![Dashboard Normal](images/04_dashboard_normal.png)

### Energy Dashboard — High Load Alert
![Dashboard High](images/05_dashboard_high.png)

### Auto-Generated PDF Report
![PDF Report](images/03_pdf_report.png)

### CSV Data Log
![CSV Log](images/02_csv_log.png)
```

Then commit:
```bash
git add images/ README.md
git commit -m "docs: add screenshots to README"
git push
```

---

## 10. .gitignore File

Create a file named `.gitignore` in your project root. This tells Git to **ignore** files that shouldn't be uploaded:

```gitignore
# Python bytecode
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python

# Virtual environments
venv/
env/
.env
*.env

# IDE files
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Large/generated files (optional — remove if you want them in repo)
# data/energy_log.csv
# reports/energy_report.pdf

# Jupyter Notebooks checkpoints
.ipynb_checkpoints/

# Logs
*.log

# Secrets — NEVER commit API keys
secrets.py
config_local.py
```

After creating:
```bash
git add .gitignore
git commit -m "chore: add .gitignore"
```

---

## 11. Ongoing Update Workflow

Every time you make changes after the initial upload:

```bash
# 1. Check what changed
git status

# 2. See the actual changes
git diff

# 3. Stage changed files
git add <filename>         # specific file
git add .                  # all changes

# 4. Commit with a clear message
git commit -m "fix: correct power factor calculation in energy_calculator.py"

# 5. Push to GitHub
git push
```

### Commit Message Format (Conventional Commits)
Use this format to look professional:
```
<type>: <short description>

Types:
  feat     → new feature
  fix      → bug fix
  docs     → documentation changes
  refactor → code restructure (no behavior change)
  data     → adding/updating data files
  chore    → maintenance (gitignore, requirements, etc.)
  test     → adding tests
```

Examples:
```
feat: add Telegram bot alert integration
fix: handle zero-current dead-band edge case in sensor_simulator
docs: update README with Wokwi simulation link
refactor: extract appliance profiles to separate JSON config file
```

---

## 12. Final Repository Checklist

Before sharing your repo link with anyone, verify:

**Repository basics:**
- [ ] Repository is **Public**
- [ ] Description is filled in (not empty)
- [ ] Topics/tags added (at least 5)
- [ ] License shown (MIT)

**Code quality:**
- [ ] All Python files have docstrings at the top
- [ ] No hardcoded API keys or passwords in code
- [ ] `requirements.txt` is accurate and complete
- [ ] Code runs without errors: `python main.py`

**Documentation:**
- [ ] `README.md` has all sections (Overview, Setup, Usage, Output)
- [ ] README has at least 3 screenshots
- [ ] Circuit diagram / wiring guide present
- [ ] `docs/` folder has project explanation

**Files:**
- [ ] `data/energy_log.csv` — sample data visible
- [ ] `reports/energy_report.pdf` — report accessible
- [ ] `dashboard/index.html` — dashboard openable in browser
- [ ] `.gitignore` present

**Git history:**
- [ ] At least 5 meaningful commits (not just one "initial commit")
- [ ] Commit messages are descriptive
- [ ] No broken/half-done commits

**Profile visibility:**
- [ ] Repository pinned on your GitHub profile
- [ ] GitHub profile has a bio mentioning IoT / Python / ESP32
- [ ] Profile picture is professional (or at least not an anime avatar)

---

## 13. Common Errors & Fixes

### Error: `fatal: not a git repository`
```bash
# You're not inside the project folder. Navigate first:
cd Desktop\Smart-Home-Energy-Monitoring-System
git init
```

### Error: `remote origin already exists`
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### Error: `failed to push — rejected, non-fast-forward`
```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### Error: Authentication failed / 403
```bash
# GitHub no longer accepts passwords. Use a Personal Access Token.
# Generate one at: GitHub → Settings → Developer settings → PAT
# Use the token as your password when prompted.
```

### Error: `src refspec main does not match any`
```bash
# You haven't committed anything yet. Add files first:
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Large file rejected (>100MB)
```bash
# GitHub rejects files over 100MB.
# Add large files to .gitignore before committing.
echo "large_file.zip" >> .gitignore
git rm --cached large_file.zip
git commit -m "chore: remove large file, add to gitignore"
```

### Accidentally committed API key
```bash
# IMMEDIATELY:
# 1. Revoke the key on ThingSpeak/GitHub settings
# 2. Generate a new key
# 3. Remove from code, add to .gitignore
# 4. Then clean history:
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch config.py' \
  --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```

---

## 🎯 Your Final GitHub Repository URL

After completing all steps, your repository will be live at:

```
https://github.com/YOUR_USERNAME/Smart-Home-Energy-Monitoring-System
```

Share this link in:
- Your resume (Projects section)
- LinkedIn profile (Featured section)
- Job application forms
- College project submissions

---

*Built for the Smart Home Energy Monitoring IoT Course Project*
