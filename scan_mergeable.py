import json, os, urllib.request, urllib.error

TOKEN = os.environ['GITHUB_TOKEN']
op = urllib.request.build_opener()

def japi(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/vnd.github+json', 'User-Agent': 'atomcode'})
    return json.load(op.open(req, timeout=20))

# 全量拉取我名下 open PR（跨页）
prs = []
page = 1
while True:
    batch = japi('https://api.github.com/user/prs?scope=created_by_me&state=open&per_page=100&page=' + str(page))
    if not batch:
        break
    prs.extend(batch)
    if len(batch) < 100:
        break
    page += 1
print('total open PRs:', len(prs))

states = {}
notable = []
for p in prs:
    st = p.get('mergeable_state')
    repo = p['base']['repo']['full_name']
    states[st] = states.get(st, 0) + 1
    # 非常态（可推进信号）：clean/ready/unstable-with-green、或 has comments 未读
    if st in ('clean', 'has_hooks', 'unknown', None):
        notable.append((repo, p['number'], st, p['title'][:40]))
    elif st == 'blocked':
        pass

print('state 分布:', states)
print()
print('=== 非常态 PR（潜在可推进） ===')
for repo, num, st, title in notable[:30]:
    print(repo + '#' + str(num), '|', st, '|', title)
