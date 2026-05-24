#!/usr/bin/env python3
"""
AFL Daily Digest — Fully Autonomous Cloud Version
================================================
Runs via GitHub Actions at 7:30 AM AEST every single day.
Your Mac does NOT need to be on. No Claude app needed.

How it works:
  1. Fetches AFL headlines from multiple public RSS feeds
  2. Sends all headlines to Claude AI (Haiku) to write a rich digest
  3. Emails the digest to danielgenisd@gmail.com via Resend

Cost: ~$0.003 per day in Anthropic API usage (~$1/year)
      Resend free tier covers 100 emails/month (more than enough)

Required environment variables (set as GitHub Secrets):
  ANTHROPIC_API_KEY  — from console.anthropic.com
  RESEND_API_KEY     — re_CtvY6bm2_DuDNehdQ8h3eqwyXMuzVFAWo
"""

import os
import json
import urllib.request
import urllib.error
import sys
import feedparser
from datetime import datetime, timezone, timedelta

# ── Configuration ──────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
RESEND_API_KEY    = os.environ["RESEND_API_KEY"]
TO_EMAIL          = "danielgenisd@gmail.com"
MODEL             = "claude-haiku-4-5-20251001"   # Fast, cheap, great quality

# Public RSS feeds — no login or API key needed
FEEDS = [
    ("AFL Official",        "https://www.afl.com.au/rss/news"),
    ("Melbourne Demons",    "https://www.melbournefc.com.au/rss/news"),
    ("The Guardian AFL",    "https://www.theguardian.com/sport/afl/rss"),
    ("Google – AFL News",   "https://news.google.com/rss/search?q=AFL+news+Australia&hl=en-AU&gl=AU&ceid=AU:en"),
    ("Google – Demons",     "https://news.google.com/rss/search?q=Melbourne+Demons+AFL&hl=en-AU&gl=AU&ceid=AU:en"),
    ("Google – Injuries",   "https://news.google.com/rss/search?q=AFL+injury+update&hl=en-AU&gl=AU&ceid=AU:en"),
    ("Google – Trade",      "https://news.google.com/rss/search?q=AFL+trade+rumour&hl=en-AU&gl=AU&ceid=AU:en"),
    ("Google – Coaches",    "https://news.google.com/rss/search?q=AFL+coach+news&hl=en-AU&gl=AU&ceid=AU:en"),
]
MAX_PER_FEED = 8   # How many headlines to pull from each feed


# ── Step 1: Fetch news ─────────────────────────────────────────────────────────
def fetch_all_news() -> str:
    """Pull headlines from all RSS feeds and return as a plain-text block."""
    lines = []
    for label, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:MAX_PER_FEED]:
                title   = (entry.get("title")   or "").strip()
                summary = (entry.get("summary") or "")[:300].strip()
                if title:
                    lines.append(f"[{label}] {title}. {summary}")
        except Exception as exc:
            print(f"  Warning: could not fetch {label}: {exc}")

    result = "\n".join(lines)
    print(f"  Collected {len(lines)} headlines from {len(FEEDS)} feeds")
    return result


