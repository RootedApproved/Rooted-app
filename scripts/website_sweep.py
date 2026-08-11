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

# WORD BOUNDARIES MATTER HERE. Without them "cialis" matches inside "speCIALISt" and
# flagged two Gelson's store pages as hijacked. A false alarm on this check is expensive:
# it accuses a legitimate business of serving pharmacy spam. Two or more distinct hits
# are also required, because one stray word in a vendor name is not a compromised site.
RISKY = re.compile(
    r'\b(casinos?|betting|sportsbook|paris sportif|slots? online|poker|'
    r'no deposit bonus|blackjack|roulette|bookmaker|wagering|online gambling|'
    r'viagra|cialis|porn|xxx|escort service|crypto ?signals|forex ?signals)\b', re.I)

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


# A site that refuses a bot is not a dead site. Trader Joe's, Bristol Farms and Mendocino
# Farms all return 403 or 503 to anything that looks automated. Reporting those as broken
# links would send J to check dozens of perfectly live pages, so they are recorded as
# BLOCKED - meaning "cannot verify", which is a different claim from "broken".
BLOCKING_CODES = {401, 403, 405, 406, 429, 503}

# Client-rendered sites return a near-empty HTML shell. Squarespace, Wix, Webflow and
# React apps all do it. An empty <body> is evidence of a framework, not of an empty site.
JS_SHELL = re.compile(
    r'(squarespace|wix\.com|_wixCssStates|webflow|__NEXT_DATA__|id="root"|id="__nuxt"|'
    r'data-reactroot|shopify|gatsby|window\.__INITIAL|elementor)', re.I)


def registrable(h):
    """crude eTLD+1 so shop.brand.com and www.brand.com compare equal"""
    parts = (h or '').split('.')
    return '.'.join(parts[-2:]) if len(parts) >= 2 else h


def check(item):
    name, url, typ = item['name'], item['url'], item['type']
    out = dict(name=name, url=url, type=typ)
    try:
        status, final, body = fetch(url)
    except urllib.error.HTTPError as e:
        if e.code in BLOCKING_CODES:
            out.update(verdict='BLOCKED',
                       detail=f'HTTP {e.code} to an automated request — likely bot protection, '
                              f'not a dead site')
        else:
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

    # Content is judged BEFORE the redirect check. Doing it the other way round hid a
    # gambling hijack: gospelflatfarm.com redirects to an Indonesian lottery site, and
    # because the redirect test returned first it was filed as a harmless "site moved".
    # Where a link goes matters less than what is served when you arrive.
    hits = {m.group(0).lower() for m in RISKY.finditer(text)}
    if len(hits) >= 2:
        out.update(verdict='RISKY_CONTENT',
                   detail='page carries gambling/pharma spam terms: '
                          + ', '.join(sorted(hits)[:6]))
        return out
    if hits:
        out.update(verdict='RISKY_MAYBE',
                   detail=f'single risky term "{list(hits)[0]}" — probably innocent, worth a glance')
        return out
    parked = PARKED.search(text) or PARKED.search(title)
    if parked:
        out.update(verdict='PARKED', detail=f'looks parked/for sale: "{parked.group(0)}"')
        return out
    if host(final) != host(url):
        # erewhonmarket.com -> ship.erewhon.com is the same business moving its own site.
        # Only a redirect to an UNRELATED registrable domain is worth reporting.
        if registrable(host(final)) != registrable(host(url)):
            a = set(re.sub(r'[^a-z0-9]', ' ', registrable(host(url))).split())
            b = set(re.sub(r'[^a-z0-9]', ' ', registrable(host(final))).split())
            shared = any(x[:5] == y[:5] for x in a for y in b if len(x) > 4 and len(y) > 4)
            if not shared:
                out.update(verdict='REDIRECTED',
                           detail=f'{host(url)} now lands on {host(final)}')
                return out
    if re.search(r'sgcaptcha|cf-browser-verification|challenge-platform|'
                 r'just a moment|checking your browser|captcha', body, re.I):
        out.update(verdict='BLOCKED',
                   detail='served a bot-protection challenge instead of the page')
        return out
    if len(text.strip()) < 250:
        if JS_SHELL.search(body):
            out.update(verdict='JS_RENDERED',
                       detail='content is rendered by JavaScript — cannot verify from HTML alone')
        else:
            out.update(verdict='EMPTY',
                       detail=f'page has almost no content ({len(text.strip())} chars)')
        return out

    toks = name_tokens(name)
    hay = (text + ' ' + title + ' ' + url).lower()
    if toks and not any(t in hay for t in toks):
        # A market's site is often the OPERATOR's site: the Pacific Palisades market runs
        # on rawinspiration.org. That is legitimate, so this is reported for a human to
        # glance at rather than treated as evidence the link is wrong.
        out.update(verdict='NAME_ABSENT',
                   detail=f'listing name not on the page — may be the operator\'s site '
                          f'(title: {title!r})')
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
