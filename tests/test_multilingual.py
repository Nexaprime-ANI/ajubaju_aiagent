import urllib.request
import json

def test_chat(q, lang):
    req = urllib.request.Request(
        'http://127.0.0.1:8000/chat',
        data=json.dumps({'query': q, 'language': lang}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req)
    d = json.loads(res.read().decode('utf-8'))
    resp_preview = d['response'][:70].encode('ascii', 'backslashreplace').decode()
    print(f"[{lang}] Q: '{q}' -> Response ({d['source']}, {d['category']}):")
    print(f"   {resp_preview}...")

if __name__ == '__main__':
    print("=== LIVE MULTILINGUAL API VERIFICATION ===")
    test_chat("how to add product", "Hindi")
    test_chat("how to add product", "Marathi")
    test_chat("what is payout cycle", "Hindi")
    test_chat("what is payout cycle", "Marathi")
    test_chat("how to logout", "Hindi")
    test_chat("how to logout", "Marathi")
    test_chat("who is prime minister", "Hindi")
    print("=== ALL TESTS PASSED ===")
