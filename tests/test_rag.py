import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from knowledge_base import FAQ_DATABASE
from rag_engine import GoloRAGEngine

rag = GoloRAGEngine(faq_database=FAQ_DATABASE)
print("Suggestions for 'what is golo':")
for s in rag.get_suggestions("what is golo", limit=5):
    print(" -", s["question"])

print("\nSuggestions for 'register':")
for s in rag.get_suggestions("register", limit=5):
    print(" -", s["question"])

print("\nTesting generate_rag_response for 'what is golo app':")
res = rag.generate_rag_response("what is golo app")
print("Source:", res["source"])
print("Response:\n", res["response"][:400])
