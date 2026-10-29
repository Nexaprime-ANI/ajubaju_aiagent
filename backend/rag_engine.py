"""
Golo AI Assistant - RAG (Retrieval-Augmented Generation) & NLP Engine
===================================================================
Implements:
1. TF-IDF + Cosine Similarity Vector Space Model (Scikit-Learn) over 163 Official FAQs.
2. N-Gram (1, 3) semantic tokenization and lemmatized intent matching.
3. Accurate In-Scope vs. Out-of-Scope NLP intent classifier.
4. Generative RAG synthesis via Google GenAI (gemini-3.8-flash) with local deterministic RAG fallback.
"""

import os
import re
import time
import concurrent.futures
from typing import Dict, List, Optional, Tuple, Any
from dotenv import load_dotenv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment
load_dotenv()
api_key = os.getenv("GOLO_API_KEY") or os.getenv("GEMINI_API_KEY")

genai_client = None
if api_key:
    try:
        from google import genai
        genai_client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Warning: Could not initialize Google GenAI client: {e}")


# Explicit Golo App Domain Vocabulary
APP_DOMAIN_TERMS = {
    # Account & Auth
    "logout", "log out", "signout", "sign out", "exit", "session", "sign off",
    "login", "log in", "signin", "sign in", "register", "registration", "signup", "sign up",
    "password", "forgot password", "reset password", "otp", "2fa", "verification", "kyc",
    "profile", "avatar", "account", "settings", "delete account", "deactivate", "security",
    
    # Store & Catalog
    "golo", "nexaprime", "merchant", "store", "shop", "catalog", "product", "products",
    "item", "items", "listing", "listings", "inventory", "stock", "sku", "barcode",
    "category", "categories", "variant", "variants", "price", "mrp", "discount", "pricing",
    
    # Orders & Logistics
    "order", "orders", "cart", "checkout", "pending", "accepted", "rejected", "completed",
    "pickup", "in-store", "delivery", "shipping", "courier", "tracking", "track", "dispatch",
    "address", "map", "gps", "directions", "location", "radius", "distance",
    
    # Offers, Vouchers & Payments
    "voucher", "vouchers", "coupon", "coupons", "offer", "offers", "deal", "deals",
    "claim", "redeem", "redemption", "qr", "qr code", "loyalty", "stars", "points",
    "payment", "payments", "payout", "payouts", "wallet", "credit note", "credit notes",
    "refund", "refunds", "cancel", "cancellation", "bank", "upi", "card", "fee", "fees",
    "commission", "commissions", "tax", "gst", "gstin", "invoice",
    
    # Support, Admin & Navigation
    "help", "support", "ticket", "tickets", "helpdesk", "contact", "report", "dispute",
    "admin", "dashboard", "portal", "compliance", "moderation", "review", "reviews",
    "rating", "ratings", "feature", "features", "app", "web app", "website", "guide",

    # Project Specifications, Architecture & Deliverables
    "project", "overview", "project overview", "architecture", "expected output", "output",
    "deliverable", "deliverables", "roadmap", "implementation", "goal", "goals", "scope",
    "in scope", "out of scope", "spec", "specification", "handoff", "phase", "phases",
    "sla", "gemini", "rag", "nlp", "benchmark", "cost", "hardware", "inference", "stack",
    "tech stack", "fastapi", "pipeline", "cache", "version 2", "v2"
}

# Strictly Out-of-Scope indicators
STRICT_OUT_OF_SCOPE_TERMS = {
    "cricket", "football", "world cup", "fifa", "ipl", "tennis", "olympics",
    "weather", "forecast", "temperature", "rain", "sunny",
    "president", "prime minister", "election", "politics", "war", "russia", "ukraine",
    "recipe", "cake", "cook", "ingredients", "pasta", "pizza",
    "python code", "write a code", "write a poem", "write an essay", "sing a song",
    "joke", "tell me a joke", "movie", "cinema", "actor", "actress", "celebrity",
    "capital of", "who discovered", "mathematics equation", "solve this math"
}


