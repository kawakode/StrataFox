#!/bin/sh
# Crée dist/StrataFox-<version>.zip : dossier chrome, instructions et licences.
# Usage : tools/package.sh v1.0.0
set -eu

VERSION="${1:?usage: tools/package.sh <version>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="$ROOT/dist/stage"
ZIP="$ROOT/dist/StrataFox-$VERSION.zip"

rm -rf "$STAGE" "$ZIP"
mkdir -p "$STAGE"
cp -R "$ROOT/chrome" "$STAGE/chrome"
cp "$ROOT/release/INSTALLATION.txt" "$ROOT/LICENSE" "$ROOT/LICENSE-MPL-1.1.txt" "$STAGE/"
# Fins de ligne Windows pour les fichiers texte ouverts dans le Bloc-notes
for f in INSTALLATION.txt chrome/userChrome.css; do
  sed 's/\r*$/\r/' "$STAGE/$f" > "$STAGE/$f.tmp" && mv "$STAGE/$f.tmp" "$STAGE/$f"
done
find "$STAGE" -name '.DS_Store' -delete

(cd "$STAGE" && zip -qrX "$ZIP" .)
rm -rf "$STAGE"
echo "$ZIP"
