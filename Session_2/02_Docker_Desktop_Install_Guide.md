# n8n on Docker Desktop — Student Install Guide

**Session 2 — Environment Setup**
**Estimated time:** 30–40 minutes
**You will need:** Docker Desktop installed, a free ngrok account, this guide.

By the end of this guide you will have your own self-hosted n8n instance running on your laptop, reachable from the internet via a public HTTPS URL (so webhooks work later in the course).

---

## Why this setup?

n8n needs to be reachable from the internet for webhook nodes to work. Running n8n locally inside Docker is fast and free, but `localhost` is not reachable from the outside world. We use **ngrok** to give your local n8n a public HTTPS URL that external services (Telegram, WhatsApp, Google, etc.) can call.

```
Internet  →  ngrok HTTPS URL  →  your laptop  →  Docker container (n8n)
```

---

## Step 0 — Get your own ngrok subdomain (DO THIS FIRST)

1. Go to https://dashboard.ngrok.com and sign up for a free account.
2. Install the ngrok CLI: https://ngrok.com/download
3. From your ngrok dashboard, copy your authtoken and run:
   ```
   ngrok config add-authtoken <YOUR-TOKEN>
   ```
4. In the dashboard, go to **Cloud Edge → Domains** and claim your free static domain. It will look something like `something-random-words.ngrok-free.app`.
5. **Write this domain down.** You will paste it into the env vars below. Every place this guide says `<YOUR-NGROK-SUBDOMAIN>`, replace it with your own domain.

> ⚠️ **Do NOT use the instructor's ngrok domain.** It belongs to the instructor's tunnel and will not work for you. You need your own.

> ⚠️ **Free ngrok URLs without a claimed static domain change every restart.** If you skip step 4, every webhook you set up will break the next time you restart ngrok. Always claim a static domain.

---

## Step 1 — Open Docker Desktop and find the n8n image

1. Open Docker Desktop.
2. Click **Images** in the left sidebar.
3. Click **Search images to run** at the top.
4. Paste `n8nio/n8n` in the search bar and press Enter.
5. The first result should be the official `n8nio/n8n` image. Click **Pull**.
6. Wait for the download to finish (a few hundred MB).

---

## Step 2 — Run the image with the right configuration

1. Once pulled, click **Run** on the `n8nio/n8n` image.
2. A configuration dialog opens. Expand **Optional settings**.
3. Fill in the fields below carefully.

