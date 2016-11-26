import os

from freebora import freebora


def test_networking():
    "Test downloading networking ebooks."

    dest = os.path.join(os.path.dirname(__file__), 'ebooks')
    cat = 'networking'
    urls_path = '%s/%s-urls.txt' % (dest, cat)
    verbose = True

    # Create destination folder if needed.
    os.makedirs(dest, exist_ok=True)

    # Get list of URLs for free ebooks.
    for url in freebora.download_filelist_sync(cat=cat, verbose=verbose):
        with open(urls_path, 'a') as f:
            f.write('%s\n' % url)

    # Fetch PDFs for given URLs.
    urls = open(urls_path).read().strip().split('\n')
    # print('#URLs found: %d' % len(urls))
    freebora.download_files_sync(urls, dest=dest, overwrite=False, verbose=verbose)

    # Test the expected files were downloaded
    expected = [
        'are-your-networks-ready-for-the-iot.pdf',
        'network-automation-with-ansible.pdf',
        'privacy-and-the-iot.pdf'
    ]
    files = os.listdir(dest)
    for exp in expected:
        assert exp in files
