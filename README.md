# CAS Supplier Search

Type a CAS number once and open its search at eleven chemical suppliers, each in its own browser
tab, to compare prices: Sigma-Aldrich/Merck, VWR, Fisher Scientific, Thermo Fisher, Th. Geyer, abcr,
ChemPUR, TCI, Santa Cruz Biotechnology, BLD Pharm and Fluorochem (Doug Discovery).
If you are logged in to a shop in that browser, its tab shows your contract prices.
Nothing here contacts the shops or reads their pages: it only opens the shops' own search URLs.
No discounts or shipping terms are included; add your institution's own with the `terms` field.

Three ways to use it, sharing one supplier list (`suppliers.json`):

- `cas_search.html`: a web page for everyone. It needs only a browser: no Python, no installation.
- `cas_search_de.html`: the same page in German.
- `cas_search.py`: the same from a terminal (Python 3, standard library only).

## Web page

Open `cas_search.html`, or the German `cas_search_de.html`, in a browser (double-click it). To give it to colleagues, send them the file
or put it on a shared drive or a web server. It is a single file and works offline.

Type or paste a CAS number (hyphens optional; the check digit is verified), optionally a purity,
untick suppliers you don't need, and press Enter or the button. Every supplier is also listed
below as a link, and each click opens one search.

Browsers let a page open one tab per click and block the others as pop-ups. Allow pop-ups for the
page once, and the button opens all of them:

- Chrome and Edge: click the blocked pop-up icon at the right end of the address bar, choose
  "Always allow pop-ups and redirects", click Done, and press the button again.
- Firefox: in the bar below the address bar, click Settings (or Options), then "Allow pop-ups for …".
- Safari: Safari › Settings › Websites › Pop-up Windows, and set the page to Allow.

If a browser won't remember the choice for a file opened from disk, click the links one by one,
or put the page on a web server. A link ending in `#62-53-3` opens the page with that CAS number filled in.

- **Open as:** tabs in this window, or one window per shop. A page can't put several tabs into a
  new window; only a browser extension could.
- **Close opened searches** closes the tabs or windows the page opened since it was loaded. A shop
  that cuts its link to the page can't be closed this way.
- **Work through a list:** paste a column copied from Excel, or drop an `.xlsx`, `.csv` or `.txt`
  file (old `.xls` isn't supported). Every CAS number in it is picked out and checked; Start and
  Next open the searches for one number after another, closing the previous ones if that box is
  ticked. The list is kept in the browser until you clear the box.

## Purity

A purity such as 99.5 narrows the results to products labelled with it (99.5 %, ≥ 99.5 %, > 99.5 %,
99.5+ %) at shops whose search accepts a purity filter in the URL. That is Fisher Scientific at
the moment; the other shops open their unfiltered CAS search:

- Sigma-Aldrich has a purity filter, but most products carry no purity value, so it would hide offers.
- Th. Geyer's search can't combine a CAS number with a purity term.
- Thermo Fisher and VWR build their result pages with JavaScript, so no purity URL could be checked.

## Command line

    python3 cas_search.py 62-53-3                  # all enabled suppliers
    python3 cas_search.py 62533 --purity 99.5      # hyphens optional; purity filter where supported
    python3 cas_search.py 62-53-3 --only sigma,vwr # a subset, by key
    python3 cas_search.py --list                   # keys, on/off, URL templates
    python3 cas_search.py 62-53-3 --dry-run        # print the URLs instead of opening them

Shortcut: add an alias to `~/.bashrc` (or `~/.zshrc`), then type `cas 62-53-3`:

    echo "alias cas='python3 /path/to/Cas-Supplier-Search/cas_search.py'" >> ~/.bashrc
    source ~/.bashrc

Under WSL the script opens the tabs through Windows PowerShell (`Start-Process`), so they land in
your Windows default browser, where your logins are. Python's `webbrowser` can't reach that browser
from WSL. Elsewhere the script uses `webbrowser`. Setting `BROWSER` (e.g. `export BROWSER=wslview`)
makes it always use `webbrowser` with that command.

## suppliers.json

One entry per shop:

- `name`: shown on the page and in messages
- `key`: short name for `--only`
- `enabled`: `false` leaves the shop unticked on the page and skips it in the script (unless named in `--only`)
- `url`: the search-results URL, with `{cas}` where the CAS number goes (every occurrence is replaced)
- `purity_url` (optional): the same search with a purity filter, with `{purity}` where the number goes
- `terms` (optional): discount and shipping conditions, shown on the page
- `terms_de` (optional): the same in German, for the German page
- `post` (optional): for shops whose search works only as a form submission (ChemPUR), the form
  fields with `{cas}`, e.g. `{"psuche": "{cas}"}`; `url` is then the form's address. Only the web
  page can submit it (not the script, and not the published claude.ai copy)
- `note`: where the URL came from; ignored

After any change, copy the list into the web pages, then share the new files:

    python3 cas_search.py --update-html

This also rebuilds `cas_search_de.html` from `cas_search.html`; the German wording lives in
`build_de.py`. Edit `suppliers.json` and the English page, never the German page or the supplier
block inside the HTML: `--update-html` overwrites both.

### Fixing a URL when a shop changes its site

1. In your browser, search the shop for a known CAS number, e.g. 62-53-3. Use the shop's CAS
   search mode if it has one.
2. Copy the URL of the results page from the address bar.
3. Replace every occurrence of the CAS number in it with `{cas}`. It can appear more than once
   (Sigma has it in the path and in `term=`).
4. Paste it as the `url` value. Keep the double quotes; JSON allows no trailing commas, and the
   script reports the line if the file doesn't parse.
5. Check it with `python3 cas_search.py 62-53-3 --only <key> --dry-run`, then run `--update-html`.

If the results URL doesn't contain the CAS number at all, that shop can't be opened by URL; set
`"enabled": false`. An entry whose `url` has no `{cas}` (such as a shop's homepage) shows on the page
as a plain link, and the open-all button and the script skip it. To make it a real supplier,
replace its `url` with a search URL containing `{cas}`. To add a shop, copy an entry and give it a new key.

### Adding a purity filter for a shop

Search the shop for a CAS number in your browser, apply its purity filter (e.g. 99.5 %), and copy the
URL. Replace the CAS number with `{cas}` and the purity number with `{purity}`, and save it as
`purity_url`. If the shop writes the same purity in several ways (99.5 %, ≥ 99.5 %), the URL may
need each of them; see the Fisher entry.

## License and credit

MIT License (see `LICENSE`), Copyright (c) 2026 Quentin Bindschaedler. You may use, change and share it freely,
as long as the copyright notice stays in the copies. Each page carries the notice too, so a page
copied on its own keeps the credit.
