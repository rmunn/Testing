#!/usr/bin/env python3
#
# check-py3-compat - check Python 3 compatibility of Mercurial files
#
# Copyright 2015 Gregory Szorc <gregory.szorc@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.


import ast
import importlib
import os
import sys
import traceback
import warnings


def check_compat_py3(f):
    """Check Python 3 compatibility of a file with Python 3."""
    with open(f, 'rb') as fh:
        content = fh.read()

    try:
        ast.parse(content, filename=f)
    except SyntaxError as e:
        print('%s: invalid syntax: %s' % (f, e))
        return

    # Try to import the module.
    # For now we only support modules in packages because figuring out module
    # paths for things not in a package can be confusing.
    if f.startswith(
        ('hgdemandimport/', 'hgext/', 'mercurial/')
    ) and not f.endswith('__init__.py'):
        assert f.endswith('.py')
        name = f.replace('/', '.')[:-3]
        try:
            importlib.import_module(name)
        except Exception as e:
            exc_type, exc_value, tb = sys.exc_info()
            # We walk the stack and ignore frames from our custom importer,
            # import mechanisms, and stdlib modules. This kinda/sorta
            # emulates CPython behavior in import.c while also attempting
            # to pin blame on a Mercurial file.
            for frame in reversed(traceback.extract_tb(tb)):
                if frame.name == '_call_with_frames_removed':
                    continue
                if 'importlib' in frame.filename:
                    continue
                if 'mercurial/__init__.py' in frame.filename:
                    continue
                if frame.filename.startswith(sys.prefix):
                    continue
                break

            if frame.filename:
                filename = os.path.basename(frame.filename)
                print(
                    '%s: error importing: <%s> %s (error at %s:%d)'
                    % (f, type(e).__name__, e, filename, frame.lineno)
                )
            else:
                print(
                    '%s: error importing module: <%s> %s (line %d)'
                    % (f, type(e).__name__, e, frame.lineno)
                )


if __name__ == '__main__':
    # check_compat_py3 will import every filename we specify as long as it
    # starts with one of a few prefixes. It does this by converting
    # specified filenames like 'mercurial/foo.py' to 'mercurial.foo' and
    # importing that. When running standalone (not as part of a test), this
    # means we actually import the installed versions, not the files we just
    # specified. When running as test-check-py3-compat.t, we technically
    # would import the correct paths, but it's cleaner to have both cases
    # use the same import logic.
    sys.path.insert(0, os.getcwd())

    for f in sys.argv[1:]:
        with warnings.catch_warnings(record=True) as warns:
            check_compat_py3(f)

        for w in warns:
            print(
                warnings.formatwarning(
                    w.message, w.category, w.filename, w.lineno
                ).rstrip()
            )

    sys.exit(0)