# ── Step 2: Generate digest with Claude AI ─────────────────────────────────────
def call_claude(news_text: str, today: str) -> str:
    """
    Call the Anthropic Messages API directly via urllib (no SDK needed).
    Returns the full HTML email body as a string.
    """
    prompt = f"""You are an AFL news assistant writing a daily email digest for Daniel, a passionate Melbourne Demons supporter.

Today is {today} (AEST).

Below are today's raw AFL news headlines and summaries scraped from public RSS feeds:

{news_text}

Using ONLY the information above (do not invent or guess any facts), write a comprehensive HTML email digest following this EXACT template. Fill in each [FILL] section with real bullet points drawn from the headlines. If there is genuinely no news for a section, write <li>Nothing to report today.</li>

<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:680px;margin:auto;color:#222;line-height:1.6;">
<div style="background:#cc0000;padding:20px;border-radius:6px 6px 0 0;">
  <h1 style="color:white;margin:0;font-size:22px;">&#127945; AFL Daily Digest</h1>
  <p style="color:#ffcccc;margin:4px 0 0 0;font-size:14px;">{today}</p>
</div>
<div style="background:#f9f9f9;padding:20px;border-radius:0 0 6px 6px;">
  <p>G'day Daniel,</p>

  <h2 style="color:#cc0000;border-bottom:2px solid #cc0000;padding-bottom:4px;">&#128308; Melbourne Demons &#8212; Latest News</h2>
  <ul>[FILL: 3-5 bullet points — Demons form, results, off-field news, each 1-2 sentences]</ul>

  <h2 style="color:#cc0000;border-bottom:2px solid #cc0000;padding-bottom:4px;">&#128203; Melbourne Demons &#8212; Player Availability</h2>
  <h4>&#9989; Playing / Selected:</h4>
  <ul>[FILL: players confirmed in squad]</ul>
  <h4>&#10060; Out / Omitted:</h4>
  <ul>[FILL: omitted players with reason if known]</ul>
  <h4>&#129318; Injured:</h4>
  <ul>[FILL: injured players, injury type, return timeline]</ul>
  <h4>&#128260; Returning Soon:</h4>
  <ul>[FILL: players close to returning from injury]</ul>

  <h2 style="color:#003087;border-bottom:2px solid #003087;padding-bottom:4px;">&#127942; AFL Headlines &#8212; Other Teams</h2>
  <ul>[FILL: 4-6 bullet points covering a range of clubs]</ul>

  <h2 style="border-bottom:2px solid #888;padding-bottom:4px;">&#129318; Injuries &amp; Comebacks &#8212; League Wide</h2>
  <ul>[FILL: notable injuries and returns across all clubs]</ul>

  <h2 style="border-bottom:2px solid #888;padding-bottom:4px;">&#128260; Trade &amp; List Management</h2>
  <ul>[FILL: trade rumours, contracts, signings, delistings]</ul>

  <h2 style="border-bottom:2px solid #888;padding-bottom:4px;">&#128084; AFL Administration &amp; Commission</h2>
  <ul>[FILL: CEO, Commission decisions, governance, rule changes]</ul>

  <h2 style="border-bottom:2px solid #888;padding-bottom:4px;">&#9889; Coaches &amp; Controversies</h2>
  <ul>[FILL: coaching news, press conferences, disciplinary matters]</ul>

  <hr style="border:none;border-top:1px solid #ddd;margin:24px 0;">
  <p style="color:#888;font-size:12px;">&#8212; Your AFL Digest &#127945; | Sent automatically at 7:30 AM AEST | Powered by Claude AI + GitHub Actions</p>
</div>
</body>
</html>

Important rules:
- Each bullet point must be 1-2 sentences drawn from the provided headlines
- Do not fabricate player names, scores, or events not mentioned in the headlines
- Return ONLY the HTML — start with <!DOCTYPE html> and end with </html>
"""

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "User-Agent": "AFL-Digest/2.0-autonomous"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        html = result["content"][0]["text"].strip()
        print(f"  Generated {len(html):,} characters of HTML")
        return html


# ── Step 3: Send email via Resend ──────────────────────────────────────────────
def send_email(html_body: str, today: str) -> str:
    """POST to Resend API and return the message ID on success."""
    subject = f"AFL Daily Digest — {today}"

    payload = json.dumps({
        "from": "AFL Digest <onboarding@resend.dev>",
        "to": [TO_EMAIL],
        "subject": subject,
        "html": html_body
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; AFL-Digest/2.0)"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
        msg_id = result.get("id", "unknown")
        print(f"  Email sent — ID: {msg_id}")
        return msg_id


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    # Use AEST (UTC+10) for the date shown in the email
    aest = timezone(timedelta(hours=10))
    today = datetime.now(tz=aest).strftime("%A, %d %B %Y")

    print(f"=== AFL Digest — {today} ===")

    print("\n[1/3] Fetching news from RSS feeds...")
    news_text = fetch_all_news()
    if not news_text.strip():
        print("ERROR: No news fetched. All feeds may be down.")
        sys.exit(1)

    print("\n[2/3] Generating digest with Claude AI...")
    html_body = call_claude(news_text, today)

    print("\n[3/3] Sending email via Resend...")
    send_email(html_body, today)

    print("\n=== SUCCESS — digest sent! ===")


if __name__ == "__main__":
    main()
