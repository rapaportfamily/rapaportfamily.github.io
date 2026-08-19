# -*- coding: utf-8 -*-
"""_deploy_check.py — is the site actually serving what we committed?

WHY THIS EXISTS. On 10 August the archive had four days of work in it — Berish's face and the
exact date of his death, the prison in Tarnów, 58 register scans, 133 Pages of Testimony,
Jacob's 493 images, the two-tree explorer — and none of it was on the site. Every push had
succeeded. Every report said "live". The Pages workflow had been failing on an OIDC token
error and then jamming: one run sat in the queue for 108 hours, and because the workflow uses
concurrency 'pages' with cancel-in-progress false, every deploy behind it waited too. The link
kept working, which is what made it invisible — it served the 30 July build.

So: a push is not a deploy, and a green deploy is not a live site. This asks the live URL.

  python scripts/_deploy_check.py            # compare live vs committed, and look for jams
  python scripts/_deploy_check.py --wait 300 # keep checking while a deploy propagates

exit 0 = the live site matches this checkout
exit 1 = it does not, or a run is stuck — the message says which
exit 2 = the check itself could not run (never confuse this with a healthy site)
"""
import io, os, re, sys, json, time, calendar, subprocess, argparse
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(HERE, 'platform', 'index.html')
LIVE = 'https://rapaportfamily.github.io/index.html'
STAMP = re.compile(r'auth-gate\.js\?v=([0-9A-Za-z.\-]+)')
STUCK_HOURS = 1.0

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def committed_stamp():
    if not os.path.exists(INDEX):
        return None, 'platform/index.html is not here — wrong directory?'
    m = STAMP.search(io.open(INDEX, encoding='utf-8').read())
    return (m.group(1), None) if m else (None, 'no ?v= build stamp in platform/index.html')


def live_stamp():
    """Fetch with cache defeated. A cached answer would be the same kind of lie as a cached
    service worker, and this check exists precisely because a plausible answer was wrong."""
    url = '%s?cachebust=%d' % (LIVE, time.time() * 1000)
    req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache',
                                               'User-Agent': 'rapaport-deploy-check'})
    try:
        html = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
    except Exception as e:
        return None, '%s: %s' % (type(e).__name__, e)
    m = STAMP.search(html)
    return (m.group(1), None) if m else (None, 'the live page carries no ?v= stamp')


def runs():
    """Recent workflow runs, if gh is available. Absence of gh is not a failure of the site —
    it is a gap in what this check can see, and it says so rather than staying silent."""
    try:
        out = subprocess.run(['gh', 'run', 'list', '--limit', '8', '--json',
                              'databaseId,status,conclusion,displayTitle,createdAt'],
                             cwd=HERE, capture_output=True, timeout=60)
        if out.returncode != 0:
            return None, (out.stderr or b'').decode('utf-8', 'replace').strip()[:200]
        return json.loads(out.stdout.decode('utf-8', 'replace')), None
    except Exception as e:
        return None, '%s: %s' % (type(e).__name__, e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wait', type=int, default=0,
                    help='seconds to keep re-checking while a deploy propagates')
    a = ap.parse_args()

    want, err = committed_stamp()
    if err:
        print('CANNOT CHECK: %s' % err)
        return 2
    print('committed here : %s' % want)

    deadline = time.time() + max(0, a.wait)
    while True:
        got, lerr = live_stamp()
        print('live site      : %s' % (got or 'UNREADABLE — %s' % lerr))
        if got == want:
            break
        if time.time() >= deadline:
            break
        time.sleep(15)

    problems = []
    if got is None:
        problems.append('the live site could not be read (%s)' % lerr)
    elif got != want:
        problems.append('the live site is serving %s, this checkout is %s — the deploy has NOT '
                        'landed' % (got, want))

    rs, rerr = runs()
    if rerr:
        print('workflow runs  : not visible (%s)' % rerr)
    elif rs is not None:
        now = time.time()
        stuck, failed = [], []
        for r in rs:
            if r['status'] in ('queued', 'waiting', 'pending', 'in_progress'):
                # GitHub stamps createdAt in UTC. time.mktime() would read that struct as
                # LOCAL time, and Israel is UTC+3 — which made every run look three hours
                # old the second it started, and this checker cried STUCK over its own
                # push. calendar.timegm() is the UTC-correct inverse of gmtime.
                age = (now - calendar.timegm(
                    time.strptime(r['createdAt'], '%Y-%m-%dT%H:%M:%SZ'))) / 3600.0
                if age > STUCK_HOURS:
                    stuck.append((r['databaseId'], round(age, 1), r['displayTitle'][:44]))
            elif r['conclusion'] == 'failure':
                failed.append((r['databaseId'], r['displayTitle'][:44]))
        print('workflow runs  : %d recent, %d stuck, %d failed' % (len(rs), len(stuck), len(failed)))
        for rid, age, title in stuck:
            print('   STUCK %s for %.1f h — %s' % (rid, age, title))
            problems.append('run %s has been queued %.1f hours and is holding the pages '
                            'concurrency group' % (rid, age))
        for rid, title in failed[:3]:
            print('   FAILED %s — %s' % (rid, title))

    if not problems:
        print('\nOK — the live site is serving this build.')
        return 0
    print('\nNOT LIVE:')
    for p in problems:
        print('  · %s' % p)
    print('\n  gh run list                 # look')
    print('  gh run cancel <id>          # free the queue if a run is stuck')
    print('  gh workflow run pages.yml   # deploy again')
    return 1


if __name__ == '__main__':
    sys.exit(main())
