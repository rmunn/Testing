This directory is where you should put any "scratchpad" files that you
want to keep around, but don't want to actually commit to the repository.
For example, notes-to-self-about-that-difficult-bug.txt could go here.
Because the whole directory is included in .gitignore, anything in here
will be ignored by default, and won't clutter up your "git status" output.

Note that any files (like this README.txt) that you explicitly add to the
repository WILL be tracked, despite their directory being in .gitignore.
This is perfect: this README.txt will appear whenever you clone the project,
reminding you what this directory is for, but the directory will still
retain its "scratchpad, therefore ignored" status for other files.
