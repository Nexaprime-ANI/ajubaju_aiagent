import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode('utf-8'))

def get(url):
    with urllib.request.urlopen(url, timeout=10) as res:
        return json.loads(res.read().decode('utf-8'))

print("=== 1. Autocomplete /suggest?q=register ===")
res_suggest = get("http://127.0.0.1:8000/suggest?q=register&limit=3")
print(json.dumps(res_suggest, indent=2))

print("\n=== 2. Popular FAQs /faqs/popular ===")
pop = get("http://127.0.0.1:8000/faqs/popular?limit=4")
for item in pop.get("popular", []):
    print(f" - [#{item['id']}] {item['question']} ({item['category']})")

print("\n=== 3. Query: how to register a number ===")
ans1 = post("http://127.0.0.1:8000/chat", {"query": "how to register a number", "session_id": "test_1"})
print("Source:", ans1.get("source"), "| Confidence:", ans1.get("confidence"))
print("Response:\n", ans1.get("response")[:450])

print("\n=== 4. Query: how do I log out ===")
ans2 = post("http://127.0.0.1:8000/chat", {"query": "how do I log out", "session_id": "test_2"})
print("Source:", ans2.get("source"), "| Confidence:", ans2.get("confidence"))
print("Response:\n", ans2.get("response")[:350])

print("\n=== 5. Query: what is the capital of France (Out of scope) ===")
ans3 = post("http://127.0.0.1:8000/chat", {"query": "what is the capital of France", "session_id": "test_3"})
print("Source:", ans3.get("source"), "| Needs CS:", ans3.get("needs_customer_service"))
print("Response:\n", ans3.get("response"))

print("\n=== 6. Query: customer support contact info ===")
ans4 = post("http://127.0.0.1:8000/chat", {"query": "how to contact golo customer care and support", "session_id": "test_4"})
print("Source:", ans4.get("source"), "| Needs CS:", ans4.get("needs_customer_service"))
print("Response:\n", ans4.get("response")[:400])
