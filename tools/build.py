"""Génère chrome/strata/strata-aero.css et strata-xp.css à partir de src/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "chrome" / "strata"

# Bouton Firefox moderne -> icône de Firefox 3
BUTTONS = {
    "reload-button": "reload",
    "stop-button": "stop",
    "home-button": "home",
    "downloads-button": "downloads",
    "history-panelmenu": "history",
    "bookmarks-menu-button": "bookmarks",
    "print-button": "print",
    "new-tab-button": "newtab",
    "new-window-button": "newwindow",
    "cut-button": "cut",
    "copy-button": "copy",
    "paste-button": "paste",
    "fullscreen-button": "fullscreen",
}


# Boutons dont l'icône n'est pas .toolbarbutton-icon
ICON_ELEMENT = {"downloads-button": "#downloads-indicator-icon"}


def icon_rules():
    rules = []
    for sel, size in (("#nav-bar", ""), ("#navigator-toolbox > toolbar:not(#nav-bar)", "-16")):
        rules.append(f"/* {sel} */")
        for button, icon in BUTTONS.items():
            base = f"{sel} #{button}"
            target = ICON_ELEMENT.get(button, ".toolbarbutton-icon")
            img = f'url("images/@V@/{icon}{size}'
            rules.append(f'{base} {target} {{ list-style-image: {img}.png") !important; }}')
            rules.append(f'{base}:not([disabled]):hover {target} {{ list-style-image: {img}-hover.png") !important; }}')
            rules.append(f'{base}[disabled] {target} {{ list-style-image: {img}-disabled.png") !important; }}')
        rules.append("")
    return "\n".join(rules)


def main():
    template = (SRC / "strata.template.css").read_text(encoding="utf-8")
    template = template.replace("@@ICONS@@", icon_rules())
    marker = "/* ---------- Variables"
    head, tail = template.split(marker, 1)
    for variant in ("aero", "xp"):
        colors = (SRC / f"variant-{variant}.css").read_text(encoding="utf-8")
        css = head + colors + "\n" + marker + tail
        (OUT / f"strata-{variant}.css").write_text(css.replace("@V@", variant), encoding="utf-8")
    print("strata-aero.css et strata-xp.css générés dans", OUT)


if __name__ == "__main__":
    main()
