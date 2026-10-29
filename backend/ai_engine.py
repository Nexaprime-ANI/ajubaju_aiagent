"""
Golo AI Assistant - AI Engine
=============================
Core engine that processes merchant queries using the knowledge base.
Handles input validation, security checks, FAQ matching, and response generation.
"""

import uuid
import time
from typing import Dict, Optional, Tuple
from datetime import datetime

from knowledge_base import (
    FAQ_DATABASE,
    APP_KNOWLEDGE,
    SYSTEM_MESSAGES,
    find_faq_match,
    get_relevant_context,
    is_golo_related,
    check_security,
    validate_input,
    get_system_message,
    normalize_text,
)
from rag_engine import GoloRAGEngine


class GoloAIEngine:
    """
    The core AI engine for the Golo Merchant AI Assistant.
    Processes queries through validation, security, FAQ matching,
    and knowledge-based response generation.
    Supports per-merchant tracking, rate limits, and escalation.
    """

    def __init__(self):
        """Initialize the AI engine with session storage, merchant tracking, and RAG NLP engine."""
        self.sessions: Dict[str, list] = {}
        self.max_session_history = 10
        # Initialize RAG Engine with all FAQs
        self.rag_engine = GoloRAGEngine(FAQ_DATABASE)
        # Per-merchant rate limit tracking
        self.merchant_query_timestamps: Dict[str, list] = {}  # merchant_id -> list of float timestamps
        self.ratings: list = []  # list of rating records
        self.escalation_tickets: list = []  # list of escalation ticket records
        self.rate_limit_rpm = 20
        self.rate_limit_rpd = 200

    def _get_or_create_session(self, session_id: str) -> list:
        """Get existing session history or create a new one."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def _add_to_session(self, session_id: str, role: str, content: str):
        """Add a message to session history."""
        history = self._get_or_create_session(session_id)
        history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last N messages
        if len(history) > self.max_session_history * 2:
            self.sessions[session_id] = history[-self.max_session_history * 2:]

    def _generate_contextual_response(self, query: str, context: str) -> str:
        """
        Generate a helpful response based on found knowledge base context.
        This simulates AI reasoning using the grounded context.
        """
        query_lower = query.lower()

        # Extract key intents and generate targeted responses
        if any(word in query_lower for word in ["how", "steps", "process", "guide", "way"]):
            # User wants step-by-step guidance
            prefix = "Here's what I found that can help you:\n\n"
        elif any(word in query_lower for word in ["what", "which", "tell me about"]):
            # User wants information
            prefix = "Here's the information you need:\n\n"
        elif any(word in query_lower for word in ["why", "reason", "cause"]):
            prefix = "Let me explain:\n\n"
        elif any(word in query_lower for word in ["can i", "is it possible", "do you"]):
            prefix = "Great question! Here's what you need to know:\n\n"
        elif any(word in query_lower for word in ["problem", "issue", "error", "not working", "help"]):
            prefix = "I understand you're facing an issue. Here's how to resolve it:\n\n"
        else:
            prefix = "Here's what I can tell you about that:\n\n"

        # Clean up context for presentation
        context_lines = context.strip().split('\n')
        cleaned_lines = []
        for line in context_lines:
            line = line.strip()
            if line and not line.startswith('"""') and len(line) > 2:
                cleaned_lines.append(line)

        # Limit response length
        response_text = '\n'.join(cleaned_lines[:30])

        # Add helpful footer
        footer = "\n\n💡 If you need more specific help, feel free to ask a more detailed question or contact our support team!"

        return prefix + response_text + footer

    def process_query(
        self,
        query: str,
        session_id: Optional[str] = None,
        merchant_id: Optional[str] = None,
        language: str = "English",
        image_base64: Optional[str] = None
    ) -> Dict:
        """
        Process a merchant query through the complete pipeline.

        Pipeline:
        1. Rate limit verification (if merchant_id provided: 20 RPM / 200 RPD)
        2. Input validation
        3. Security check
        4. FAQ matching (zero-cost)
        5. Knowledge base search
        6. Context-based response generation
        7. Out-of-scope detection

        Returns a dict with: response, source, confidence, timestamp, session_id, merchant_id
        """
        if not session_id:
            session_id = str(uuid.uuid4())

        start_time = time.time()
        now_ts = time.time()
        timestamp = datetime.now().isoformat()

        # ─── Step 0: Per-Merchant Rate Limit Check ──────────────────
        if merchant_id:
            if merchant_id not in self.merchant_query_timestamps:
                self.merchant_query_timestamps[merchant_id] = []
            
            # Prune records older than 24h
            self.merchant_query_timestamps[merchant_id] = [
                ts for ts in self.merchant_query_timestamps[merchant_id] if (now_ts - ts) < 86400
            ]
            user_history = self.merchant_query_timestamps[merchant_id]

            # 1. RPM Check (last 60s)
            rpm_count = sum(1 for ts in user_history if (now_ts - ts) < 60)
            if rpm_count >= self.rate_limit_rpm:
                return {
                    "response": f"I'm handling a lot of queries right now! ⏳ You have reached the rate limit ({self.rate_limit_rpm} queries/min) for merchant ID [{merchant_id}]. Please wait about 60 seconds before trying again.",
                    "source": "rate_limiter",
                    "category": "rate_limit_rpm",
                    "confidence": 1.0,
                    "timestamp": timestamp,
                    "session_id": session_id,
                    "merchant_id": merchant_id,
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }

            # 2. Daily Check (last 24h)
            if len(user_history) >= self.rate_limit_rpd:
                return {
                    "response": f"You've reached today's daily query limit ({self.rate_limit_rpd} queries/day) for merchant ID [{merchant_id}]. Your limit resets at midnight IST. For urgent platform issues, please contact support@golo.com.",
                    "source": "rate_limiter",
                    "category": "rate_limit_day",
                    "confidence": 1.0,
                    "timestamp": timestamp,
                    "session_id": session_id,
                    "merchant_id": merchant_id,
                    "latency_ms": round((time.time() - start_time) * 1000, 2)
                }

            # Record this query
            self.merchant_query_timestamps[merchant_id].append(now_ts)

        # ─── Step 1: Input Validation ─────────────────────────
        validation_error = validate_input(query)
        if validation_error:
            if validation_error == "empty" or validation_error == "too_short":
                response = get_system_message("invalid_input")
            elif validation_error == "too_long":
                response = f"Your message is {len(query)} characters long, which exceeds our 2000 character limit. Could you please shorten your question? I'll be happy to help with a more concise version! 📝"
            elif validation_error == "gibberish":
                response = SYSTEM_MESSAGES["invalid_input"][1]
            else:
                response = get_system_message("invalid_input")

            return {
                "response": response,
                "source": "system",
                "category": "invalid_input",
                "confidence": 1.0,
                "timestamp": timestamp,
                "session_id": session_id,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # ─── Step 2: Security Check ─────────────────────────
        security_threat = check_security(query)
        if security_threat:
            if security_threat == "injection":
                response = SYSTEM_MESSAGES["security"][0]
            elif security_threat == "pii":
                response = SYSTEM_MESSAGES["security"][1]
            elif security_threat == "abuse":
                response = SYSTEM_MESSAGES["security"][2]
            else:
                response = get_system_message("security")

            return {
                "response": response,
                "source": "security_filter",
                "category": "security",
                "confidence": 1.0,
                "timestamp": timestamp,
                "session_id": session_id,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

        # ─── Step 3: RAG & NLP Semantic Retrieval & Generation ───────
        rag_output = self.rag_engine.generate_rag_response(
            query=query,
            session_id=session_id,
            merchant_id=merchant_id,
            language=language,
            image_base64=image_base64
        )

        response_text = rag_output.get("response", "")
        source = rag_output.get("source", "rag_nlp")
        category = rag_output.get("category", "General")
        confidence = rag_output.get("confidence", 0.95)
        faq_id = rag_output.get("faq_id")
        faq_question = rag_output.get("faq_question")
        needs_customer_service = rag_output.get("needs_customer_service", False)

        if source != "out_of_scope":
            self._add_to_session(session_id, "user", query)
            self._add_to_session(session_id, "assistant", response_text)

        return {
            "response": response_text,
            "source": source,
            "category": category,
            "faq_id": faq_id,
            "faq_question": faq_question,
            "needs_customer_service": needs_customer_service,
            "confidence": confidence,
            "timestamp": timestamp,
            "session_id": session_id,
            "merchant_id": merchant_id,
            "latency_ms": round((time.time() - start_time) * 1000, 2)
        }


    def get_welcome_message(self) -> str:
        """Get a welcome message for new sessions."""
        return get_system_message("welcome")

    def get_all_faqs(self) -> list:
        """Get all FAQ entries."""
        return FAQ_DATABASE

    def get_faqs_by_category(self, category: str) -> list:
        """Get FAQs filtered by category."""
        return [faq for faq in FAQ_DATABASE if faq["category"].lower() == category.lower()]

    def get_categories(self) -> list:
        """Get all FAQ categories."""
        categories = set(faq["category"] for faq in FAQ_DATABASE)
        return sorted(list(categories))

    def get_session_history(self, session_id: str) -> list:
        """Get conversation history for a session."""
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str):
        """Clear a session's conversation history."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def record_rating(self, session_id: str, rating: int, comment: Optional[str] = None, merchant_id: Optional[str] = None) -> Dict:
        """
        Record a customer satisfaction rating (1-5 stars) linked to session and optional merchant_id.
        Fulfills State 8 (Conversation Rating) from the specification.
        """
        record = {
            "session_id": session_id,
            "merchant_id": merchant_id,
            "rating": max(1, min(5, rating)),
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        self.ratings.append(record)
        return {"status": "recorded", "rating_id": len(self.ratings), "record": record}

    def create_escalation(self, session_id: str, reason: str, details: Optional[str] = None, merchant_id: Optional[str] = None) -> Dict:
        """
        Create a human support escalation ticket with conversation context.
        Fulfills State 7 (Support Escalation) from the specification.
        """
        import random
        ticket_ref = f"REF-{random.randint(1000, 9999)}"
        ticket = {
            "ticket_ref": ticket_ref,
            "merchant_id": merchant_id or "UNAUTHENTICATED",
            "session_id": session_id,
            "reason": reason,
            "details": details,
            "conversation_snippet": self.sessions.get(session_id, [])[-4:],
            "created_at": datetime.now().isoformat(),
            "status": "OPEN",
            "eta_hours": 4
        }
        self.escalation_tickets.append(ticket)
        return ticket

    def get_merchant_usage(self, merchant_id: str) -> Dict:
        """
        Get rate limit usage metrics for a specific merchant_id.
        Fulfills F07 & F12 from the specification.
        """
        now_ts = time.time()
        user_history = self.merchant_query_timestamps.get(merchant_id, [])
        rpm_used = sum(1 for ts in user_history if (now_ts - ts) < 60)
        rpd_used = sum(1 for ts in user_history if (now_ts - ts) < 86400)
        return {
            "merchant_id": merchant_id,
            "rpm_used": rpm_used,
            "rpm_limit": self.rate_limit_rpm,
            "rpm_remaining": max(0, self.rate_limit_rpm - rpm_used),
            "rpd_used": rpd_used,
            "rpd_limit": self.rate_limit_rpd,
            "rpd_remaining": max(0, self.rate_limit_rpd - rpd_used),
            "total_queries_recorded": len(user_history)
        }

    def get_suggestions(self, prefix: str, limit: int = 4) -> list:
        """Get query suggestions for autocomplete."""
        return self.rag_engine.get_suggestions(prefix, limit)

    def get_popular_faqs(self, limit: int = 8) -> list:
        """Get frequently asked questions for AI mode."""
        return self.rag_engine.get_popular_faqs(limit)

