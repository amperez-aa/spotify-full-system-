# spotify-full-system-
# Spotify Intelligence & Mix Automation - Full Project
This repository automates fetching Spotify playlist data and produces a full DJ-grade intelligence pack:
- deep sync (playlist + audio features + audio analysis)
- waveform generator (PNG waveforms)
- PDF mix blueprint (per-run)
- harmonic intelligence (Camelot mapping)
- clustering and optimal ordering
- beatgrid & suggested cut points
- AI mix timeline builder
- devcontainer for Codespaces
- GitHub Actions CI: scheduled or manual runs
- auto-PR snapshot option
- multi-platform sync stubs (YouTube/Apple placeholders)
- outputs saved to `output/` for easy download

**Important:** This project uses Spotify's Client Credentials flow (Client ID + Client Secret) and works for **public playlists**. You must supply Spotify credentials as GitHub Secrets for automated runs.

---
## Files included (high level)
- `.github/workflows/run_full.yml` — full scheduled workflow
- `scripts/*.py` — pipeline scripts (fetch, features, analysis, clustering, waveforms, PDF, harmonic, timeline)
- `.devcontainer/devcontainer.json` — Codespaces/Dev Container configuration
- `Dockerfile` — (optional dev container)
- `requirements.txt` — Python dependencies for Actions/Codespaces
- `output/` — runtime outputs (not committed; .gitignore present)

---
## Quick install (upload to GitHub + add secrets)
1. Create a new repository on GitHub.
2. Upload or drag-and-drop the extracted project files into the repo root and commit.
3. Go to **Settings → Secrets and variables → Actions** and add:
- `SPOTIFY_CLIENT_ID` — from https://developer.spotify.com/dashboard/
- `SPOTIFY_CLIENT_SECRET` — from the same dashboard
- (optional) `GITHUB_PAT` — Personal Access Token if you want auto-PR creation (repo scope).

4. Run the workflow manually from **Actions → Run workflow** or wait for scheduled runs (every 12 hours by default).

---
## How it works (end-to-end)
1. **GitHub Action** triggers (manual or schedule).
2. Action uses Client ID/Secret to request an OAuth token from Spotify (`accounts.spotify.com/api/token`).
3. The pipeline scripts run in order:
- `fetch_playlist.py` — paginate and save playlist metadata
- `fetch_audio_features.py` — batch-fetch audio-features (tempo, energy, danceability, etc.)
- `fetch_audio_analysis.py` — call audio-analysis endpoint (beats, bars, sections)
- `waveform_generator.py` — generate per-track waveform PNGs (matplotlib + librosa)
- `harmonic_engine.py` — map keys to Camelot, suggest harmonic-safe moves
- `cluster_tracks.py` — KMeans clusters on audio-features
- `optimal_order.py` — heuristic energy-arc ordering
- `beatgrid_and_cuts.py` — suggest cut points using beat times
- `ai_mix_timeline.py` — assemble a mix timeline (start offsets, overlaps)
- `mix_blueprint_pdf.py` — render a PDF blueprint summarizing the mix

4. Action commits outputs into the repo (optionally creates a PR with snapshot).
5. You download artifacts from the repository or open files in Codespaces.

---
## Where to find outputs
After the workflow runs, open your repo and view the `output/` folder. Files produced include:
- `output/playlist_data.json`
- `output/audio_features.json`
- `output/audio_analysis.json`
- `output/waveforms/<track_id>.png`
- `output/clusters.json`
- `output/optimal_order.json`
- `output/cuts.json`
- `output/ai_mix_timeline.json`
- `output/mix_blueprint.pdf`
- `output/harmonic_path.json`

---
## Running locally (optional)
1. Clone repo locally.
2. Create a virtualenv and install requirements:
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
3. Export env vars:
```bash
export SPOTIFY_CLIENT_ID=...
export SPOTIFY_CLIENT_SECRET=...
```
4. Run the pipeline:
```bash
python scripts/fetch_playlist.py
python scripts/fetch_audio_features.py
python scripts/fetch_audio_analysis.py
python scripts/waveform_generator.py
python scripts/harmonic_engine.py
python scripts/cluster_tracks.py
python scripts/optimal_order.py
python scripts/beatgrid_and_cuts.py
python scripts/ai_mix_timeline.py
python scripts/mix_blueprint_pdf.py
```

---
## Notes & Troubleshooting
- Audio analysis requests may fail for some tracks; the script records `error` entries.
- Waveform generation uses `librosa` + `matplotlib` and requires `ffmpeg` for some operations in Action runners; the workflow installs `ffmpeg` via apt.
- The auto-PR feature requires a `GITHUB_TOKEN` by default; for cross-branch PRs you may supply a `GITHUB_PAT` repository secret.
- This system is intended as a production-grade starting point; some heuristics can be tuned to taste.

If you want I can also:
- Push this repo into your GitHub (if you create a repo and give me a temporary collaborator invite)
- Or guide you step-by-step on your device while you upload and run the workflow.
