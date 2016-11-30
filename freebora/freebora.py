
import re
import os
import asyncio
import concurrent

import requests
import aiohttp
import aiofiles
from lxml import etree


# sequential

def get_cats_sync(full_urls=False, verbose=False):
    "Generate category URLs for free O'Reilly ebooks."

    base_url = 'http://shop.oreilly.com'
    url = base_url + '/category/ebooks.do'
    if verbose:
        print(url)
    p = etree.HTMLParser()
    tree = etree.parse(url, parser=p)
    xpath_expr = '//a[starts-with(@href, "/category/ebooks/")]/@href'
    cat_urls = tree.xpath(xpath_expr)
    cat_urls = [base_url + u for u in cat_urls if u.endswith('.do')]
    for u in cat_urls:
        if verbose:
            print(u)
        tree1 = etree.parse(u, parser=p)
        urls = tree1.xpath(xpath_expr)
        for u in urls:
            if not u.endswith('.do'):
                continue
            if full_urls:
                yield base_url + u
            else:
                pat = 'category/ebooks/(.*?).do'
                yield re.findall(pat, u)[0]


def download_filelist_sync(cat, verbose=False):
    "Generate URLs for free O'Reilly ebooks in PDF format."

    url = 'http://shop.oreilly.com/category/ebooks/%s.do' % cat
    if verbose:
        print(url)
    p = etree.HTMLParser()
    t1 = etree.parse(url, parser=p)
    table_pag1 = t1.xpath('//table[@class="pagination"]')[0]
    xp = '//td[@class="default"]/select[@name="dirPage"]/option/@value'
    page_urls = set(table_pag1.xpath(xp))
    for i, page_url in enumerate(page_urls):
        # if verbose:
        #     print(page_url)
        t2 = etree.parse('http://shop.oreilly.com' + page_url, parser=p)
        xp = '//span[@class="price"][contains(., "$0.00")]/'\
             '../../../../div[@class="thumbheader"]/a/@href'
        paths = t2.xpath(xp)
        for j, path in enumerate(paths):
            url = 'http://shop.oreilly.com' + path
            html = requests.get(url).text
            url_csps = re.findall('path_info\:\s+(.*?\.csp)', html)
            if len(url_csps) != 1:
                continue
            url_csp = url_csps[0]
            url_csp = re.sub('\?.*', '', url_csp)
            url_pdf = re.sub('\.csp', '.pdf', url_csp)
            url_pdf = re.sub('/free/', '/free/files/', url_pdf)
            u = 'http://www.oreilly.com/%s' % url_pdf
            if verbose:
                print(u)
            yield u


def download_files_sync(urls, dest='.', overwrite=False, verbose=False):
    "Download a list of URLs sequentially (synchronuously)."

    for url in urls:
        pdf_name = os.path.basename(url)
        path = os.path.join(dest, pdf_name)
        if not os.path.exists(path) or overwrite:
            # if verbose:
            #     print(url)
            response = requests.get(url)
            pdf = response.content
            # if verbose:
            #     print('%s %d' % (url, len(pdf)))
            open(path, mode='wb').write(pdf)
            if verbose:
                print('saved %s (%d bytes)' % (path, len(pdf)))


# parallel

async def fetch(session, url, dest='.', overwrite=False, verbose=False):
    "Fetch a single PDF file if not already existing."

    pdf_name = os.path.basename(url)
    path = os.path.join(dest, pdf_name)
    if not os.path.exists(path) or overwrite:
        # if verbose:
        #     print(url)
        with aiohttp.Timeout(60, loop=session.loop):
            async with session.get(url) as response:
                pdf = await response.read()
                # if verbose:
                #     print('%s %d' % (url, len(pdf)))
                async with aiofiles.open(path, mode='wb') as f:
                    await f.write(pdf)
                    if verbose:
                        print('saved %s (%d bytes)' % (path, len(pdf)))


async def fetch_async(loop, urls, dest='.', overwrite=False, verbose=False):
    "Download a list of URLs in parallel (asynchronuously)."

    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [fetch(session, url, 
            dest=dest, overwrite=overwrite, verbose=verbose) for url in urls]
        await asyncio.gather(*tasks)


def download_files_async(urls, dest='.', overwrite=False, verbose=False):
    "Build and execute async. event loop for downloading a list of URLs."

    # This can produce timeouts which are cached and worked around, which 
    # slows down the process. It's not very clear how to best select the 
    # chunk size and number of workers for the ThreadPoolExecutor, both
    # hardcoded below.

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(20)
    loop.set_default_executor(executor)
    while urls:
        chunk, urls = urls[:10], urls[10:]
        while True:
            try:
                loop.run_until_complete(fetch_async(loop, chunk, 
                    dest=dest, overwrite=overwrite, verbose=verbose))
                break
            except concurrent.futures._base.TimeoutError:
                print('retrying...')
    executor.shutdown(wait=True)
    loop.close()
