mkdir -p x/y
redo x/y/z
redo x/y/somefile

[ "$(cat x/y/somefile)" = "default" ] || exit 11
[ "$(cat x/y/z)" = "z" ] || exit 12

