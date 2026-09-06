#!/usr/bin/env python3
"""
OSS Contributions Generator

Fetches every merged PR you have authored, drops the ones to your own repos,
looks up line counts, and prints a single HTML fragment whose formatting matches
the <section id="impact"> + <section id="contributions"> blocks in oss.html.

Nothing is written to disk unless you pass --out; no JSON/markdown side files.
Progress goes to stderr, the HTML fragment goes to stdout, so you can do:

    python3 generate_complete_oss.py > snippet.html
    python3 generate_complete_oss.py --out snippet.html

Then paste the fragment over the two matching <section> blocks in oss.html. The
rest of that page (styles, scripts) is untouched.

Requires the GitHub CLI (`gh`) to be installed and authenticated.

Note on formatting: the template below reproduces Prettier's output for these
blocks. Every real entry wraps the same way (the GitHub URL always pushes the
<a> past the print width), so the fragment should drop in without a reformat. If
you ever run Prettier on the page afterwards and see a one-line diff on some
unusually short entry, that's why.
"""

import argparse
import html
import json
import subprocess
import sys
import time
from collections import defaultdict

USERNAME = "AnarchistHoneybun"  # repos owned by this login are treated as "internal"
MAX_PRS = 1000
RATE_LIMIT_DELAY = 0.5  # seconds between `gh pr view` calls

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:  # pragma: no cover - very old Python
    pass


def log(*args):
    print(*args, file=sys.stderr, flush=True)


def run_gh(cmd, timeout=30):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "command timed out"
    except FileNotFoundError:
        return False, "`gh` not found - install and authenticate the GitHub CLI"
    if result.returncode != 0:
        return False, result.stderr.strip()
    return True, result.stdout


def fetch_merged_prs():
    log("Fetching merged PRs authored by you...")
    ok, out = run_gh([
        "gh", "search", "prs",
        "--author=@me",
        "--merged",
        f"--limit={MAX_PRS}",
        "--json", "title,repository,url,number",
    ])
    if not ok:
        log(f"error: {out}")
        sys.exit(1)
    prs = json.loads(out)
    log(f"  {len(prs)} merged PRs")
    return prs


def external_only(prs):
    owner = USERNAME.lower()
    ext = [pr for pr in prs
           if pr["repository"]["nameWithOwner"].split("/")[0].lower() != owner]
    log(f"  {len(ext)} to external repos ({len(prs) - len(ext)} to your own)")
    return ext


def add_line_counts(prs):
    log(f"Looking up line counts for {len(prs)} PRs...")
    out = []
    for i, pr in enumerate(prs, 1):
        repo = pr["repository"]["nameWithOwner"]
        num = pr["number"]
        ok, raw = run_gh([
            "gh", "pr", "view", str(num),
            "--repo", repo,
            "--json", "additions,deletions",
        ])
        additions = deletions = 0
        if ok:
            try:
                d = json.loads(raw)
                additions = d.get("additions", 0)
                deletions = d.get("deletions", 0)
            except json.JSONDecodeError:
                ok = False
        log(f"  [{i}/{len(prs)}] {repo}#{num} "
            + (f"+{additions} -{deletions}" if ok else "(no diff stats)"))
        out.append({
            "repo": repo,
            "title": pr["title"],
            "url": pr["url"],
            "additions": additions,
            "deletions": deletions,
        })
        time.sleep(RATE_LIMIT_DELAY)
    return out


def order(prs):
    """Group by repo; PRs within a repo by additions desc; repos by their
    biggest single contribution desc. Matches the current page ordering."""
    groups = defaultdict(list)
    for pr in prs:
        groups[pr["repo"]].append(pr)
    for items in groups.values():
        items.sort(key=lambda p: p["additions"], reverse=True)
    ordered_repos = sorted(
        groups.items(),
        key=lambda kv: max(p["additions"] for p in kv[1]),
        reverse=True,
    )
    return [pr for _, items in ordered_repos for pr in items]


LI_TEMPLATE = """\
            <li>
              <strong>{repo}</strong> →
              <a href="{url}"
                >{title}</a
              >
              <span class="line-changes"
                ><span class="additions">+{additions}</span>
                <span class="deletions">-{deletions}</span></span
              >
            </li>"""


def render(prs):
    total_add = sum(p["additions"] for p in prs)
    total_del = sum(p["deletions"] for p in prs)

    impact = (
        '        <section id="impact">\n'
        '          <p class="line-changes">\n'
        f'            <span class="additions"> +{total_add:,}</span>\n'
        f'            <span class="deletions"> -{total_del:,}</span>\n'
        "          </p>\n"
        "        </section>"
    )

    items = "\n".join(
        LI_TEMPLATE.format(
            repo=html.escape(p["repo"], quote=False),
            url=html.escape(p["url"], quote=True),
            title=html.escape(p["title"], quote=False),
            additions=p["additions"],
            deletions=p["deletions"],
        )
        for p in prs
    )

    contributions = (
        '        <section id="contributions">\n'
        "          <ol>\n"
        f"{items}\n"
        "          </ol>\n"
        "        </section>"
    )

    return f"{impact}\n\n{contributions}\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", metavar="PATH",
                    help="write the fragment here instead of stdout")
    args = ap.parse_args()

    prs = add_line_counts(external_only(fetch_merged_prs()))
    if not prs:
        log("no external contributions found")
        sys.exit(1)

    fragment = render(order(prs))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(fragment)
        log(f"wrote {args.out} ({len(prs)} entries)")
    else:
        sys.stdout.write(fragment)
        log(f"done ({len(prs)} entries)")


if __name__ == "__main__":
    main()
