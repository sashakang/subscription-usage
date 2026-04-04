# Claude Usage Dashboard

Ever wonder how much of your Claude allowance you've burned through? This dashboard tracks it for you.

Claude's API has rate limits — a 5-hour session window and a 7-day weekly window. This tool polls your usage every 5 minutes and builds a visual dashboard so you can see exactly where you stand, how fast you're burning, and when your limits reset.

![Dashboard](screenshots/dashboard-full.png)

## What You See

- **Usage cards** at the top — how much is left in each window, color-coded (green/yellow/red)
- **Usage plots** — your consumption over time with a diagonal "even pace" reference line
- **Burn rate plots** — how fast you're consuming right now (%/hour) with a horizontal "sustainable pace" line
- **Alerts** — warnings when you're approaching limits

### Usage Plots

| Session (5h) | Weekly (7d) | Sonnet |
|:---:|:---:|:---:|
| ![Session](screenshots/session-5h-window.png) | ![Weekly](screenshots/weekly-7d-window.png) | ![Sonnet](screenshots/sonnet-weekly.png) |

### Burn Rate Plots

| Session | Weekly | Sonnet |
|:---:|:---:|:---:|
| ![Session Burn](screenshots/session-burn-rate-pct-h.png) | ![Weekly Burn](screenshots/weekly-burn-rate-pct-h.png) | ![Sonnet Burn](screenshots/sonnet-burn-rate-pct-h.png) |

## Requirements

- **macOS** (uses launchd for scheduling and Keychain for auth)
- **Claude Code** installed and logged in (the OAuth token is read from your Keychain)
- **Python 3**

## Install

Paste this into Claude Code:

> Install https://github.com/sashakang/claude-usage-dashboard — clone to ~/claude-usage-dashboard, symlink both scripts from scripts/ into ~/.local/bin, install the launchd plist (sed \_\_HOME\_\_ → $HOME, then launchctl load), run claude-usage-build to verify. Make sure ~/.local/bin exists and is in PATH.

### Manual install

```bash
git clone https://github.com/sashakang/claude-usage-dashboard.git
cd claude-usage-dashboard

# Make sure ~/.local/bin exists and is in your PATH
mkdir -p ~/.local/bin

# Symlink scripts
ln -sf "$(pwd)/scripts/claude-usage-log" ~/.local/bin/claude-usage-log
ln -sf "$(pwd)/scripts/claude-usage-build" ~/.local/bin/claude-usage-build

# Install the scheduled job (runs every 5 minutes)
sed "s|__HOME__|$HOME|g" scripts/com.claude-usage.log.plist > ~/Library/LaunchAgents/com.claude-usage.log.plist
launchctl load ~/Library/LaunchAgents/com.claude-usage.log.plist
```

Data is stored in `~/.claude/projects/claude-usage-dashboard/`.

## Usage

**Open the dashboard:**
```bash
open index.html
```

**Or run a local server:**
```bash
python3 serve.py  # http://localhost:8766
```

**Rebuild after editing the template:**
```bash
claude-usage-build
```

## How It Works

A launchd job runs `claude-usage-log` every 5 minutes:
1. Reads your OAuth token from the macOS Keychain
2. Fetches usage from `https://api.anthropic.com/api/oauth/usage`
3. Appends a timestamped record to a JSONL file (with 7-day rotation)
4. Calls `claude-usage-build` which bakes the data into `template.html` and writes `index.html`

The dashboard is a single static HTML file — no backend needed, just open it in a browser.

## Project Structure

| File | Purpose |
|------|---------|
| `template.html` | Dashboard source — edit this |
| `index.html` | Generated (gitignored) |
| `serve.py` | Optional dev server (port 8766) |
| `scripts/claude-usage-log` | Collector: fetch, rotate, append |
| `scripts/claude-usage-build` | Builder: JSONL + template -> HTML |
| `scripts/com.claude-usage.log.plist` | macOS LaunchAgent (5-min schedule) |

## Data Format

Each JSONL record:
```json
{
  "ts": "2026-04-04T16:47:27Z",
  "five_hour": 3.0,
  "five_hour_resets": "2026-04-04T20:00:00Z",
  "seven_day": 13.0,
  "seven_day_resets": "2026-04-09T05:00:00Z",
  "sonnet": 0.0,
  "opus": null,
  "extra_enabled": true
}
```
