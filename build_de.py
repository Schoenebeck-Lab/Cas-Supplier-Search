#!/usr/bin/env python3
# Copyright (c) 2026 Quentin Bindschaedler. MIT License, see LICENSE.
"""Make the German page cas_search_de.html from cas_search.html by swapping the visible text.

`python3 cas_search.py --update-html` runs this too. Change features in the English page only;
change German wording here. Every English string below must still occur in the English page:
the script names any that no longer do, so you can update this table.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

TEXT = [  # (English, German); longer strings come before shorter ones they contain
    # Page head and intro
    ("<title>CAS Supplier Search</title>", "<title>CAS-Lieferantensuche</title>"),
    ("<h1>CAS Supplier Search</h1>", "<h1>CAS-Lieferantensuche</h1>"),
    ("Type a CAS number to open its search at every supplier at once. If you are logged in to a shop in this browser, its tab shows your contract prices.",
     "CAS-Nummer eingeben und die Suche bei allen Lieferanten auf einmal öffnen. Wer in diesem Browser bei einem Shop angemeldet ist, sieht in dessen Tab die eigenen Vertragspreise."),
    # Form
    ('for="cas">CAS number</label>', 'for="cas">CAS-Nummer</label>'),
    ('for="purity">Purity <span', 'for="purity">Reinheit <span'),
    ('placeholder="99.5"', 'placeholder="99,5"'),
    ('<legend class="label">Suppliers</legend>', '<legend class="label">Lieferanten</legend>'),
    ('<legend class="label">Open as</legend>', '<legend class="label">Öffnen als</legend>'),
    ("> Tabs in this window</label>", "> Tabs in diesem Fenster</label>"),
    ("<p>“Close opened searches” closes what this page opened since it was loaded; a shop that cuts its link to the page can’t be closed this way. “One window per shop” exists because a page can’t put several tabs into a new window.</p>",
     "<p>„Geöffnete Suchen schließen“ schließt, was diese Seite seit dem Laden geöffnet hat; ein Shop, der die Verbindung zur Seite trennt, lässt sich so nicht schließen. „Ein Fenster pro Shop“ gibt es, weil eine Seite nicht mehrere Tabs in ein neues Fenster legen kann.</p>"),
    ("> One window per shop</label>", "> Ein Fenster pro Shop</label>"),
    ("Open all searches", "Alle Suchen öffnen"),
    ('`Close ${n} opened search${n === 1 ? "" : "es"}`', '`${n} geöffnete Suche${n === 1 ? "" : "n"} schließen`'),
    ("Close opened searches", "Geöffnete Suchen schließen"),
    # List card
    ('<h2 id="batch-title">Work through a list</h2>', '<h2 id="batch-title">Liste abarbeiten</h2>'),
    ("Paste a column copied from Excel, or drop an .xlsx, .csv or .txt file on the box. Every CAS number in it is picked out and checked; then step through them one by one.",
     "Eine aus Excel kopierte Spalte einfügen oder eine .xlsx-, .csv- oder .txt-Datei in das Feld ziehen. Alle CAS-Nummern darin werden erkannt und geprüft; danach geht es eine nach der anderen durch."),
    (">Choose a file<", ">Datei auswählen<"),
    ("> Close the previous searches when moving on</label>", "> Vorherige Suchen beim Weitergehen schließen</label>"),
    (">◀ Previous</button>", ">◀ Zurück</button>"),
    ('"Next ▶"', '"Weiter ▶"'),
    # Tracking
    ('<legend class="label">Tracking</legend>', '<legend class="label">Merkliste</legend>'),
    ("> Note the shop I pick for each CAS number</label>", "> Gewählten Shop für jede CAS-Nummer merken</label>"),
    ('<h2 id="picks-title">Picked shops</h2>', '<h2 id="picks-title">Gewählte Shops</h2>'),
    ("Put a chemical in a shop’s cart, then press Pick next to that shop in the searches above. The page closes the searches and, in a list, opens the next CAS number still to pick. When you are done, open all the carts at once. Picks are kept in this browser only.",
     "Eine Chemikalie in den Warenkorb eines Shops legen, dann oben bei diesem Shop auf „Wählen“ drücken. Die Seite schließt die Suchen und öffnet in einer Liste die nächste CAS-Nummer ohne Auswahl. Zum Schluss alle Warenkörbe auf einmal öffnen. Die Auswahl wird nur in diesem Browser gespeichert."),
    ('`Open carts at ${n} shop${n === 1 ? "" : "s"}`', '`Warenkörbe bei ${n} Shop${n === 1 ? "" : "s"} öffnen`'),
    ("Open carts", "Warenkörbe öffnen"),
    (">Copy as table<", ">Als Tabelle kopieren<"),
    ('`Press again to clear ${picks.length} pick${picks.length === 1 ? "" : "s"}`',
     '`Erneut drücken: ${picks.length} Eintr${picks.length === 1 ? "ag" : "äge"} löschen`'),
    ("Clear picks", "Auswahl löschen"),
    ('aria-label="Picks as a table"', 'aria-label="Auswahl als Tabelle"'),
    ('"Picked ✓"', '"Gewählt ✓"'),
    ('"Pick"', '"Wählen"'),
    ("`Pick ${shop.name}`", "`${shop.name} wählen`"),
    ('"Not picked yet"', '"Noch nicht gewählt"'),
    ('"Cart ↗"', '"Warenkorb ↗"'),
    ('"no cart: order from its search"', '"kein Warenkorb: über die Suche bestellen"'),
    ('"Show the searches for this CAS number"', '"Die Suchen für diese CAS-Nummer zeigen"'),
    ('"Nothing picked yet."', '"Noch nichts gewählt."'),
    ('`End of the list; ${left} CAS number${left === 1 ? "" : "s"} not picked yet.`',
     '`Ende der Liste; ${left} CAS-Nummer${left === 1 ? "" : "n"} noch ohne Auswahl.`'),
    ('"Every CAS number in the list is picked. Open the carts when you are ready."',
     '"Für jede CAS-Nummer der Liste ist ein Shop gewählt. Jetzt können die Warenkörbe geöffnet werden."'),
    ('"This browser did not let the page open tabs. Use the Cart links above."',
     '"Dieser Browser lässt die Seite keine Tabs öffnen. Bitte die Warenkorb-Links oben benutzen."'),
    ("`Opened ${count} of ${jobs.length}; the browser blocked the others as pop-ups. Use the Cart links above, or allow pop-ups for this page (see the help below).`",
     "`${count} von ${jobs.length} geöffnet; der Browser hat die übrigen als Pop-ups blockiert. Die Warenkorb-Links oben benutzen oder Pop-ups für diese Seite erlauben (siehe Hilfe unten).`"),
    ('["CAS number", "Shop"]', '["CAS-Nummer", "Lieferant"]'),
    ('"not picked"', '"nicht gewählt"'),
    ('`Copied ${n} row${n === 1 ? "" : "s"} and a header. Paste them into Excel.`',
     '`${n} Zeile${n === 1 ? "" : "n"} und eine Kopfzeile kopiert. In Excel einfügen.`'),
    ('"The browser did not allow copying. The table is selected below: press Ctrl+C."',
     '"Der Browser hat das Kopieren nicht erlaubt. Die Tabelle ist unten markiert: Strg+C drücken."'),
    # Results and help
    ('<h2 id="results-title">Searches</h2>', '<h2 id="results-title">Suchen</h2>'),
    ("<summary>The button opened only one tab?</summary>", "<summary>Der Button hat nur einen Tab geöffnet?</summary>"),
    ("Browsers let a page open one tab per click and block the others as pop-ups. Allow pop-ups for this page once:",
     "Browser lassen eine Seite pro Klick nur einen Tab öffnen und blockieren die übrigen als Pop-ups. Pop-ups für diese Seite einmalig erlauben:"),
    ("<strong>Chrome and Edge:</strong> click the blocked pop-up icon at the right end of the address bar, choose “Always allow pop-ups and redirects”, click Done, then press the button again.",
     "<strong>Chrome und Edge:</strong> rechts in der Adressleiste auf das Symbol für blockierte Pop-ups klicken, „Pop-ups und Weiterleitungen … immer zulassen“ wählen, auf „Fertig“ klicken und den Button erneut drücken."),
    ("<strong>Firefox:</strong> in the bar below the address bar (“Firefox prevented this site from opening … pop-up windows”), click Settings or Options, then “Allow pop-ups for …”.",
     "<strong>Firefox:</strong> in der Leiste unter der Adressleiste („Firefox hat diese Website daran gehindert, … Pop-up-Fenster zu öffnen“) auf „Einstellungen“ klicken, dann „Pop-ups für … erlauben“."),
    ("<strong>Safari:</strong> Safari › Settings › Websites › Pop-up Windows, and set this page to Allow.",
     "<strong>Safari:</strong> Safari › Einstellungen › Websites › Pop-up-Fenster, diese Seite auf „Erlauben“ stellen."),
    ("If your browser doesn’t offer to remember the choice, click the suppliers in the list one by one. Each click opens one search.",
     "Bietet der Browser nicht an, die Wahl zu speichern, die Lieferanten in der Liste nacheinander anklicken. Jeder Klick öffnet eine Suche."),
    ("This page makes no requests of its own. It only opens the suppliers’ search and cart pages in new tabs, in this browser, with your logins. A link ending in #62-53-3 opens it with that CAS number filled in.",
     "Diese Seite stellt selbst keine Anfragen. Sie öffnet nur die Such- und Warenkorbseiten der Lieferanten in neuen Tabs, in diesem Browser, mit Ihren Anmeldungen. Ein Link, der auf #62-53-3 endet, öffnet sie mit dieser CAS-Nummer."),
    # Script messages
    ("/* Page */\n", '/* Page */\ndocument.documentElement.lang = "de";\n'),
    ("“${shown}” does not look like a CAS number (e.g. 62-53-3 or 62533).", "„${shown}“ sieht nicht wie eine CAS-Nummer aus (z. B. 62-53-3 oder 62533)."),
    ("“${shown}” has ${digits.length} digits; a CAS number has 5 to 10.", "„${shown}“ hat ${digits.length} Ziffern; eine CAS-Nummer hat 5 bis 10."),
    ("“${shown}” fails the CAS check digit: the last digit should be ${sum % 10}. Typo?",
     "„${shown}“ hat eine falsche Prüfziffer: Die letzte Ziffer müsste ${sum % 10} sein. Tippfehler?"),
    ("Purity “${raw.trim()}” should be a percentage between 0 and 100, e.g. 99.5.",
     "Reinheit „${raw.trim()}“ muss ein Prozentwert zwischen 0 und 100 sein, z. B. 99,5."),
    ('"The supplier list in this file is broken: "', '"Die Lieferantenliste in dieser Datei ist fehlerhaft: "'),
    ('"Type or paste a CAS number."', '"CAS-Nummer eingeben oder einfügen."'),
    ('"Opened ✓"', '"Geöffnet ✓"'),
    ('let go = "Open ↗";', 'let go = "Öffnen ↗";'),
    ('if (shop.terms) meta.append(el("span", "terms", shop.terms));',
     'if (shop.terms_de || shop.terms) meta.append(el("span", "terms", shop.terms_de || shop.terms));'),
    ('"no CAS search yet"', '"noch keine CAS-Suche"'),
    ('go = "Homepage ↗";', 'go = "Startseite ↗";'),
    ("`${search.purity} % filter`", '`Filter ${search.purity.replace(".", ",")} %`'),
    ('"no purity filter"', '"kein Reinheitsfilter"'),
    ("`${search.cas} · check digit matches`", "`${search.cas} · Prüfziffer stimmt`"),
    ("` · purity ${search.purity} %`", '` · Reinheit ${search.purity.replace(".", ",")} %`'),
    ('" · example: aniline"', '" · Beispiel: Anilin"'),
    ('"No supplier ticked. Tick at least one above."', '"Kein Lieferant ausgewählt. Bitte oben mindestens einen auswählen."'),
    ('`Open ${ready} search${ready === 1 ? "" : "es"}`', '`${ready} Suche${ready === 1 ? "" : "n"} öffnen`'),
    ('`Purity narrows the results at ${filtering.join(", ")} to products labelled with it (99.5 finds 99.5 %, ≥ 99.5 % and 99.5+ %). The other suppliers open unfiltered.`',
     '`Die Reinheit grenzt die Ergebnisse bei ${filtering.join(", ")} auf Produkte mit dieser Angabe ein (99,5 findet 99,5 %, ≥ 99,5 % und 99,5+ %). Die übrigen Lieferanten öffnen ungefiltert.`'),
    ('"None of the suppliers can filter by purity yet."', '"Noch kann kein Lieferant nach Reinheit filtern."'),
    ('"This browser did not let the page open tabs. Click each supplier below; every click opens its search."',
     '"Dieser Browser lässt die Seite keine Tabs öffnen. Bitte die Lieferanten unten einzeln anklicken; jeder Klick öffnet seine Suche."'),
    ("`Opened ${count} of ${targets.length} searches; the browser blocked the others as pop-ups. Click the remaining suppliers below, or allow pop-ups for this page (see the help below the list).`",
     "`${count} von ${targets.length} Suchen geöffnet; der Browser hat die übrigen als Pop-ups blockiert. Die restlichen Lieferanten unten anklicken oder Pop-ups für diese Seite erlauben (siehe Hilfe unter der Liste).`"),
    ('"not a readable .xlsx file"', '"keine lesbare .xlsx-Datei"'),
    ("old .xls files can't be read here; save as .xlsx or .csv, or copy the column and paste it",
     "alte .xls-Dateien können hier nicht gelesen werden; als .xlsx oder .csv speichern oder die Spalte kopieren und einfügen"),
    ("`Could not read ${file.name}: ${e.message}.`", "`${file.name} konnte nicht gelesen werden: ${e.message}.`"),
    ('"No list yet."', '"Noch keine Liste."'),
    ('"No CAS numbers found in this text."', '"Keine CAS-Nummern in diesem Text gefunden."'),
    ('`${batch.length} CAS number${batch.length === 1 ? "" : "s"}`', '`${batch.length} CAS-Nummer${batch.length === 1 ? "" : "n"}`'),
    (" · ${invalid.length} failing the check digit, skipped: ", " · ${invalid.length} mit falscher Prüfziffer übersprungen: "),
    ("`${batch.length} to go`", "`${batch.length} offen`"),
    ("`${batchIndex + 1} of ${batch.length}`", "`${batchIndex + 1} von ${batch.length}`"),
    ("CAS Supplier Search by Quentin Bindschaedler · MIT License · <a", "CAS-Lieferantensuche von Quentin Bindschaedler · MIT-Lizenz · <a"),
    (">Source code</a>", ">Quellcode</a>"),
]


def build():
    """Write cas_search_de.html; return the English strings that were not found."""
    page = (HERE / "cas_search.html").read_text(encoding="utf-8")
    missing = [en for en, _ in TEXT if en not in page]
    for en, de in TEXT:
        page = page.replace(en, de)
    (HERE / "cas_search_de.html").write_text(page, encoding="utf-8")
    return missing


if __name__ == "__main__":
    missing = build()
    print("Wrote cas_search_de.html" + (f"; English text not found: {missing}" if missing else ""))
    sys.exit(1 if missing else 0)
