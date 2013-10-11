set -eu
redo build/output
dodirs="$(find . -name 'do' | wc -l)"
[ "$dodirs" -eq "0" ] || exit 5

# we expect .redo dir in root and build, but not in src/
redodirs="$(find . -name '.redo' | wc -l)"
[ "$redodirs" -eq "2" ] || (echo "$redodirs" >&2; exit 6)
