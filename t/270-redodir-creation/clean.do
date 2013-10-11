exec >&2
rm -f build/output
# NOTE: could break .redo metadata, but required
# for the test itself to pass
find src build -name '.redo' | xargs rm -rf
