#!/usr/bin/env python3
"""
Check every media_website on the catalogue for being dead, parked, or hijacked.

WHY THIS IS NOT JUST A LINK CHECKER
A 404 is the harmless failure. The dangerous one is a domain that LAPSED and was
re-registered by someone else: it returns HTTP 200, looks alive to any status check, and
serves whatever the new owner wants. One was already found on this catalogue redirecting
to gambling content. On a platform whose entire claim is that listings are verified, a
link to a casino is a different category of problem from a broken link.

So each URL is judged on four things, not one:
  status      did it respond at all
  redirect    did it land on a different domain than the one recorded
  content     does the page look parked, for-sale, or like adult/gambling content
  identity    does the business name actually appear on the page

The last is what separates "the site moved" from "someone else owns this now".
"""
import concurrent.futures as cf
import gzip
import io
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')

PARKED = re.compile(
    r'(domain (is )?for sale|buy this domain|this domain (may be|is) for sale|'
    r'parked (free )?(by|at)|domain parking|godaddy\.com/domainsearch|'
    r'sedoparking|hugedomains|afternic|dan\.com|namecheap.*parked|'
    r'expired domain|renew (your |this )?domain|website coming soon|'
    r'account suspended|site temporarily unavailable)', re.I)

RISKY = re.compile(
    r'(casino|betting|sportsbook|slots online|poker room|no deposit bonus|'
    r'blackjack|roulette|bookmaker|wagering|online gambling|'
    r'viagra|cialis|porn|xxx|escort service|crypto ?signals|forex ?signals)', re.I)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA, 'Accept': 'text/html,*/*',
        'Accept-Language': 'en-US,en;q=0.9', 'Accept-Encoding': 'gzip'})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        raw = r.read(400000)
        if r.headers.get('Content-Encoding') == 'gzip':
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass
        return r.status, r.geturl(), raw.decode('utf-8', 'replace')


def host(u):
    try:
        return urllib.parse.urlparse(u).hostname.replace('www.', '').lower()
    except Exception:
        return ''


def name_tokens(name):
    stop = {'the', 'and', 'market', 'markets', 'farmers', 'farmer', 'certified',
            'cfm', 'farm', 'farms', 'organic', 'co', 'inc', 'llc', 'company'}
    return {w for w in re.sub(r'[^a-z0-9 ]', ' ', (name or '').lower()).split()
            if len(w) > 2 and w not in stop}


def check(item):
    name, url, typ = item['name'], item['url'], item['type']
    out = dict(name=name, url=url, type=typ)
    try:
        status, final, body = fetch(url)
    except urllib.error.HTTPError as e:
        out.update(verdict='HTTP_ERROR', detail=f'HTTP {e.code}')
        return out
    except Exception as e:
        out.update(verdict='UNREACHABLE', detail=f'{type(e).__name__}: {str(e)[:70]}')
        return out

    out['final'] = final
    out['status'] = status
    text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', body,
                  flags=re.S | re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)[:20000]
    title = ''
    tm = re.search(r'<title[^>]*>(.*?)</title>', body, re.S | re.I)
    if tm:
        title = re.sub(r'\s+', ' ', tm.group(1)).strip()[:120]
    out['title'] = title

    risky = RISKY.search(text)
    if risky:
        out.update(verdict='RISKY_CONTENT',
                   detail=f'page mentions "{risky.group(0)}" — possible hijacked domain')
        return out
    parked = PARKED.search(text) or PARKED.search(title)
    if parked:
        out.update(verdict='PARKED', detail=f'looks parked/for sale: "{parked.group(0)}"')
        return out
    if host(final) != host(url):
        out.update(verdict='REDIRECTED',
                   detail=f'{host(url)} now lands on {host(final)}')
        return out
    if len(text.strip()) < 250:
        out.update(verdict='EMPTY', detail=f'page has almost no content ({len(text.strip())} chars)')
        return out

    toks = name_tokens(name)
    hay = (text + ' ' + title + ' ' + url).lower()
    if toks and not any(t in hay for t in toks):
        out.update(verdict='NAME_ABSENT',
                   detail=f'no part of the listing name appears on the page (title: {title!r})')
        return out
    out.update(verdict='OK', detail='live, on the recorded domain, name present')
    return out


def main():
    items = json.load(open('/home/claude/websites.json'))
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else len(items)
    batch = items[start:start + count]
    results = []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        for r in ex.map(check, batch):
            results.append(r)
    json.dump(results, open(f'/home/claude/websweep_{start:04d}.json', 'w'), indent=1)
    from collections import Counter
    print(dict(Counter(r['verdict'] for r in results)))


if __name__ == '__main__':
    main()
