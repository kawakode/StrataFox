"""Découpe les sprites originaux de Firefox 3.6 (winstripe) en images individuelles."""
import os, shutil, sys
from PIL import Image

SRC = sys.argv[1]          # racine gecko (browser/themes/winstripe, toolkit/themes/winstripe)
OUT = sys.argv[2]          # dossier chrome/strata/images
B = os.path.join(SRC, "browser/themes/winstripe/browser")
T = os.path.join(SRC, "toolkit/themes/winstripe/global")

ICONS = ["back", "forward", "stop", "reload", "home", "downloads", "history",
         "bookmarks", "print", "newtab", "newwindow", "cut", "copy", "paste", "fullscreen"]

def crop(im, box, path):
    im.crop(box).save(path, optimize=True)

def suffixed(path, sfx):
    root, ext = os.path.splitext(path)
    cand = root + sfx + ext
    return cand if sfx and os.path.exists(cand) else path

for variant, sfx in (("xp", ""), ("aero", "-aero")):
    d = os.path.join(OUT, variant)
    os.makedirs(d, exist_ok=True)
    # Grandes icônes 24px : lignes normal / survol / désactivé
    big = Image.open(suffixed(os.path.join(B, "Toolbar.png"), sfx)).convert("RGBA")
    for i, name in enumerate(ICONS):
        for row, state in enumerate(("", "-hover", "-disabled")):
            crop(big, (i * 24, row * 24, i * 24 + 24, row * 24 + 24), f"{d}/{name}{state}.png")
    # Petites icônes 16px
    small = Image.open(suffixed(os.path.join(B, "Toolbar-small.png"), sfx)).convert("RGBA")
    for i, name in enumerate(ICONS):
        for row, state in enumerate(("", "-hover", "-disabled")):
            crop(small, (i * 16, row * 16, i * 16 + 16, row * 16 + 16), f"{d}/{name}-16{state}.png")
    # Bouton « trou de serrure » (keyhole) : normal / survol / désactivé / enfoncé
    for row, state in enumerate(("", "-hover", "-disabled", "-active")):
        y = row * 34
        crop(big, (360, y, 396, y + 34), f"{d}/keyhole-back{state}.png")
        crop(big, (396, y + 3, 422, y + 31), f"{d}/keyhole-forward{state}.png")
        crop(big, (422, y + 3, 438, y + 31), f"{d}/keyhole-dropmarker{state}.png")
        y = row * 24
        crop(small, (240, y, 264, y + 24), f"{d}/keyhole-back-16{state}.png")
        crop(small, (264, y, 288, y + 24), f"{d}/keyhole-forward-16{state}.png")
        crop(small, (288, y, 301, y + 24), f"{d}/keyhole-dropmarker-16{state}.png")
    # Bouton « Aller » : normal / survol
    go = Image.open(suffixed(os.path.join(B, "Go-arrow.png"), sfx)).convert("RGBA")
    crop(go, (0, 0, 16, 16), f"{d}/go.png")
    crop(go, (0, 16, 16, 32), f"{d}/go-hover.png")
    # Étoile des marque-pages
    star = Image.open(suffixed(os.path.join(B, "places/bookmark.png"), sfx)).convert("RGBA")
    for i, state in enumerate(("", "-hover", "-active")):
        crop(star, (i * 16, 0, i * 16 + 16, 16), f"{d}/star{state}.png")
    shutil.copy(suffixed(os.path.join(B, "places/editBookmark.png"), sfx), f"{d}/star-starred-full.png")
    starred = Image.open(f"{d}/star-starred-full.png").convert("RGBA")
    crop(starred, (0, 0, 16, 16), f"{d}/star-starred.png")
    os.remove(f"{d}/star-starred-full.png")
    # Bouton de fermeture d'onglet : sélectionné / survol / enfoncé / normal
    close = Image.open(suffixed(os.path.join(T, "icons/close.png"), sfx)).convert("RGBA")
    for i, state in enumerate(("-selected", "-hover", "-active", "")):
        crop(close, (i * 14, 0, i * 14 + 14, 14), f"{d}/tab-close{state}.png")
    # Loupe de la barre de recherche
    glass = Image.open(suffixed(os.path.join(T, "icons/Search-glass.png"), sfx)).convert("RGBA")
    for i, state in enumerate(("", "-hover", "-active")):
        crop(glass, (i * 16, 0, i * 16 + 16, 16), f"{d}/search-glass{state}.png")
    # Dossier / page par défaut
    folder = Image.open(suffixed(os.path.join(T, "icons/folder-item.png"), sfx)).convert("RGBA")
    crop(folder, (0, 0, 16, 16), f"{d}/page.png")
    crop(folder, (16, 0, 32, 16), f"{d}/folder.png")
    crop(folder, (16, 16, 32, 32), f"{d}/folder-open.png")
    # Onglets : nouvel onglet, liste, flèches de défilement
    nt = Image.open(suffixed(os.path.join(B, "tabbrowser/newtab.png"), sfx)).convert("RGBA")
    crop(nt, (0, 0, 18, 18), f"{d}/tabs-newtab.png")
    crop(nt, (18, 0, 36, 18), f"{d}/tabs-newtab-active.png")
    at = Image.open(suffixed(os.path.join(B, "mainwindow-dropdown-arrow.png"), sfx)).convert("RGBA")
    crop(at, (0, 0, 13, 11), f"{d}/tabs-alltabs.png")
    crop(at, (13, 0, 26, 11), f"{d}/tabs-alltabs-active.png")
    for side in ("left", "right"):
        ar = Image.open(suffixed(os.path.join(B, f"tabbrowser/tab-arrow-{side}.png"), sfx)).convert("RGBA")
        for i, state in enumerate(("", "-hover", "-active")):
            crop(ar, (i * 15, 0, i * 15 + 15, 17), f"{d}/tab-arrow-{side}{state}.png")
    # Images copiées telles quelles
    for src, dst in (("navbar-textbox-buttons.png", "identity-box.png"),
                     ("urlbar-favicon-glow.png", "favicon-glow.png"),
                     ("places/bookmarksToolbar.png", "bookmarks-toolbar.png"),
                     ("places/history.png", "history-16.png"),
                     ("places/allBookmarks.png", "all-bookmarks.png"),
                     ("feeds/feedIcon16.png", "feed.png"),
                     ("places/searching_16.png", "searching.png"),
                     ("Secure.png", "secure.png"),
                     ("tabbrowser/progress.png", "progress.png")):
        shutil.copy(suffixed(os.path.join(B, src), sfx), f"{d}/{dst}")
    shutil.copy(suffixed(os.path.join(T, "icons/loading_16.png"), sfx), f"{d}/loading.png")

# Fonds communs (pas de variante -aero dans l'original)
c = os.path.join(OUT, "common")
os.makedirs(c, exist_ok=True)
for f in ("tabbrowser-tabs-bkgnd.png", "tab-bkgnd.png", "tab-hover-bkgnd.png",
          "tab-active-bkgnd.png", "tabstrip-bottom.png"):
    shutil.copy(os.path.join(B, "tabbrowser", f), os.path.join(c, f))
print("ok")
