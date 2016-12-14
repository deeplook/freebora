#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI entry point for the program.
"""

from __future__ import unicode_literals, print_function
import os
import sys
import argparse

from freebora.version import __version__
if sys.version_info.major >= 3:
    from freebora.freebora import download_filelist_sync, \
        download_files_sync, download_files_async, get_cats_sync
else:
    # Python 2 not really supported, yet
    from freebora import download_filelist_sync, download_files_sync, \
        download_files_async, get_cats_sync


def main():
    desc = 'Download free ebooks from http://shop.oreilly.com/'\
           'category/ebooks.do.'
    p = argparse.ArgumentParser(description=desc)

    p.add_argument('-v', '--verbose', action='store_true',
        help='Set more verbose (debugging) output.')
    p.add_argument('-V', '--version', action='store_true',
        help='Show version number and quit.')
    p.add_argument('--dest', metavar='PATH', default='.',
        help='Destination folder path, for both the URL list and/or the '
             'downloaded PDFs. Will be created if not existing.')
    p.add_argument('--overwrite', action='store_true',
        help='Overwrite previously created file(s), for both the URL '
             'list and/or downloaded PDFs.')
    p.add_argument('--cat', metavar='NAME', default='data',
        help='Category of ebooks to download, e.g. data (default), '\
             'design, iot, python/programming, ... Get a full list '\
             'with --list-cats-sync.')
    p.add_argument('--list-cats-sync', action='store_true',
        help='Collect and list available ebook category names (to use with --cat).')
    p.add_argument('--list-sync', metavar='NAME',
        help='Collect URLs to be downloaded into given filename.')
    p.add_argument('--fetch-sync', metavar='NAME',
        help='Download URLs sequentially from given filename.')
    p.add_argument('--fetch-async', metavar='NAME',
        help='Download URLs in parallel from given filename.')

    args = p.parse_args()

    if args.version:
        print('Freebora version %s' % __version__)
        sys.exit()

    # Create destination folder if needed.
    if args.dest != '.':
        created = False
        if not os.path.exists(args.dest):
            os.makedirs(args.dest, exist_ok=True)
            created = True
        if args.verbose and os.path.exists(args.dest) and created:
            print('Created destination folder: "%s"' % args.dest)

    # Get list of free ebook categories.
    if args.list_cats_sync:
        for cat in get_cats_sync(full_urls=False, verbose=args.verbose):
            print(cat)

    # Get list of URLs for free ebooks.
    if args.list_sync:
        path = os.path.join(args.dest, args.list_sync)
        if not os.path.exists(path) or args.overwrite:
            for url in  download_filelist_sync(cat=args.cat, verbose=args.verbose):
                with open(path, 'a') as f:
                    f.write('%s\n' % url)

    # Fetch PDFs for given URLs.
    if args.fetch_sync or args.fetch_async:
        if args.fetch_sync:
            path = args.fetch_sync
        elif args.fetch_async:
            path = args.fetch_async
        urls = open(os.path.join(args.dest, path)).read().strip().split('\n')
        print('#URLs found: %d' % len(urls))

        if args.fetch_sync:
            f = download_files_sync
        elif args.fetch_async:
            f = download_files_async
        f(urls, dest=args.dest, overwrite=args.overwrite, verbose=args.verbose)


if __name__ == '__main__':
    main()
