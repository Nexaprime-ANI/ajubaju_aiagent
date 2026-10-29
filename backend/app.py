"""
Golo AI Assistant - FastAPI Backend Server
==========================================
REST API server for the Golo Merchant AI Assistant.
Provides endpoints for chat, FAQ retrieval, and health checks.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai_engine import GoloAIEngine

# ─── Initialize FastAPI App ─────────────────────────────
app = FastAPI(
    title="Golo AI Assistant API",
    description="Backend API for the Golo Merchant AI Assistant",
    version="1.0.0",
)

# ─── CORS Configuration ─────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Initialize AI Engine ─────────────────────────────
ai_engine = GoloAIEngine()


# ─── Request/Response Models ─────────────────────────────
class ChatRequest(BaseModel):
    query: str = Field(..., description="The merchant's question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    merchant_id: Optional[str] = Field(None, description="Unique Merchant ID (e.g. MRC-8821) for tracking & rate limits")
    language: Optional[str] = Field("English", description="Target language requested by user")
    image_base64: Optional[str] = Field(None, description="Optional image base64 data for visual analysis")


class ChatResponse(BaseModel):
    response: str
    source: str
    category: str
    confidence: float
    timestamp: str
    session_id: str
    latency_ms: float
    merchant_id: Optional[str] = None
    faq_id: Optional[int] = None
    faq_question: Optional[str] = None
    needs_customer_service: Optional[bool] = False


class RatingRequest(BaseModel):
    session_id: str
    rating: int = Field(..., ge=1, le=5, description="1 to 5 star rating")
    comment: Optional[str] = None
    merchant_id: Optional[str] = None


class EscalationRequest(BaseModel):
    session_id: str
    reason: str
    details: Optional[str] = None
    merchant_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    faq_count: int
    categories: list


# ─── API Endpoints ─────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Golo AI Assistant API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "faq_count": len(ai_engine.get_all_faqs()),
        "categories": ai_engine.get_categories(),
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Process a merchant query and return AI response.
    
    Accepts:
    - query: User natural language input
    - session_id: Conversation session UUID
    - merchant_id: (Optional) Merchant identifier for rate limits & telemetry
    """
    result = ai_engine.process_query(
        query=request.query,
        session_id=request.session_id,
        merchant_id=request.merchant_id,
        language=request.language or "English",
        image_base64=request.image_base64
    )
    if "merchant_id" not in result:
        result["merchant_id"] = request.merchant_id
    return result


@app.post("/ratings", tags=["Feedback"])
async def submit_rating(req: RatingRequest):
    """Submit post-conversation rating (1-5 stars) linked to session and merchant ID."""
    return ai_engine.record_rating(
        session_id=req.session_id,
        rating=req.rating,
        comment=req.comment,
        merchant_id=req.merchant_id
    )


@app.post("/escalate", tags=["Support"])
async def escalate_to_human(req: EscalationRequest):
    """Escalate a merchant issue to human support and generate a ticket."""
    return ai_engine.create_escalation(
        session_id=req.session_id,
        reason=req.reason,
        details=req.details,
        merchant_id=req.merchant_id
    )


@app.get("/merchant/{merchant_id}/usage", tags=["Merchant"])
async def get_merchant_rate_limits(merchant_id: str):
    """Get active query counts and rate limit quotas for a specific merchant ID."""
    return ai_engine.get_merchant_usage(merchant_id)


@app.get("/welcome", tags=["Chat"])
async def get_welcome():
    """Get a welcome message for new chat sessions."""
    return {
        "message": ai_engine.get_welcome_message(),
        "session_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/faqs", tags=["FAQ"])
async def get_all_faqs():
    """Get all FAQ entries."""
    faqs = ai_engine.get_all_faqs()
    return {
        "count": len(faqs),
        "faqs": faqs,
    }


@app.get("/faqs/categories", tags=["FAQ"])
async def get_faq_categories():
    """Get all FAQ categories."""
    return {
        "categories": ai_engine.get_categories(),
    }


@app.get("/faqs/popular", tags=["FAQ"])
async def get_popular_faqs(limit: int = 8):
    """
    Get top frequently asked questions ranked by NLP and user priority for AI mode.
    """
    popular = ai_engine.get_popular_faqs(limit=limit)
    return {
        "count": len(popular),
        "popular": popular
    }


@app.get("/faqs/{category}", tags=["FAQ"])
async def get_faqs_by_category(category: str):
    """Get FAQs filtered by category."""
    faqs = ai_engine.get_faqs_by_category(category)
    if not faqs:
        raise HTTPException(status_code=404, detail=f"No FAQs found for category: {category}")
    return {
        "category": category,
        "count": len(faqs),
        "faqs": faqs,
    }