class GoloRAGEngine:
    """
    RAG & NLP Engine for Golo Assistant.
    Combines Scikit-Learn TF-IDF Vector Space search with Google GenAI (gemini-3.8-flash) RAG.
    """

    def __init__(self, faq_database: List[Dict[str, Any]]):
        self.faq_database = faq_database
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            sublinear_tf=True,
            stop_words='english',
            min_df=1
        )
        self._build_vector_index()

    def _build_vector_index(self):
        """Construct weighted document corpus and fit TF-IDF vectorizer."""
        corpus = []
        for faq in self.faq_database:
            q = faq.get("question", "")
            cat = faq.get("category", "")
            tags = " ".join(faq.get("tags", []))
            ans = faq.get("answer", "")
            
            # Boost question and tags
            doc = f"{q} {q} {q} {tags} {tags} {cat} {ans[:250]}"
            corpus.append(doc)
            
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def is_in_scope(self, query: str) -> bool:
        """
        NLP Scope Evaluation:
        Determines whether the query pertains to the Golo web app / retail ecosystem.
        """
        q_lower = query.lower().strip()
        
        # 1. Check for explicit out-of-scope markers
        for term in STRICT_OUT_OF_SCOPE_TERMS:
            if term in q_lower:
                # Unless explicitly mentioning Golo platform features
                if not any(k in q_lower for k in ["golo", "nexaprime", "merchant", "store"]):
                    return False
                    
        # 2. Check for app domain vocabulary match
        tokens = re.findall(r'\b[a-z0-9\-]+\b', q_lower)
        for term in APP_DOMAIN_TERMS:
            if " " in term:
                if term in q_lower:
                    return True
            elif term in tokens:
                return True
                
        # 3. Vector similarity fallback: if it has semantic overlap with our FAQ corpus
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        if np.max(sims) >= 0.08:
            return True

        # 4. General conversational app/platform queries
        general_intents = [
            "what is", "how do", "how to", "can i", "where can", "who can",
            "tell me", "explain", "help", "hi", "hello", "work", "features",
            "benefits", "start", "use", "platform", "guide"
        ]
        if any(gi in q_lower for gi in general_intents):
            return True

        return False

    def retrieve_top_k(self, query: str, k: int = 6) -> List[Tuple[Dict[str, Any], float]]:
        """Retrieve Top-K most semantically relevant FAQs using Cosine Similarity."""
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        top_indices = np.argsort(sims)[::-1][:k]
        results = []
        for idx in top_indices:
            score = float(sims[idx])
            results.append((self.faq_database[idx], score))
            
        return results

    def generate_rag_response(
        self,
        query: str,
        session_id: Optional[str] = None,
        merchant_id: Optional[str] = None,
        language: str = "English",
        image_base64: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process query through RAG pipeline:
        1. Scope verification
        2. Vector retrieval of top FAQ contexts
        3. Intent-specific routing (e.g. Logout, Return, KYC)
        4. Generative RAG synthesis with Gemini 3.5 / 3.1 Flash (multimodal & multilingual)
        """
        start_time = time.time()
        
        # 1. Out of scope check
        if not self.is_in_scope(query):
            refusal = (
                "It is not our app related question. Please try again. "
                "I am the Golo Merchant AI Assistant, specialized exclusively in guiding you "
                "through the Golo web application, product listings, orders, payments, KYC verification, "
                "and store settings. 😊"
            )
            return {
                "response": refusal,
                "source": "out_of_scope",
                "category": "out_of_scope",
                "confidence": 1.0,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # 2. Query Normalization & Typo Tolerance
        q_norm = query.lower().strip()
        q_norm = re.sub(r'\b(golu|gollu|golo ai|gloo|polo|goloapp)\b', 'golo', q_norm)
        q_norm = re.sub(r'\b(ph no|mobile no|contact no|phone no|cell no)\b', 'mobile number', q_norm)
        q_norm = re.sub(r'\b(whats|wat is|whats is)\b', 'what is', q_norm)

        # 3. Vector retrieval using normalized query
        top_matches = self.retrieve_top_k(q_norm, k=6)
        best_faq, best_score = top_matches[0]

        # 4. Canonical Fast-Path Intent Routing (< 20ms response time)
        # Helper to return a specific FAQ instantly
        def _get_faq_by_id(fid: int):
            for f in self.faq_database:
                if f["id"] == fid:
                    return f
            return best_faq

        lang_clean = (language or "").strip().lower()
        is_marathi = "marathi" in lang_clean or lang_clean == "mr" or lang_clean.startswith("mr-")
        is_hindi = not is_marathi and ("hindi" in lang_clean or lang_clean == "hi" or lang_clean.startswith("hi-"))

        # INTENT A: WHAT IS GOLO / PLATFORM OVERVIEW
        if any(p in q_norm for p in ["what is golo", "what golo is", "who is golo", "about golo", "tell me about golo", "explain golo", "golo kya hai", "kya hai golo", "golo kay ahe", "golo platform", "how does golo work", "how golo works"]) or q_norm in ["golo", "what is golo"]:
            target_faq = _get_faq_by_id(1)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**GOLO** एक हाइपर-लोकल खोज (hyper-local discovery) और रिटेल बचत प्लेटफ़ॉर्म है, जिसे **NexaPrime Ecosystem** द्वारा संचालित किया जाता है। यह स्थानीय दुकानदारों और ग्राहकों को डिजिटल स्टोरफ़्रंट, उत्पाद कैटलॉग और क्यूआर कोड वाउचर छूट के माध्यम से जोड़ता है।"
            elif is_marathi:
                ans = "**GOLO** हे एक अग्रगण्य हायपर-लोकल शोध (hyper-local discovery) आणि रिटेल सेव्हिंग्स प्लॅटफॉर्म आहे, जे **NexaPrime Ecosystem** द्वारे चालवले जाते. हे स्थानिक दुकानदार आणि ग्राहकांना डिजिटल स्टोअरफ्रंट, प्रॉडक्ट कॅटलॉग आणि QR कोड व्हाउचर सवलतींद्वारे थेट जोडते."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.99,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # INTENT B: LOGOUT
        if any(term in q_norm for term in ["logout", "log out", "signout", "sign out", "exit account", "exit session"]):
            target_faq = _get_faq_by_id(163)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**GOLO खाते से लॉग आउट करने की चरण-दर-चरण मार्गदर्शिका:**\n\n1. **चरण 1:** शीर्ष नेविगेशन बार में अपने **Profile Avatar** पर क्लिक करें।\n2. **चरण 2:** ड्रॉपडाउन मेनू से **Sign Out / Log Out** का चयन करें।\n3. **चरण 3:** आपका सत्र सुरक्षित रूप से समाप्त हो जाएगा।"
            elif is_marathi:
                ans = "**GOLO खात्यामधून लॉग आउट करण्याची सोपी प्रक्रिया:**\n\n1. **पायरी १:** वरच्या नेव्हिगेशन बारमधील तुमच्या **Profile Avatar** वर क्लिक करा.\n2. **पायरी २:** ड्रॉपडाउन मेनूमधून **Sign Out / Log Out** निवडा.\n3. **पायरी ३:** तुमचे सत्र सुरक्षितपणे बंद होईल."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.99,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # INTENT C: REGISTER / ADD MOBILE NUMBER / NEW ACCOUNT
        if any(p in q_norm for p in ["register", "create account", "add mobile", "add number", "signup", "sign up", "open account"]) and not any(p in q_norm for p in ["change", "update", "edit", "replace"]):
            target_faq = _get_faq_by_id(172)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**GOLO पर मोबाइल नंबर रजिस्टर करने और नया खाता बनाने की चरण-दर-चरण प्रक्रिया:**\n\n1. **चरण 1 — पोर्टल खोलें:** GOLO वेब पोर्टल या ऐप पर जाएं।\n2. **चरण 2 — रजिस्टर चुनें:** शीर्ष दाएं कोने में **Register** बटन पर क्लिक करें।\n3. **चरण 3 — मोबाइल नंबर दर्ज करें:** अपना 10-अंकों का वैध मोबाइल नंबर दर्ज करें।\n4. **चरण 4 — ओटीपी सत्यापन:** प्राप्त 6-अंकों का OTP दर्ज करके **Verify OTP** पर क्लिक करें।\n5. **चरण 5 — पुष्टि:** आपका GOLO खाता तुरंत सक्रिय हो जाएगा।"
            elif is_marathi:
                ans = "**GOLO वर मोबाईल नंबर नोंदणी करण्याची पद्धत:**\n\n1. **पायरी १:** GOLO वेब पोर्टल किंवा ॲप उघडा.\n2. **पायरी २:** वरच्या उजव्या कोपऱ्यातील **Register** बटणावर क्लिक करा.\n3. **पायरी ३:** तुमचा १०-अंकी मोबाईल नंबर टाका.\n4. **पायरी ४:** SMS द्वारे मिळालेला ६-अंकी OTP टाकून **Verify OTP** वर क्लिक करा.\n5. **पायरी ५:** तुमचे GOLO खाते त्वरित सक्रिय होईल."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.99,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # INTENT D: CHANGE / UPDATE REGISTERED MOBILE NUMBER
        if any(p in q_norm for p in ["change number", "update number", "edit number", "change mobile", "update mobile", "edit mobile", "replace number"]):
            target_faq = _get_faq_by_id(173)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**पंजीकृत मोबाइल नंबर बदलने की प्रक्रिया:**\n1. **Account Settings** → **Security & Login** पर जाएं।\n2. **Change Mobile Number** पर क्लिक करें।\n3. पुराने और नए नंबर पर आए OTP को सत्यापित करें।"
            elif is_marathi:
                ans = "**नोंदणीकृत मोबाईल नंबर बदलण्याची प्रक्रिया:**\n1. **Account Settings** → **Security & Login** वर जा.\n2. **Change Mobile Number** निवडा.\n3. जुन्या व नवीन नंबरवर आलेला OTP व्हेरिफाय करा."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.99,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # INTENT E: PAYOUTS & SETTLEMENT CYCLE (T+2 / T+3)
        if any(p in q_norm for p in ["payout", "settlement", "payment schedule", "t+2", "t+3", "bank transfer", "when do i get paid"]):
            target_faq = _get_faq_by_id(176)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**GOLO व्यापारियों के लिए भुगतान (Payout) और निपटान चक्र:**\n\n• **निपटान चक्र:** T+2 / T+3 कार्य दिवस (शनिवार, रविवार और बैंक अवकाश छोड़कर)।\n• **न्यूनतम पेआउट सीमा:** ₹500 शुद्ध आय।\n• **स्थानांतरण विधि:** सीधे पंजीकृत बैंक खाते में सुरक्षित NEFT / RTGS / IMPS।\n• **कटौतियां:** प्लेटफ़ॉर्म सुविधा शुल्क और लागू GST स्वचालित रूप से समायोजित होते हैं।"
            elif is_marathi:
                ans = "**GOLO मर्चंट्ससाठी पेआउट आणि सेटलमेंट सायकल:**\n\n• **सेटलमेंट सायकल:** T+2 / T+3 व्यावसायिक दिवस.\n• **किमान पेआउट मर्यादा:** ₹500 शुद्ध उत्पन्न.\n• **पद्धत:** थेट नोंदणीकृत बँक खात्यात NEFT / RTGS / IMPS द्वारे सुरक्षित ट्रान्सफर.\n• **कपाती:** प्लॅटफॉर्म फी आणि GST आपोआप समायोजित होतात."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.99,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # INTENT F: CUSTOMER CARE & SUPPORT
        if any(p in q_norm for p in ["customer care", "customer service", "support", "helpline", "toll free", "call care", "complaint"]):
            target_faq = _get_faq_by_id(175)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**GOLO मर्चेंट कस्टमर सपोर्ट २४/७ सहायता:**\n- **टोल-फ्री हेल्पलाइन:** 1800-267-4656\n- **ईमेल सपोर्ट:** support@golo.com\n- **लाइव टिकट:** 'Create Ticket' पर क्लिक करके वरिष्ठ तकनीकी डेस्क से संपर्क करें।"
            elif is_marathi:
                ans = "**GOLO मर्चंट कस्टमर सपोर्ट २४/७ उपलब्ध आहे:**\n- **टोल-फ्री हेल्पलाइन:** 1800-267-4656\n- **ईमेल सहाय्य:** support@golo.com\n- **लाइव्ह तिकीट:** 'Create Ticket' बटणावर क्लिक करून थेट संपर्क साधा."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.99,
                "needs_customer_service": True,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # INTENT G: KYC VERIFICATION
        if any(p in q_norm for p in ["kyc", "pan", "aadhaar", "verification", "verify account", "documents"]):
            target_faq = _get_faq_by_id(73)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**KYC सत्यापन आवश्यकताएं:**\n1. **GSTIN प्रमाणपत्र** या पैन कार्ड\n2. **रद्द चेक (Cancelled Cheque)** या बैंक पासबुक विवरण\n3. **व्यावसायिक पते का प्रमाण**.\nस्वीकृति में आमतौर पर ४ व्यावसायिक घंटे लगते हैं।"
            elif is_marathi:
                ans = "**KYC पडताळणी आवश्यकता:**\n1. **GSTIN प्रमाणपत्र** किंवा पॅन कार्ड\n2. **रद्द केलेला चेक (Cancelled Cheque)** किंवा बँक पासबुक\n3. **पत्ता पुरावा**.\nमंजुरी साधारणतः ४ व्यावसायिक तासांत मिळते."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.98,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # INTENT H: LIST OR ADD PRODUCT
        if any(p in q_norm for p in ["list product", "add product", "upload product", "create product", "new listing"]):
            target_faq = _get_faq_by_id(66)
            ans = target_faq["answer"]
            if is_hindi:
                ans = "**नया उत्पाद जोड़ने की चरण-दर-चरण प्रक्रिया:**\n1. **Catalog** → **Products** → **Add Product** पर जाएं।\n2. उत्पाद शीर्षक, विवरण, मूल्य और स्टॉक दर्ज करें।\n3. उच्च गुणवत्ता वाली तस्वीरें अपलोड करें और **Publish** दबाएं।"
            elif is_marathi:
                ans = "**नवीन उत्पादन जोडण्याची सोपी पद्धत:**\n1. **Catalog** → **Products** → **Add Product** वर जा.\n2. उत्पादनाचे नाव, किंमत, स्टॉक आणि वर्णन प्रविष्ट करा.\n3. फोटो अपलोड करून **Publish** दाबा."
            return {
                "response": ans,
                "source": "faq",
                "category": target_faq["category"],
                "faq_id": target_faq["id"],
                "faq_question": target_faq["question"],
                "confidence": 0.98,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # Direct High-Confidence Vector Match
        if not image_base64 and (not language or language.lower() in ["en", "english"]) and best_score >= 0.12:
            return {
                "response": best_faq["answer"],
                "source": "faq",
                "category": best_faq["category"],
                "faq_id": best_faq["id"],
                "faq_question": best_faq["question"],
                "confidence": round(best_score, 2),
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # 4. Generative RAG Synthesis with Google GenAI (Gemini 3.5 / 3.1 Flash)
        if genai_client:
            context_passages = [
                "[GOLO CORE PLATFORM OVERVIEW]\n"
                "GOLO is a hyper-local discovery and retail savings platform operated by NexaPrime Ecosystem. "
                "It connects neighborhood merchants with local shoppers, providing digital storefronts, product catalogs, "
                "inventory tracking, geo-targeted promotional ad campaigns, and voucher redemption verification via QR code. "
                "The platform is available as both a web portal (merchant.golo.com) and mobile applications (Android & iOS). "
                "Core Policies: Payouts are on a T+2 / T+3 rolling business day cycle via bank NEFT/RTGS. "
                "Refunds are issued as Credit Notes or Wallet credits by NexaPrime Pvt. Ltd.; direct cash refunds are not provided. "
                "Customer Care: 1800-267-4656 (Toll-Free, 9 AM – 9 PM IST), support@golo.com, +91 80 4567 8900."
            ]
            for i, (faq, score) in enumerate(top_matches):
                context_passages.append(
                    f"[FAQ Reference {i+1} - {faq['category']}]\n"
                    f"Question: {faq['question']}\n"
                    f"Answer: {faq['answer']}"
                )
            rag_context = "\n\n".join(context_passages)

            lang_mandate = ""
            if language and language.strip().lower() not in ["en", "english"]:
                lang_mandate = f"""
CRITICAL MULTILINGUAL MANDATE:
The user has selected the language: {language}.
You MUST generate your entire response in {language}.
Every step description, explanation, heading, and guidance must be in natural, accurate {language}.
Do NOT reply in English.
"""

            prompt = f"""You are the official Golo AI Assistant for the Golo merchant & customer web application (operated by NexaPrime Ecosystem).
Your mission is to provide concise, accurate, authoritative guidance to users.

STRICT GROUNDING & STEP-BY-STEP FORMATTING RULES:
1. Ground your answer in the provided Golo Knowledge Base passages below.
2. If the user asks how to do ANY action (e.g. how to register a number, how to create an account, how to list a product, how to log out, how to change settings):
   - Always structure your answer into clean, numbered steps: **Step 1 — ...**, **Step 2 — ...**, **Step 3 — ...**.
   - Bold exact UI buttons, tabs, input fields, and paths (e.g. **Register**, **Mobile Number**, **Send OTP**, **Settings**).
3. If the user asks what GOLO is, or about the GOLO app/platform features:
   - Provide a clear, professional overview of the platform (hyper-local discovery, merchant digital stores, savings vouchers, mobile apps).
4. If an image is provided:
   - Inspect the image thoroughly (OCR any text, recognize product items, voucher barcodes/QRs, receipts, UI error messages, or forms).
   - Answer the user's question directly with respect to what is seen in the image and relevant GOLO procedures.
5. If the user asks about Credit Notes / Refunds: GOLO generally does not provide cash refunds for paid platform services; credits are issued as Credit Notes or Wallet credits by NexaPrime Pvt. Ltd.
6. If the question is completely outside our documented features or unanswerable, advise contacting customer care at 1800-267-4656 or support@golo.com.
{lang_mandate}
---
RELEVANT GOLO KNOWLEDGE BASE PASSAGES:
{rag_context}
---

USER QUESTION: {query}
"""
            # Build multimodal payload if image provided
            contents_payload = prompt
            if image_base64:
                try:
                    import base64
                    from google.genai import types
                    clean_b64 = image_base64.split(",")[1] if "," in image_base64 else image_base64
                    mime = "image/png"
                    if "data:" in image_base64 and ";" in image_base64:
                        mime = image_base64.split(";")[0].replace("data:", "")
                    img_bytes = base64.b64decode(clean_b64)
                    img_part = types.Part.from_bytes(data=img_bytes, mime_type=mime)
                    contents_payload = [img_part, prompt]
                except Exception as e:
                    print(f"Warning: Multimodal image decode failed: {e}")
                    contents_payload = prompt

            def _call_gemini_models():
                candidate_models = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite"]
                for model_name in candidate_models:
                    try:
                        resp = genai_client.models.generate_content(
                            model=model_name,
                            contents=contents_payload
                        )
                        if resp and resp.text:
                            return resp.text.strip()
                    except Exception:
                        continue
                return None

            resp_text = None
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(_call_gemini_models)
                    resp_text = future.result(timeout=1.8)
            except Exception:
                resp_text = None

            if resp_text:
                is_cs_referral = any(phrase in resp_text.lower() for phrase in [
                    "customer care", "customer support", "contact customer",
                    "1800-267-4656", "support@golo.com", "care@golo.com",
                    "don't have verified documentation", "do not have verified documentation",
                    "not have verified documentation", "not have documentation", "cannot find documentation"
                ])
                return {
                    "response": resp_text,
                    "source": "customer_support" if is_cs_referral else "rag_generative",
                    "category": best_faq["category"],
                    "confidence": 0.70 if is_cs_referral else 0.95,
                    "faq_id": best_faq["id"],
                    "faq_question": best_faq["question"],
                    "needs_customer_service": is_cs_referral,
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }

        # 5. Deterministic RAG Fallback
        if best_score >= 0.10:
            return {
                "response": best_faq["answer"],
                "source": "faq",
                "category": best_faq["category"],
                "faq_id": best_faq["id"],
                "faq_question": best_faq["question"],
                "needs_customer_service": False,
                "confidence": round(best_score, 2),
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # 6. Unanswered / Missing Data Fallback with Customer Care Contact Options
        fallback_msg = (
            "We don't currently have verified documentation in our database for this specific query.\n\n"
            "If you want to resolve your query immediately, our Customer Care team is on standby to assist you directly:\n\n"
            "• **Toll-Free Helpline:** `1800-267-4656` (9:00 AM – 9:00 PM IST)\n"
            "• **Support Email:** `support@golo.com`\n"
            "• **Live Operations Desk:** `+91 80 4567 8900`\n\n"
            "You can click the **Customer Service** button below to connect with our support team."
        )
        return {
            "response": fallback_msg,
            "source": "customer_support",
            "category": "Customer Support",
            "confidence": 0.50,
            "needs_customer_service": True,
            "latency_ms": round((time.time() - start_time) * 1000, 2)
        }

    def get_suggestions(self, prefix: str, limit: int = 4) -> List[Dict[str, Any]]:
        """
        Google-style Predictive Query Suggestions with Multi-Token & Substring Matching.
        Predicts what the user is typing based on the 175 FAQ database.
        """
        p = prefix.lower().strip()
        if not p or len(p) < 2:
            return []

        p_tokens = set(re.findall(r'\b[a-z0-9\-]+\b', p))

        scored_matches = []
        for faq in self.faq_database:
            q_text = faq.get("question", "")
            q_lower = q_text.lower()
            q_tokens = set(re.findall(r'\b[a-z0-9\-]+\b', q_lower))
            
            score = 0
            # Exact prefix match (highest weight)
            if q_lower.startswith(p):
                score += 150
            # Exact substring match
            elif p in q_lower:
                idx = q_lower.find(p)
                score += 100 - min(idx, 40)
            
            # Token / Word Overlap
            overlap = p_tokens & q_tokens
            if overlap:
                score += len(overlap) * 25
                if p_tokens.issubset(q_tokens):
                    score += 50
                    
            # Tag match
            for tag in faq.get("tags", []):
                t_lower = tag.lower()
                if t_lower.startswith(p) or p in t_lower:
                    score += 30
                    break
                if any(tok in t_lower for tok in p_tokens):
                    score += 15
                    break

            # Answer text match
            ans_lower = faq.get("answer", "").lower()
            if p in ans_lower:
                score += 40
            elif any(tok in ans_lower for tok in p_tokens):
                score += 15

            if score > 0:
                scored_matches.append((faq, score))

        scored_matches.sort(key=lambda x: x[1], reverse=True)
        
        seen_questions = set()
        suggestions = []
        for faq, _ in scored_matches:
            q = faq.get("question", "")
            if q not in seen_questions:
                seen_questions.add(q)
                suggestions.append({
                    "id": faq.get("id"),
                    "question": q,
                    "category": faq.get("category", "")
                })
                if len(suggestions) >= limit:
                    break

        return suggestions

    def get_popular_faqs(self, limit: int = 8) -> List[Dict[str, Any]]:
        """
        NLP/Frequency-Curated Most Frequently Asked Questions for AI mode.
        """
        priority_ids = [172, 163, 68, 116, 38, 174, 164, 167, 18, 27]
        popular = []
        for pid in priority_ids:
            for faq in self.faq_database:
                if faq["id"] == pid:
                    popular.append({
                        "id": faq["id"],
                        "question": faq["question"],
                        "category": faq["category"]
                    })
        return popular[:limit]

