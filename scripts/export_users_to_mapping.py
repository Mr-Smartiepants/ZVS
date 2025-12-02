#!/usr/bin/env python3
"""
This script used to export firstname/name to `user_mapping.csv` during migration.
It has been intentionally replaced with a safe no-op to avoid accidental use now
that the database no longer contains `firstname`/`name` columns.

If you still need to export legacy names, run a manual SQL query or restore from
your offline backup. The migration README has guidance.
"""

import sys

def main():
    print("The export script has been removed/replaced. See scripts/README_MIGRATION.md for alternatives.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
