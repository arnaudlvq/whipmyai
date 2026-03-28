#!/bin/zsh
# Adds a 'whip' alias to ~/.zshrc pointing to this project directory.

DIR="$(cd "$(dirname "$0")" && pwd)"
ZSHRC="$HOME/.zshrc"
MARKER="# whipmyai alias"

if grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
  echo "Alias already present in $ZSHRC — nothing to do."
  echo "Run 'whip' to toggle."
  exit 0
fi

cat >> "$ZSHRC" <<EOF

$MARKER
whip() {
  if make -C "$DIR" status 2>/dev/null | grep -q "running"; then
    make -C "$DIR" stop
  else
    make -C "$DIR" start
  fi
}
EOF

echo "✓ Alias 'whip' added to $ZSHRC (project path: $DIR)"
echo ""
echo "Reload your shell:"
echo "  source ~/.zshrc"
echo ""
echo "Then just type 'whip' to start or stop the daemon."
