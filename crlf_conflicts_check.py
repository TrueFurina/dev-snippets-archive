import json, os, urllib.request, urllib.error

TOKEN = os.environ['GITHUB_TOKEN']
op = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def japi(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/vnd.github+json', 'User-Agent': 'atomcode'})
    return json.load(op.open(req, timeout=20))

def raw_fetch(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/vnd.github.raw', 'User-Agent': 'atomcode'})
    return op.open(req, timeout=30).read()

CASES = [
    ('opendatahub-io/notebooks', 4461, TrueFurina_repo := 'TrueFurina/notebooks'),
    ('Trustpoint-Project/trustpoint', 901, 'TrueFurina/trustpoint'),
]

for repo, num, fork in CASES:
    print('#####', repo + '#' + str(num))
    try:
        p = japi('https://api.github.com/repos/' + repo + '/pulls/' + str(num))
    except urllib.error.HTTPError as e:
        print('  PR fetch err', e.code)
        continue
    head_repo = (p['head'].get('repo') or {}).get('full_name')
    br = p['head']['ref']
    print('  head repo:', head_repo, '| branch:', br, '| state:', p.get('mergeable_state'))
    if not head_repo:
        print('  fork deleted - skip')
        continue
    fs = japi('https://api.github.com/repos/' + repo + '/pulls/' + str(num) + '/files?per_page=100')
    print('  changed files:', len(fs))
    churn = []
    for f in fs:
        fn = f['filename']
        sym = f['additions'] == f['deletions'] and f['additions'] > 10
        cr_mine = None
        try:
            mine = raw_fetch('https://api.github.com/repos/' + head_repo + '/contents/' + fn + '?ref=' + br)
            cr_mine = mine.count(b'\r\n')
            cr_up = -1
            try:
                up = raw_fetch('https://api.github.com/repos/' + repo + '/contents/' + fn + '?ref=' + (p['base']['ref']))
                cr_up = up.count(b'\r\n')
            except urllib.error.HTTPError:
                pass
            print('  ', fn[:58], '| mine CR:', cr_mine, '| up CR:', cr_up, '| +' + str(f['additions']), '-' + str(f['deletions']), '<<< CHURN?' if sym and cr_mine and not cr_up else ('<<< CRLF CONFIRMED' if cr_mine and cr_up == 0 else ''))
        except urllib.error.HTTPError as e2:
            print('  ', fn[:58], '| fetch err', e2.code)
    print()
