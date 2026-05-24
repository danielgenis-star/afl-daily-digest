# AFL Daily Digest — Setup Guide
### Fully Autonomous Cloud Version (Mac does NOT need to be on)

---

## What This Does

Every morning at **7:30 AM AEST**, GitHub's free cloud servers will:
1. Fetch AFL news from 8 public RSS feeds
2. Use Claude AI to write your personalised digest
3. Email it to danielgenisd@gmail.com automatically

**No Mac needed. No Claude app needed. Runs forever.**

---

## What You Need

| Item | Cost | Where to get it |
|------|------|-----------------|
| GitHub account | Free | github.com |
| Anthropic API key | ~$1/year in usage | console.anthropic.com |
| Resend API key | Already have it | — |

---

## Step-by-Step Setup

---

### STEP 1 — Create a free GitHub account
*(Skip if you already have one)*

1. Go to **https://github.com/signup**
2. Enter your email, a password, and a username
3. Verify your email address

---

### STEP 2 — Create a new repository

1. Log in to GitHub
2. Click the **+** button in the top-right corner → **New repository**
3. Fill in:
   - **Repository name:** `afl-daily-digest`
   - **Visibility:** Public *(required for free Actions minutes)*
   - Leave everything else as default
4. Click **Create repository**

---

### STEP 3 — Upload the script files

You need to upload **3 files** into the repository.

**File 1 — `afl_digest.py`**
(this is the main script — already created for you)

1. In your new repository, click **Add file → Upload files**
2. Drag and drop `afl_digest.py` from your computer
3. Click **Commit changes**

**File 2 — the GitHub Actions workflow**

This file MUST go in a specific folder. Here's how:

1. In your repository, click **Add file → Create new file**
2. In the filename box, type exactly:
   ```
   .github/workflows/daily-afl-digest.yml
   ```
   *(GitHub will automatically create the folders as you type the slashes)*
3. Open the file `daily-afl-digest.yml` that was created for you, copy its entire contents, and paste it into the editor
4. Click **Commit changes**

---

### STEP 4 — Get an Anthropic API key

This is what gives the digest its AI-powered intelligence. Cost: about $1 per year.

1. Go to **https://console.anthropic.com**
2. Sign up for an account (or log in)
3. Go to **Settings → Billing** and add a credit card
4. Add **$5 credit** — this will last approximately 4–5 years at current usage
5. Go to **API Keys** → click **Create Key**
6. Give it a name like `afl-digest`
7. **Copy the key immediately** — you won't be able to see it again
   - It looks like: `sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx`

---

### STEP 5 — Add your secrets to GitHub

Secrets are encrypted — GitHub never shows them to anyone.

1. Go to your `afl-daily-digest` repository on GitHub
2. Click **Settings** (top menu) → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these two secrets:

   | Secret name | Value |
   |-------------|-------|
   | `ANTHROPIC_API_KEY` | The key you copied in Step 4 |
   | `RESEND_API_KEY` | `re_CtvY6bm2_DuDNehdQ8h3eqwyXMuzVFAWo` |

4. Click **Add secret** after each one

---

### STEP 6 — Test it manually

Before waiting until tomorrow morning, test that everything works right now:

1. In your repository, click the **Actions** tab
2. Click **AFL Daily Digest** in the left sidebar
3. Click the **Run workflow** button (top right) → **Run workflow**
4. Wait about 60–90 seconds
5. Click on the running job to watch the logs
6. If it shows a green tick ✅, check your email inbox — the digest should arrive within a minute

---

### STEP 7 — You're done!

From now on, at 7:30 AM every morning (AEST), the digest will arrive automatically in your inbox. Your Mac can be off, Claude can be closed — it doesn't matter.

---

## Troubleshooting

**The workflow shows a red ✗**
- Click on it to read the error logs
- Most common cause: the secrets weren't added correctly in Step 5
- Check that the secret names are exactly `ANTHROPIC_API_KEY` and `RESEND_API_KEY` (case-sensitive)

**Email isn't arriving**
- Check your spam/junk folder
- Verify the Resend API key is correct in GitHub Secrets

**"No news fetched" error**
- Rare — means all RSS feeds were temporarily down
- It will work again the next day automatically

---

## How to Stop It

If you ever want to stop the digest:
- Go to your repository → **Actions** → **AFL Daily Digest** → click the **...** menu → **Disable workflow**

---

## Summary of Files

| File | Where it goes | What it does |
|------|--------------|--------------|
| `afl_digest.py` | Root of repository | Main script |
| `.github/workflows/daily-afl-digest.yml` | `.github/workflows/` folder | Scheduling |

---

*Setup takes about 15 minutes. After that it runs completely automatically, forever.*
