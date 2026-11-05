#!/usr/bin/env python3
# Copyright (c) 2026 Quentin Bindschaedler. MIT License, see LICENSE.
"""Open the search results for one CAS number on every supplier webshop, one browser tab each.

    python3 cas_search.py 62-53-3                  # all enabled suppliers
    python3 cas_search.py 62533 --purity 99.5      # hyphens optional; purity filter where supported
    python3 cas_search.py 62-53-3 --only sigma,vwr # a subset
    python3 cas_search.py --list                   # show the configured suppliers
    python3 cas_search.py 62-53-3 --dry-run        # print the URLs instead of opening them
    python3 cas_search.py --update-html            # copy suppliers.json into cas_search.html

Suppliers and their URL templates live in suppliers.json next to this script.
The script never contacts the shops itself: it only hands URLs to your browser,
so the tabs use your existing logins and contract prices.
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import webbrowser
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUPPLIERS_FILE = HERE / "suppliers.json"
HTML_FILE = HERE / "cas_search.html"

# Dash look-alikes that come along when a CAS number is copied from a PDF or a web page.
DASHES = str.maketrans(dict.fromkeys("‐‑‒–—―−", "-"))


# CAS number and purity rules: keep in step with the script in cas_search.html.
def normalize_cas(raw):
    """Return the CAS number in canonical form ("62-53-3"), or raise ValueError."""
    text = "".join(raw.split()).translate(DASHES)
    if not re.fullmatch(r"\d+-\d\d-\d|\d+", text, re.ASCII):
        raise ValueError(f"'{raw}' does not look like a CAS number (e.g. 62-53-3 or 62533)")
    digits = text.replace("-", "").lstrip("0")  # some lists zero-pad: 000062-53-3
    if not 5 <= len(digits) <= 10:
        raise ValueError(f"'{raw}' has {len(digits)} digits; a CAS number has 5 to 10")
    body, check = digits[:-1], int(digits[-1])
    expected = sum(i * int(d) for i, d in enumerate(reversed(body), start=1)) % 10
    if check != expected:
        raise ValueError(f"'{raw}' fails the CAS check digit (the last digit should be {expected}); typo?")
    return f"{body[:-2]}-{body[-2:]}-{check}"


def normalize_purity(raw):
    """Return a purity such as "99.5" for inputs like "99,5", "≥99.5 %" or "99.5+%", or raise ValueError."""
    text = re.sub(r"^(≥|>=|>)", "", "".join(raw.split())).rstrip("%").rstrip("+").replace(",", ".")
    if not re.fullmatch(r"\d{1,3}(\.\d+)?", text, re.ASCII) or not 0 < Decimal(text) <= 100:
        raise ValueError(f"purity '{raw}' should be a percentage between 0 and 100, e.g. 99.5")
    return format(Decimal(text).normalize(), "f")


def search_url(supplier, cas, purity):
    """Return (url, filtered): the purity_url when a purity is given and the shop has one, else url."""
    template = supplier.get("purity_url") or ""
    filtered = bool(purity) and "{purity}" in template
    if not filtered:
        template = supplier["url"]
    return template.replace("{cas}", cas).replace("{purity}", purity or ""), filtered


def load_suppliers():
    try:
        return json.loads(SUPPLIERS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: {SUPPLIERS_FILE} not found")
    except json.JSONDecodeError as e:
        sys.exit(f"error: {SUPPLIERS_FILE.name} line {e.lineno}, column {e.colno}: {e.msg}")


def select(suppliers, only):
    """The enabled suppliers, or exactly the --only keys (which may name disabled ones)."""
    if not only:
        return [s for s in suppliers if s.get("enabled", True)]
    by_key = {s["key"].lower(): s for s in suppliers}
    keys = [k.strip().lower() for k in only.split(",") if k.strip()]
    unknown = [k for k in keys if k not in by_key]
    if unknown:
        sys.exit(f"error: unknown supplier key {', '.join(unknown)} (known: {', '.join(by_key)})")
    return [by_key[k] for k in keys]


def windows_powershell():
    """powershell.exe when running under WSL (and BROWSER is unset), else None.

    Under WSL, Python's webbrowser only sees Linux handlers (with WSLg: gio, which has no
    browser behind it), so it reports success while no tab appears. PowerShell's Start-Process
    hands a URL to the Windows default browser, where your logins are. (explorer.exe, used
    before, did not open the URLs that contain '?'.) Setting BROWSER skips this.
    """
    if "BROWSER" in os.environ or "microsoft" not in platform.uname().release.lower():
        return None
    return shutil.which("powershell.exe") or "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"


def open_tabs(urls):
    """Open each URL in a new browser tab; False if no browser could be started."""
    powershell = windows_powershell()
    if not powershell:
        return all(webbrowser.open_new_tab(url) for url in urls)
    # One PowerShell call for all tabs; inside single quotes '&' and '?' stay literal.
    script = "; ".join("Start-Process '%s'" % url.replace("'", "''") for url in urls)
    try:
        subprocess.run([powershell, "-NoProfile", "-NonInteractive", "-Command", script], check=True)
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


def update_html(suppliers):
    """Copy the supplier list into the <script id="suppliers"> block of cas_search.html."""
    page = HTML_FILE.read_text(encoding="utf-8")
    block = re.compile(r'(<script type="application/json" id="suppliers">).*?(</script>)', re.S)
    if not block.search(page):
        sys.exit(f"error: no supplier block found in {HTML_FILE.name}")
    data = json.dumps(suppliers, indent=2, ensure_ascii=False).replace("</", "<\\/")
    HTML_FILE.write_text(block.sub(lambda m: f"{m[1]}\n{data}\n{m[2]}", page, count=1), encoding="utf-8")
    print(f"Copied {len(suppliers)} suppliers into {HTML_FILE.name}")
    import build_de  # the German page is made from the English one
    missing = build_de.build()
    print("Rebuilt cas_search_de.html" + (f"; English text not found: {missing}" if missing else ""))


def main():
    parser = argparse.ArgumentParser(description="Open a CAS number search on every supplier webshop.")
    parser.add_argument("cas", nargs="?", help="CAS number, with or without hyphens (e.g. 62-53-3)")
    parser.add_argument("--purity", help="purity in %%, e.g. 99.5; filters where the shop supports it")
    parser.add_argument("--only", metavar="KEYS", help="comma-separated supplier keys, e.g. sigma,vwr")
    parser.add_argument("--list", action="store_true", help="show the configured suppliers and exit")
    parser.add_argument("--dry-run", action="store_true", help="print the URLs instead of opening them")
    parser.add_argument("--update-html", action="store_true", help="copy suppliers.json into the web pages (English and German)")
    args = parser.parse_args()

    suppliers = load_suppliers()
    if args.update_html:
        update_html(suppliers)
        return
    if args.list:
        for s in suppliers:
            state = "on " if s.get("enabled", True) else "off"
            purity = "  (purity filter)" if s.get("purity_url") else ""
            terms = f"  [{s['terms']}]" if s.get("terms") else ""
            print(f"{s['key']:<8} {state}  {s['name']}{purity}{terms}\n{'':14}{s['url']}")
        return
    if not args.cas:
        parser.error("give a CAS number (or --list)")

    try:
        cas = normalize_cas(args.cas)
        purity = normalize_purity(args.purity) if args.purity else None
    except ValueError as e:
        sys.exit(f"error: {e}")

    targets, unfiltered, no_search, form_only = [], [], [], []
    for s in select(suppliers, args.only):
        if s.get("post"):  # searches only through a form POST, which a plain URL can't do
            form_only.append(s["name"])
            continue
        if "{cas}" not in s["url"]:
            no_search.append(s["name"])
            continue
        url, filtered = search_url(s, cas, purity)
        targets.append((s, url))
        if purity and not filtered:
            unfiltered.append(s["name"])
    if no_search:
        print(f"no CAS search URL yet for {', '.join(no_search)}: skipped", file=sys.stderr)
    if form_only:
        print(f"{', '.join(form_only)}: search only works from cas_search.html (form submission); skipped", file=sys.stderr)
    if not targets:
        sys.exit("error: no supplier left to open")
    if unfiltered:
        print(f"no purity filter at {', '.join(unfiltered)}: opening their plain CAS search", file=sys.stderr)

    if args.dry_run:
        for s, url in targets:
            print(f"{s['key']:<8} {url}")
        return

    label = f"{cas} ({purity} %)" if purity else cas
    print(f"Opening {label} at: {', '.join(s['name'] for s, _ in targets)}")
    if not open_tabs([url for _, url in targets]):
        sys.exit("error: could not start a browser; see 'Command line' in README.md")


if __name__ == "__main__":
    main()
