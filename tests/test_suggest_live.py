import urllib.request, json
for term in ['what is', 'what is golo', 'register', 'payout']:
    url = f"http://127.0.0.1:8000/suggest?q={term.replace(' ', '%20')}&limit=4"
    res = urllib.request.urlopen(url, timeout=5)
    data = json.loads(res.read().decode('utf-8'))
    print(f"=== Suggestions for: '{term}' ===")
    for s in data.get('suggestions', []):
        print(f" - {s['question']} ({s['category']})")
    print()
