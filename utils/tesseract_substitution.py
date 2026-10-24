#!/usr/bin/env python3

# Copyright 2026 The Tesseract Authors
# You can use, redistribute, and/or modify this source code under
# the terms of the GPL-3.0 license that can be found in the LICENSE file.
"""
Post-pass after name_substitution.py: replaces the Helium product name with
Tesseract in .grd/.xtb strings. URLs, reverse-DNS IDs and the upstream
authors credit are left alone. The helium:// scheme is kept as is, because
the scheme itself is defined by Helium's patches.
"""

import multiprocessing
import re

REPLACEMENT_REGEX = re.compile(r'(?<!The )\bHelium\b(?! Authors)')


def replace_text(text):
    """Replaces the Helium product name with Tesseract in a string"""
    replaced, count = REPLACEMENT_REGEX.subn('Tesseract', text)
    return replaced, count > 0


def main():
    """CLI entrypoint: same file selection and l10n handling as name_substitution.py"""
    # pylint: disable=import-outside-toplevel
    import name_substitution
    import name_substitution_utils

    # Workers must inherit the swapped replace_text, so they are forked.
    multiprocessing.set_start_method('fork')
    name_substitution_utils.replace_text = replace_text

    args = name_substitution.parse_args()
    if not (args.t / "OWNERS").exists():
        raise ValueError("wrong src directory")
    if args.unsub:
        name_substitution.do_unsubstitution(args.t, args.backup_path)
    else:
        name_substitution.do_substitution(args.t, args.backup_path, args.workers, args.dry_run)


if __name__ == '__main__':
    main()
