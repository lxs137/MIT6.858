#!/bin/sh

# Download and install phantomjs; the version on Debian doesn't work with the
# grading scripts, since it doesn't render fonts correctly on the default VM.
PHANTOMJS=phantomjs-2.1.1-linux-x86_64
if [ ! -e "$HOME/phantomjs" ]; then
  echo "One moment, downloading PhantomJS..."
  TEMPFILE=$(mktemp)
  TEMPDIR=$(mktemp -d)
  wget -O "$TEMPFILE" "https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOMJS.tar.bz2"
  echo "Unpacking..."
  tar -C "$TEMPDIR" -xjf "$TEMPFILE"
  mv "$TEMPDIR/$PHANTOMJS/bin/phantomjs" "$HOME"
  # Cleanup
  rm "$TEMPFILE"
  rm -rf "$TEMPDIR"
  echo "Done"
fi