@app.get("/session/{session_id}", tags=["Session"])
async def get_session_history(session_id: str):
    """Get conversation history for a session."""
    history = ai_engine.get_session_history(session_id)
    return {
        "session_id": session_id,
        "message_count": len(history),
        "history": history,
    }


@app.delete("/session/{session_id}", tags=["Session"])
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    ai_engine.clear_session(session_id)
    return {
        "status": "cleared",
        "session_id": session_id,
    }


@app.get("/search", tags=["Search"])
async def semantic_search(q: str, limit: int = 5):
    """Semantic search across all FAQs and project specifications."""
    if not q or not q.strip():
        return {"query": "", "results": []}
    
    # Use RAG vector search to find best matches
    rag = ai_engine.rag_engine
    q_vec = rag.vectorizer.transform([q.lower()])
    sims = (q_vec * rag.tfidf_matrix.T).toarray()[0]
    
    top_indices = sims.argsort()[::-1][:limit]
    results = []
    for idx in top_indices:
        score = float(sims[idx])
        if score > 0.05:
            faq = rag.faq_database[idx]
            results.append({
                "id": faq.get("id"),
                "question": faq.get("question"),
                "answer": faq.get("answer"),
                "category": faq.get("category"),
                "tags": faq.get("tags", []),
                "relevance_score": round(score, 3)
            })
            
    return {
        "query": q,
        "total_matches": len(results),
        "results": results
    }


@app.get("/suggest", tags=["Search"])
async def query_suggestions(q: str = "", limit: int = 4):
    """
    Google-style predictive query autocomplete suggestions.
    Predicts what the user is typing based on 175 FAQs in the database.
    """
    if not q or len(q.strip()) < 2:
        return {"query": q, "suggestions": []}
    suggestions = ai_engine.get_suggestions(q.strip(), limit=limit)
    return {
        "query": q,
        "count": len(suggestions),
        "suggestions": suggestions
    }






@app.get("/project/overview", tags=["Project"])
async def get_project_overview():
    """Structured project overview, goals, architecture, and roadmap for demo."""
    return {
        "project_name": "Golo AI Assistant",
        "ecosystem": "NexaPrime Enterprise Platform",
        "version": "2.0 (September 2026)",
        "business_problem": "High merchant support volume, 24/7 availability gap, onboarding friction, and support cost scalability.",
        "goals": {
            "G1": "Instant Query Resolution (80%+ automated resolution)",
            "G2": "24/7 Continuous Availability without shift windows",
            "G3": "Accelerate merchant onboarding by 50%",
            "G4": "Reduce inbound human tickets by 60% within 3 months",
            "G5": "Graceful multi-tier degradation (Gemini -> Groq -> Local RAG)",
            "G6": "Scalable architecture supporting 10,000+ concurrent sessions"
        },
        "expected_outputs": [
            "Modern Dual-Section Search & Reasoning UI",
            "Dedicated Conversational Assistant Workspace",
            "Dual-Path Grounded Knowledge Resolution Engine (<50ms FAQ, <1.8s RAG)",
            "Multimodal Image & Document Inspection",
            "Web Speech API Voice Recognition",
            "Strict Out-of-Scope Domain Guardrails & PII Redaction"
        ],
        "architecture_layers": [
            "Layer 1: HTML5/CSS3/Vanilla JS UI Single Page Application",
            "Layer 2: FastAPI Gateway with CORS & Rate Limiting",
            "Layer 3: L1 In-Memory Cache for Sub-50ms FAQ Resolution",
            "Layer 4: TF-IDF N-gram (1,3) Vector Space Model",
            "Layer 5: Google Gemini 3 Flash / Flash-Lite Reasoning Engine",
            "Layer 6: Safety, Grounding Verification & Delivery"
        ],
        "roadmap_phases": [
            {"phase": "Phase 0", "title": "Environment Provisioning & API Setup", "status": "Completed"},
            {"phase": "Phase 1", "title": "Foundation & Content Ingestion (163 FAQs)", "status": "Completed"},
            {"phase": "Phase 2", "title": "Core AI Engine & Dual-Path Resolution", "status": "Completed"},
            {"phase": "Phase 3", "title": "Security Guardrails & PII Protection", "status": "Completed"},
            {"phase": "Phase 4", "title": "Voice, Multimodal & Mascot Polish", "status": "Completed"},
            {"phase": "Phase 5", "title": "API Integration & SLA Benchmarking", "status": "Completed"},
            {"phase": "Phase 6", "title": "Testing & Load Verification", "status": "Completed"},
            {"phase": "Phase 7", "title": "Version 2 Launch & Live Prototype", "status": "Active / Live"}
        ],
        "total_faqs_grounded": len(ai_engine.get_all_faqs())
    }


