import re

def update_rag_engine():
    path = "backend/rag_engine.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add import
    if "from translations import translate_text, OUT_OF_SCOPE_MESSAGES, FALLBACK_MESSAGES" not in content:
        content = "from translations import translate_text, OUT_OF_SCOPE_MESSAGES, FALLBACK_MESSAGES\n" + content

    # 2. Update out of scope refusal
    out_of_scope_old = r'''if not self\.is_in_scope\(query\):
            refusal = \(
                "It is not our app related question\. Please try again\. "
                "I am the Golo Merchant AI Assistant, specialized exclusively in guiding you "
                "through the Golo web application, product listings, orders, payments, KYC verification, "
                "and store settings\. 😊"
            \)
            return \{
                "response": refusal,'''
    
    out_of_scope_new = '''if not self.is_in_scope(query):
            lang_clean = (language or "").strip().lower()
            if "marathi" in lang_clean or lang_clean == "mr" or lang_clean.startswith("mr-"):
                refusal = OUT_OF_SCOPE_MESSAGES["mr"]
            elif "hindi" in lang_clean or lang_clean == "hi" or lang_clean.startswith("hi-"):
                refusal = OUT_OF_SCOPE_MESSAGES["hi"]
            else:
                refusal = OUT_OF_SCOPE_MESSAGES["en"]
            return {
                "response": refusal,'''

    content, c1 = re.subn(out_of_scope_old, out_of_scope_new, content)
    print("Out of scope updated:", c1)

    # 3. Update deterministic RAG fallback and final fallback
    # Replace line where best_score >= 0.10 returns best_faq["answer"]
    det_old = r'''# 5\. Deterministic RAG Fallback
        if best_score >= 0\.10:
            return \{
                "response": best_faq\["answer"\],'''

    det_new = '''# 5. Deterministic RAG Fallback
        if best_score >= 0.10:
            final_ans = translate_text(best_faq["answer"], language, faq_id=best_faq["id"])
            return {
                "response": final_ans,'''

    content, c2 = re.subn(det_old, det_new, content)
    print("Deterministic RAG updated:", c2)

    # Replace fallback_msg return
    fb_old = r'''return \{
            "response": fallback_msg,
            "source": "customer_support",'''

    fb_new = '''fallback_resp = translate_text(fallback_msg, language)
        return {
            "response": fallback_resp,
            "source": "customer_support",'''

    content, c3 = re.subn(fb_old, fb_new, content)
    print("Fallback msg updated:", c3)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("backend/rag_engine.py updated successfully.")

if __name__ == "__main__":
    update_rag_engine()