### Container name
```
n8n-demo
```
(any name works, but pick something you'll recognize)

### Ports
| Host port | Container port |
|-----------|----------------|
| `5678`    | `5678`         |

This maps your laptop's port 5678 to the container's port 5678, so you can open n8n at `http://localhost:5678`.

### Volumes
| Host path                                | Container path     |
|------------------------------------------|--------------------|
| Pick a folder, e.g. `~/n8n_data`         | `/home/node/.n8n`  |

This is where n8n stores your workflows, credentials, and database. **Without this volume, everything disappears when the container restarts.**

### Environment variables
Add each of the following. Every variable has a "why" — read them.

| Variable | Value | Why it matters |
|----------|-------|----------------|
| `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE` | `true` | Lets community-built nodes work as AI agent tools. We'll use this in Sessions 10–12. |
| `N8N_EDITOR_BASE_URL` | `https://<YOUR-NGROK-SUBDOMAIN>` | Tells n8n what its public URL is, so the editor builds correct links. |
| `WEBHOOK_URL` | `https://<YOUR-NGROK-SUBDOMAIN>` | The most important one. Webhook nodes generate URLs based on this. Get this wrong and webhooks break. |
| `N8N_HOST` | `<YOUR-NGROK-SUBDOMAIN>` (no `https://`) | The hostname n8n binds to. Note: no protocol prefix. |
| `N8N_PROTOCOL` | `https` | Tells n8n to assume HTTPS (because ngrok terminates SSL for us). |
| `N8N_DEFAULT_BINARY_DATA_MODE` | `filesystem` | Stores file uploads on disk instead of in the database. Required for OCR/image workflows in Session 9. |
| `GENERIC_TIMEZONE` | `Asia/Amman` | **Set this to YOUR timezone.** Controls when Schedule triggers fire. Wrong value = your 9am report runs at 2am. |
| `NODE_FUNCTION_ALLOW_EXTERNAL` | `*` | Lets the Code node import npm packages. We'll use this in Session 6. |

> 🛑 **Replace `<YOUR-NGROK-SUBDOMAIN>` with your actual claimed ngrok domain from Step 0.** Do not leave it as a placeholder. Do not use the instructor's domain.

> 🌍 **Set `GENERIC_TIMEZONE` to YOUR timezone**, not Asia/Amman, unless you're actually in Jordan. Common values: `America/New_York`, `Europe/London`, `Asia/Riyadh`, `Asia/Dubai`, `Africa/Cairo`. Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

4. Click **Run**.

---

## Step 3 — Start the ngrok tunnel

Open a terminal and run (replace with your own domain):

```
ngrok http --url=https://<YOUR-NGROK-SUBDOMAIN> 5678
```

You should see output like:
```
Forwarding   https://your-domain.ngrok-free.app -> http://localhost:5678
```

**Leave this terminal window open.** If you close it, the tunnel dies and your n8n is no longer reachable from the internet.

---

## Step 4 — Open n8n and finish setup

1. In your browser, go to `https://<YOUR-NGROK-SUBDOMAIN>` (your ngrok URL).
2. n8n will show a setup screen. Create your owner account (email + password). **Save these somewhere — you'll need them every time.**
3. You should land in the n8n editor with an empty workspace.

✅ **You're done.** Your n8n is running locally, reachable from the internet, and ready for the smoke test.

---

## Step 5 — Import the smoke-test workflow

Your instructor will share `02_Instance_Smoke_Test.json`. To import it:

1. In n8n, click the **+** in the top-right or open the workflows list.
2. Click the three-dot menu → **Import from File**.
3. Select `02_Instance_Smoke_Test.json`.
4. Click **Execute Workflow** at the bottom.
5. Click each node and check the output panel — you should see your name and a current timestamp.

If the timestamp is in the wrong timezone, your `GENERIC_TIMEZONE` env var is wrong. Stop the container, fix it, and run again.

---

## Troubleshooting

### "Port 5678 is already in use"
You already have an n8n container running (probably from a previous attempt).
- In Docker Desktop → **Containers**, find any running container using port 5678 and stop it.
- Or change your host port to `5679` and access n8n at `http://localhost:5679`.

### Container starts then immediately stops
- Check the container logs (click the container in Docker Desktop → **Logs** tab).
- 95% of the time it's a typo in an environment variable. Common offenders: missing `https://` in `WEBHOOK_URL`, or `https://` accidentally included in `N8N_HOST`.

### "This site can't be reached" when opening the ngrok URL
- Is the ngrok terminal window still open and showing "Forwarding"?
- Is the Docker container still running (green indicator in Docker Desktop)?
- Try `http://localhost:5678` first — if that works, the issue is ngrok.

### Webhooks worked yesterday, broken today
- Your ngrok URL changed. This happens if you skipped Step 0's static domain.
- Either claim a static domain (free) or accept that you must update `WEBHOOK_URL` every time you restart.

### Mac (Apple Silicon) — image won't pull or run
- The `n8nio/n8n` image supports arm64, but make sure Docker Desktop is up to date.
- If it still fails, fall back to **n8n Cloud** for today's class and try again at home.

### Windows — Docker Desktop won't start
- You probably need WSL2 enabled. This takes 15+ minutes to set up and isn't worth doing in class.
- Use **n8n Cloud** for today's class. Install Docker Desktop + WSL2 at home.

---

## What you should have at the end of Session 2

- [ ] A Docker container named `n8n-demo` running locally
- [ ] An ngrok terminal showing your tunnel as "Forwarding"
- [ ] An n8n editor open in your browser at your ngrok URL
- [ ] An owner account created (email + password saved)
- [ ] The smoke-test workflow imported and successfully executed
- [ ] A GitHub account, with at least one workflow JSON pushed to a repo

If any box is unchecked, get help from the instructor before leaving.
