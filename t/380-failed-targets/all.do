exec >&2
redo output

rm -f VERSION
st=0
redo VERSION 2>/dev/null || st=$?

[ "$st" -ne 0 ] || (echo "created VERSION"; exit 5)

echo 0.1 > VERSION

output="$(redo-ifchange VERSION 2>&1)"
st=$?
[ "$st" -eq 0 ] || (echo "redo VERSION failed"; exit 6)
[ "x$output" = "x" ] || (echo "redo-ifchange VERSION printed: $output"; exit 7)