@app.get("/analytics/metrics", tags=["Analytics"])
async def get_analytics_metrics():
    """Live demo store metrics for Intelligent Analysis view."""
    return {
        "merchant_name": "Metro Retail Hub #402",
        "merchant_id": "MRC-78921",
        "gross_sales_mtd": 125000,
        "total_orders": 248,
        "new_customers": 156,
        "order_breakdown": {
            "delivered": 68,
            "processing": 20,
            "pending": 12
        },
        "sales_growth_pct": 32,
        "inventory_alerts": [
            {"sku": "SKU-9921", "name": "Wireless Noise-Canceling Earbuds", "stock_left": 4, "status": "Low Stock"},
            {"sku": "SKU-4412", "name": "Organic Cotton Crew T-Shirt (M)", "stock_left": 2, "status": "Critical"},
            {"sku": "SKU-1109", "name": "Ceramic Matte Coffee Mug", "stock_left": 45, "status": "Optimal"}
        ],
        "ai_resolution_rate": "84.6%",
        "average_response_time_ms": 142
    }


@app.post("/multimodal/analyze", tags=["Multimodal"])
async def analyze_multimodal_file(file_name: str, query: Optional[str] = None):
    """Simulated multimodal OCR and visual inspection for merchant documents & photos."""
    name_lower = file_name.lower()
    
    if "gst" in name_lower or "tax" in name_lower or "cert" in name_lower:
        return {
            "file_name": file_name,
            "document_type": "GST Registration Certificate (REG-06)",
            "extracted_fields": {
                "gstin": "27AABCU9603R1ZX",
                "legal_name": "METRO RETAIL SOLUTIONS PVT LTD",
                "trade_name": "Golo Mart Express",
                "verification_status": "Valid & Verified",
                "taxpayer_type": "Regular",
                "date_of_liability": "01/04/2024"
            },
            "ai_insights": "The GST certificate is valid and matches merchant legal identity. KYC tier 2 status approved.",
            "confidence": 0.98
        }
    elif "receipt" in name_lower or "invoice" in name_lower or "bill" in name_lower:
        return {
            "file_name": file_name,
            "document_type": "Store Purchase Invoice / Receipt",
            "extracted_fields": {
                "invoice_number": "INV-2026-0881",
                "date": "28/09/2026",
                "subtotal": "₹4,250.00",
                "cgst_9pct": "₹382.50",
                "sgst_9pct": "₹382.50",
                "total_amount": "₹5,015.00",
                "payment_mode": "UPI / QR Code"
            },
            "ai_insights": "All tax calculations verified. Payout credit note scheduled for standard T+2 settlement.",
            "confidence": 0.96
        }
    else:
        return {
            "file_name": file_name,
            "document_type": "Product Catalog / Visual Inventory Item",
            "extracted_fields": {
                "detected_object": "Consumer Electronics / Audio Device",
                "suggested_title": "Wireless Bluetooth Earbuds Pro",
                "suggested_category": "Electronics > Audio > Headphones",
                "image_resolution": "High Quality (1024x1024)",
                "background_compliance": "Clean white studio background - Passed"
            },
            "ai_insights": "Image meets GOLO Merchant catalog guidelines. Product title and high-res variants generated successfully.",
            "confidence": 0.95
        }


@app.get("/languages", tags=["Languages"])
async def get_supported_languages():
    """Returns list of supported international languages and sample greetings."""
    return {
        "supported_count": 105,
        "primary_languages": [
            {"code": "en", "name": "English", "native": "English", "greeting": "Ask anything. Get intelligent answers."},
            {"code": "es", "name": "Spanish", "native": "Español", "greeting": "Pregunta lo que sea. Obtén respuestas inteligentes."},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी", "greeting": "कुछ भी पूछें। समझदार और सटीक उत्तर पाएं।"},
            {"code": "fr", "name": "French", "native": "Français", "greeting": "Demandez n'importe quoi. Obtenez des réponses intelligentes."},
            {"code": "de", "name": "German", "native": "Deutsch", "greeting": "Fragen Sie alles. Erhalten Sie intelligente Antworten."},
            {"code": "ja", "name": "Japanese", "native": "日本語", "greeting": "何でも質問してください。的確な回答を提供します。"},
            {"code": "zh", "name": "Mandarin", "native": "中文", "greeting": "随心提问。获取智能准确的答案。"},
            {"code": "ar", "name": "Arabic", "native": "العربية", "greeting": "اسأل أي شيء. واحصل على إجابات ذكية وموثوقة."}
        ]
    }


# ─── Run Server ─────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
