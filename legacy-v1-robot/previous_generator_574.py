"""
Generator script to update frontend/index.html with:
1. Official Golo Hero background image (golo_official_hero.jpg) on the introduction page.
2. Animated interactive Golo Robot in the upper-left of the AI assistant window.
3. 5 Dynamic Animated States:
   - IDLE: Gentle floating, soft cyan breathing.
   - TYPING: Keyboard movement, mechanical key-tap vibration, focused head bobbing.
   - PROCESSING: Spinning concentric energy rings on robot head, thought tilt.
   - HAPPY: Celebratory bounce, golden sparkle aura, victory badge.
   - ERROR / OUT-OF-SCOPE: Horizontal head shake, flashing red/amber alert beacon.
4. Synchronized in both Light Mode (default) and Dark Mode.
5. All 163 FAQs embedded with RAG & NLP support.
"""

import os
import json
import sys

sys.path.append(r'c:\Users\Windows\Downloads\golo\golo-ai-assistant\backend')
from knowledge_base import FAQ_DATABASE

faqs_json = json.dumps(FAQ_DATABASE)

html_code = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Golo AI — Smarter Insights for Stronger Merchants</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <link rel="icon" type="image/png" href="logo.png">

    <style>
        /* ==========================================================================
           GOLO CINEMATIC PALETTE & DESIGN SYSTEM
           Default Theme: LIGHT MODE (Clean, luminous retail cyber-tech)
           Alternate: DARK MODE (Deep neon cyberpunk midnight)
           ========================================================================== */
        :root {{
            --font-display: 'Orbitron', -apple-system, sans-serif;
            --font-sub: 'Rajdhani', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;

            /* Brand Colors matching Golo Logo */
            --golo-blue: #2563EB;
            --golo-blue-dark: #1D4ED8;
            --golo-blue-light: #60A5FA;
            --golo-yellow: #F5B849;
            --golo-gold: #D97706;
            --golo-cyan: #06B6D4;
            --golo-green: #10B981;
            --golo-red: #EF4444;

            /* Light Mode Variables (DEFAULT) */
            --bg-page: #F8FAFC;
            --bg-grid: rgba(37, 99, 235, 0.04);
            --bg-surface: #FFFFFF;
            --bg-surface-trans: rgba(255, 255, 255, 0.94);
            --bg-card: #F1F5F9;
            --bg-card-hover: #E2E8F0;
            --text-main: #0F172A;
            --text-sub: #334155;
            --text-muted: #64748B;
            --border-ui: #CBD5E1;
            --border-highlight: #93C5FD;
            --hero-overlay: linear-gradient(180deg, rgba(255, 255, 255, 0.35) 0%, rgba(248, 250, 252, 0.88) 55%, #F8FAFC 100%);
            --neon-shadow: 0 10px 30px rgba(37, 99, 235, 0.15);
            --cube-border: #2563EB;
            --cube-face-bg: rgba(255, 255, 255, 0.92);
            --cube-text: #1E3A8A;
            --robot-aura-color: rgba(37, 99, 235, 0.35);
        }}

        [data-theme="dark"] {{
            /* Dark Mode Variables */
            --bg-page: #060A14;
            --bg-grid: rgba(6, 182, 212, 0.05);
            --bg-surface: #0B132B;
            --bg-surface-trans: rgba(11, 19, 43, 0.94);
            --bg-card: #111E3D;
            --bg-card-hover: #1A2B52;
            --text-main: #F8FAFC;
            --text-sub: #CBD5E1;
            --text-muted: #94A3B8;
            --border-ui: #1E293B;
            --border-highlight: #0284C7;
            --hero-overlay: linear-gradient(180deg, rgba(6, 10, 20, 0.50) 0%, rgba(6, 10, 20, 0.92) 55%, #060A14 100%);
            --neon-shadow: 0 10px 35px rgba(6, 182, 212, 0.35);
            --cube-border: #06B6D4;
            --cube-face-bg: rgba(6, 182, 212, 0.22);
            --cube-text: #38BDF8;
            --robot-aura-color: rgba(6, 182, 212, 0.45);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: background-color 0.25s ease, border-color 0.25s ease, color 0.25s ease;
        }}

        body {{
            background-color: var(--bg-page);
            color: var(--text-main);
            font-family: var(--font-body);
            overflow-x: hidden;
            min-height: 100vh;
            position: relative;
        }}

        /* Subtle animated background grid */
        .cyber-grid {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: 
                linear-gradient(to right, var(--bg-grid) 1px, transparent 1px),
                linear-gradient(to bottom, var(--bg-grid) 1px, transparent 1px);
            background-size: 48px 48px;
            pointer-events: none;
            z-index: 0;
        }}

        /* Clean Top Navigation Bar */
        .gaming-nav {{
            position: sticky;
            top: 0;
            width: 100%;
            height: 70px;
            background: var(--bg-surface-trans);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-ui);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            z-index: 100;
        }}

        .brand-cluster {{
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }}
        .brand-logo-img {{
            height: 38px;
            object-fit: contain;
            filter: drop-shadow(0 2px 4px rgba(37,99,235,0.2));
        }}
        .brand-badge {{
            font-family: var(--font-mono);
            font-size: 0.72rem;
            font-weight: 700;
            color: #ffffff;
            background: linear-gradient(135deg, var(--golo-blue), var(--golo-cyan));
            padding: 4px 10px;
            border-radius: 999px;
            letter-spacing: 0.5px;
        }}

        .nav-controls {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .btn-theme-quick {{
            background: var(--bg-card);
            border: 1px solid var(--border-ui);
            color: var(--text-main);
            width: 38px;
            height: 38px;
            border-radius: 9px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            transition: all 0.2s;
        }}
        .btn-theme-quick:hover {{
            background: var(--bg-card-hover);
            border-color: var(--golo-blue);
            transform: scale(1.05);
        }}

        .btn-open-assistant-hero {{
            background: linear-gradient(135deg, var(--golo-blue), #1D4ED8);
            color: #ffffff;
            border: none;
            padding: 9px 20px;
            border-radius: 10px;
            font-family: var(--font-sub);
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .btn-open-assistant-hero:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
        }}

        /* ==========================================================================
           FULL-WIDTH ALL-OVER INTRODUCTION HERO BANNER (USING OFFICIAL GOLO HERO IMAGE)
           ========================================================================== */
        .hero-allover-section {{
            position: relative;
            width: 100%;
            min-height: calc(100vh - 70px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2.5rem 2rem 4rem 2rem;
            overflow: hidden;
        }}

        /* Official GOLO Hero Background (Robot, Laptop Dashboard, Phone, Mug, Desk) */
        .hero-backdrop-image {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            object-fit: cover;
            object-position: center 20%;
            z-index: 1;
            filter: contrast(1.05) brightness(1.02);
            animation: subtleZoom 30s ease-in-out infinite alternate;
        }}
        @keyframes subtleZoom {{
            0% {{ transform: scale(1); }}
            100% {{ transform: scale(1.04); }}
        }}

        /* Luminous Scrim Gradient Layer */
        .hero-scrim-overlay {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: var(--hero-overlay);
            z-index: 2;
            pointer-events: none;
        }}

        /* Foreground Content Layer */
        .hero-content-wrapper {{
            position: relative;
            z-index: 3;
            max-width: 1050px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 1.4rem;
        }}

        /* 3D ROTATING "AI" CUBE CORE AT THE HERO CENTER */
        .cube-stage {{
            width: 120px;
            height: 120px;
            perspective: 800px;
            margin: 0 auto;
            cursor: pointer;
            position: relative;
        }}
        .cube-aura {{
            position: absolute;
            top: 50%; left: 50%;
            width: 130px; height: 130px;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            background: radial-gradient(circle, rgba(37, 99, 235, 0.4) 0%, rgba(6, 182, 212, 0.2) 50%, transparent 75%);
            animation: auraPulse 3s infinite alternate;
            pointer-events: none;
        }}
        @keyframes auraPulse {{
            0% {{ transform: translate(-50%, -50%) scale(0.9); opacity: 0.6; }}
            100% {{ transform: translate(-50%, -50%) scale(1.3); opacity: 1; }}
        }}

        .cube-3d {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            animation: rotateCube 12s linear infinite;
        }}
        .cube-3d:hover {{
            animation-duration: 4s;
        }}
        @keyframes rotateCube {{
            0% {{ transform: rotateX(-18deg) rotateY(0deg) rotateZ(0deg); }}
            100% {{ transform: rotateX(-18deg) rotateY(360deg) rotateZ(0deg); }}
        }}

        .cube-face {{
            position: absolute;
            width: 110px;
            height: 110px;
            background: var(--cube-face-bg);
            border: 2px solid var(--cube-border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-display);
            font-size: 2rem;
            font-weight: 900;
            color: var(--cube-text);
            box-shadow: inset 0 0 15px rgba(37, 99, 235, 0.2);
            backdrop-filter: blur(8px);
            user-select: none;
        }}
        .cube-face-front  {{ transform: rotateY(0deg) translateZ(55px); }}
        .cube-face-back   {{ transform: rotateY(180deg) translateZ(55px); }}
        .cube-face-right  {{ transform: rotateY(90deg) translateZ(55px); }}
        .cube-face-left   {{ transform: rotateY(-90deg) translateZ(55px); }}
        .cube-face-top    {{ transform: rotateX(90deg) translateZ(55px); }}
        .cube-face-bottom {{ transform: rotateX(-90deg) translateZ(55px); }}

        .cube-trigger-label {{
            font-family: var(--font-mono);
            font-size: 0.74rem;
            color: var(--golo-blue);
            font-weight: 700;
            letter-spacing: 1px;
            margin-top: 4px;
            background: var(--bg-surface-trans);
            padding: 3px 12px;
            border-radius: 999px;
            border: 1px solid var(--border-ui);
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}

        /* Hero Text & Badges */
        .hero-tag-wrap {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-surface-trans);
            border: 1px solid var(--border-highlight);
            padding: 6px 16px;
            border-radius: 999px;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--golo-blue);
            box-shadow: 0 2px 10px rgba(37, 99, 235, 0.12);
        }}

        .hero-headline {{
            font-family: var(--font-display);
            font-size: 2.7rem;
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.5px;
            color: var(--text-main);
            text-shadow: 0 2px 10px rgba(255,255,255,0.85);
        }}
        [data-theme="dark"] .hero-headline {{
            text-shadow: 0 4px 20px rgba(0,0,0,0.85);
        }}

        .hero-desc {{
            font-size: 1.1rem;
            line-height: 1.6;
            color: var(--text-sub);
            max-width: 760px;
            font-weight: 500;
        }}

        /* Hero Search Bar with Working Voice Mic */
        .hero-search-capsule {{
            width: 100%;
            max-width: 680px;
            background: var(--bg-surface);
            border: 2px solid var(--border-highlight);
            border-radius: 999px;
            padding: 6px 8px 6px 20px;
            display: flex;
            align-items: center;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.18);
            transition: all 0.25s;
        }}
        .hero-search-capsule:focus-within {{
            border-color: var(--golo-blue);
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.3);
            transform: scale(1.01);
        }}

        .hero-search-input {{
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            font-size: 1.02rem;
            font-family: var(--font-body);
            color: var(--text-main);
        }}

        .btn-hero-mic {{
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            margin-right: 6px;
        }}
        .btn-hero-mic:hover {{
            background: var(--bg-card);
            color: var(--golo-blue);
        }}
        .btn-hero-mic.recording-active {{
            background: var(--golo-red);
            color: #ffffff;
            animation: pulseHeroMic 1.2s infinite;
        }}
        @keyframes pulseHeroMic {{
            0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
            70% {{ transform: scale(1.1); box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }}
            100% {{ transform: scale(1); }}
        }}

        .btn-hero-submit {{
            background: linear-gradient(135deg, var(--golo-blue), var(--golo-blue-dark));
            color: #ffffff;
            border: none;
            padding: 10px 22px;
            border-radius: 999px;
            font-family: var(--font-sub);
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .btn-hero-submit:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }}

        /* 6 Curated Starting FAQ Chips */
        .chips-section {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            margin-top: 0.5rem;
        }}
        .chips-title {{
            font-family: var(--font-sub);
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-muted);
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .chips-cluster {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.65rem;
            max-width: 900px;
        }}
        .hero-chip {{
            background: var(--bg-surface-trans);
            border: 1px solid var(--border-ui);
            padding: 8px 16px;
            border-radius: 999px;
            font-family: var(--font-body);
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-main);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            transition: all 0.2s;
        }}
        .hero-chip:hover {{
            border-color: var(--golo-blue);
            color: var(--golo-blue);
            transform: translateY(-2px);
            box-shadow: 0 6px 14px var(--neon-shadow);
        }}

        /* ==========================================================================
           ANIMATED ROBOT CHARACTER IN AI MODEL WINDOW (HEADER LEFT)
           States: IDLE | TYPING | PROCESSING | HAPPY | ERROR
           ========================================================================== */
        .robot-actor-box {{
            position: relative;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            user-select: none;
        }}

        /* Robot Avatar Capsule Frame */
        .robot-avatar-capsule {{
            position: relative;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--bg-surface);
            border: 2px solid var(--golo-blue);
            box-shadow: 0 0 12px var(--robot-aura-color);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: visible;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}

        .robot-avatar-img {{
            width: 42px;
            height: 42px;
            border-radius: 50%;
            object-fit: cover;
            object-position: center 20%;
            transition: transform 0.25s ease;
        }}

        /* Head Aura & Antenna Pulse */
        .robot-antenna-aura {{
            position: absolute;
            top: -6px;
            left: 50%;
            width: 14px;
            height: 14px;
            transform: translateX(-50%);
            border-radius: 50%;
            background: var(--golo-cyan);
            box-shadow: 0 0 8px var(--golo-cyan);
            pointer-events: none;
            opacity: 0.8;
            transition: all 0.3s ease;
        }}

        /* Reaction Badge (Emoji reaction on robot's shoulder) */
        .robot-reaction-icon {{
            position: absolute;
            bottom: -3px;
            right: -5px;
            font-size: 0.85rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-ui);
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            transition: transform 0.3s;
        }}

        /* Robot Status & Name Cluster */
        .robot-actor-text {{
            display: flex;
            flex-direction: column;
            text-align: left;
        }}
        .robot-actor-name {{
            font-family: var(--font-display);
            font-size: 0.95rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.3px;
        }}
        .robot-actor-status {{
            font-family: var(--font-mono);
            font-size: 0.72rem;
            font-weight: 600;
            color: #93C5FD;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: color 0.3s;
        }}

        /* Mini Holographic Keyboard that appears when typing */
        .robot-holo-keys {{
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            display: none;
            gap: 2px;
            background: rgba(37, 99, 235, 0.85);
            padding: 2px 6px;
            border-radius: 4px;
            box-shadow: 0 0 10px var(--golo-cyan);
            pointer-events: none;
        }}
        .holo-dot {{
            width: 4px;
            height: 4px;
            border-radius: 1px;
            background: #ffffff;
        }}

        /* --- STATE 1: IDLE --- */
        [data-robot-state="idle"] .robot-avatar-img {{
            animation: robotBreathe 4s ease-in-out infinite;
        }}
        @keyframes robotBreathe {{
            0%, 100% {{ transform: translateY(0px) scale(1); }}
            50% {{ transform: translateY(-2px) scale(1.02); }}
        }}

        /* --- STATE 2: TYPING (Moving arms / typing keys) --- */
        [data-robot-state="typing"] .robot-avatar-capsule {{
            border-color: var(--golo-cyan);
            box-shadow: 0 0 16px var(--golo-cyan);
        }}
        [data-robot-state="typing"] .robot-avatar-img {{
            animation: robotTypingMotion 0.35s ease-in-out infinite alternate;
        }}
        @keyframes robotTypingMotion {{
            0% {{ transform: translateY(0px) rotate(-2deg); }}
            100% {{ transform: translateY(2px) rotate(2deg); }}
        }}
        [data-robot-state="typing"] .robot-holo-keys {{
            display: flex;
        }}
        [data-robot-state="typing"] .holo-dot:nth-child(1) {{ animation: keyTap 0.3s infinite alternate 0.05s; }}
        [data-robot-state="typing"] .holo-dot:nth-child(2) {{ animation: keyTap 0.3s infinite alternate 0.15s; }}
        [data-robot-state="typing"] .holo-dot:nth-child(3) {{ animation: keyTap 0.3s infinite alternate 0.25s; }}
        @keyframes keyTap {{
            0% {{ transform: scaleY(0.6); opacity: 0.4; }}
            100% {{ transform: scaleY(1.3); opacity: 1; }}
        }}
        [data-robot-state="typing"] .robot-actor-status {{
            color: #67E8F9;
        }}

        /* --- STATE 3: PROCESSING (Head Antenna Rings & Deep Thought) --- */
        [data-robot-state="processing"] .robot-avatar-capsule {{
            border-color: var(--golo-yellow);
            box-shadow: 0 0 20px rgba(245, 184, 73, 0.7);
        }}
        [data-robot-state="processing"] .robot-avatar-img {{
            animation: robotThinkingTilt 1.4s ease-in-out infinite alternate;
        }}
        @keyframes robotThinkingTilt {{
            0% {{ transform: rotate(-5deg); }}
            100% {{ transform: rotate(5deg); }}
        }}
        [data-robot-state="processing"] .robot-antenna-aura {{
            background: var(--golo-yellow);
            animation: antennaProcessingRings 1s infinite;
        }}
        @keyframes antennaProcessingRings {{
            0% {{ transform: translateX(-50%) scale(0.9); box-shadow: 0 0 4px var(--golo-yellow); opacity: 1; }}
            100% {{ transform: translateX(-50%) scale(2.6); box-shadow: 0 0 20px var(--golo-yellow); opacity: 0; }}
        }}
        [data-robot-state="processing"] .robot-actor-status {{
            color: var(--golo-yellow);
        }}

        /* --- STATE 4: HAPPY / CELEBRATION (Bouncy victory & joy) --- */
        [data-robot-state="happy"] .robot-avatar-capsule {{
            border-color: var(--golo-green);
            box-shadow: 0 0 24px rgba(16, 185, 129, 0.8);
            animation: happyAuraPop 0.8s ease-out;
        }}
        @keyframes happyAuraPop {{
            0% {{ transform: scale(0.85); }}
            50% {{ transform: scale(1.2); }}
            100% {{ transform: scale(1); }}
        }}
        [data-robot-state="happy"] .robot-avatar-img {{
            animation: robotHappyBounce 0.6s ease-in-out infinite alternate;
        }}
        @keyframes robotHappyBounce {{
            0% {{ transform: translateY(0px) scale(1); }}
            100% {{ transform: translateY(-7px) scale(1.08); }}
        }}
        [data-robot-state="happy"] .robot-antenna-aura {{
            background: var(--golo-green);
            box-shadow: 0 0 14px var(--golo-green);
        }}
        [data-robot-state="happy"] .robot-actor-status {{
            color: #6EE7B7;
        }}

        /* --- STATE 5: ERROR / OUT OF SCOPE (Head Shake & Red Alert Beacon) --- */
        [data-robot-state="error"] .robot-avatar-capsule {{
            border-color: var(--golo-red);
            box-shadow: 0 0 22px rgba(239, 68, 68, 0.8);
            animation: shakeError 0.5s ease-in-out;
        }}
        @keyframes shakeError {{
            0%, 100% {{ transform: translateX(0); }}
            20%, 60% {{ transform: translateX(-6px) rotate(-3deg); }}
            40%, 80% {{ transform: translateX(6px) rotate(3deg); }}
        }}
        [data-robot-state="error"] .robot-avatar-img {{
            animation: robotHeadShake 0.4s ease-in-out infinite alternate;
        }}
        @keyframes robotHeadShake {{
            0% {{ transform: rotate(-5deg); }}
            100% {{ transform: rotate(5deg); }}
        }}
        [data-robot-state="error"] .robot-antenna-aura {{
            background: var(--golo-red);
            animation: redAlertBlink 0.6s infinite alternate;
        }}
        @keyframes redAlertBlink {{
            0% {{ box-shadow: 0 0 4px var(--golo-red); opacity: 0.4; }}
            100% {{ box-shadow: 0 0 18px var(--golo-red); opacity: 1; transform: translateX(-50%) scale(1.4); }}
        }}
        [data-robot-state="error"] .robot-actor-status {{
            color: #FCA5A5;
        }}

        /* ==========================================================================
           FLOATING TRIGGER & CHAT ASSISTANT DRAWER (SCREEN VIEWPORT SAFE + BACK BUTTON)
           ========================================================================== */
        .chat-floating-button {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 62px;
            height: 62px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--golo-blue), var(--golo-cyan));
            color: #ffffff;
            border: none;
            cursor: pointer;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.25s, box-shadow 0.25s;
        }}
        .chat-floating-button:hover {{
            transform: scale(1.08) translateY(-2px);
        }}
        .beacon-dot {{
            position: absolute;
            top: 2px; right: 2px;
            width: 14px; height: 14px;
            border-radius: 50%;
            background: var(--golo-green);
            border: 2px solid var(--bg-surface);
            box-shadow: 0 0 8px var(--golo-green);
        }}

        /* CHAT DRAWER: Strict Screen Sizing to Prevent Cutoff */
        .chat-drawer {{
            position: fixed;
            bottom: 85px;
            right: 24px;
            width: min(440px, calc(100vw - 32px));
            height: min(580px, calc(100vh - 105px));
            max-height: calc(100vh - 100px);
            background: var(--bg-surface);
            border: 1px solid var(--border-ui);
            border-radius: 20px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
            display: flex;
            flex-direction: column;
            z-index: 9998;
            transform-origin: bottom right;
            transform: scale(0.7) translateY(40px);
            opacity: 0;
            pointer-events: none;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s, width 0.3s, height 0.3s;
            overflow: hidden;
        }}
        .chat-drawer.open {{
            transform: scale(1) translateY(0);
            opacity: 1;
            pointer-events: all;
        }}

        /* Maximized Mode */
        .chat-drawer.maximized {{
            width: min(920px, calc(100vw - 40px));
            height: min(720px, calc(100vh - 90px));
            max-height: calc(100vh - 90px);
            bottom: 30px;
            right: 20px;
        }}

        /* Chat Header with Dedicated Back Button & Left Animated Robot Character */
        .chat-header {{
            background: linear-gradient(135deg, #1E3A8A, var(--golo-blue));
            color: #ffffff;
            padding: 0.75rem 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            user-select: none;
        }}

        .header-left-cluster {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        /* Dedicated Back Button */
        .btn-back-header {{
            background: rgba(255, 255, 255, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #ffffff;
            padding: 6px 12px;
            border-radius: 8px;
            font-family: var(--font-sub);
            font-size: 0.88rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: all 0.2s;
        }}
        .btn-back-header:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateX(-2px);
        }}

        .header-actions-group {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .header-icon-btn {{
            background: rgba(255, 255, 255, 0.14);
            border: none;
            color: #ffffff;
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.2s;
        }}
        .header-icon-btn:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}

        /* Message Stream Body */
        .chat-body-stream {{
            flex: 1;
            padding: 1rem 1.15rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            background: var(--bg-surface);
        }}

        .message-row {{
            display: flex;
            flex-direction: column;
            max-width: 86%;
            animation: msgFadeIn 0.25s ease-out;
        }}
        @keyframes msgFadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .message-row.user {{
            align-self: flex-end;
            align-items: flex-end;
        }}
        .message-row.ai {{
            align-self: flex-start;
            align-items: flex-start;
        }}

        .msg-bubble-box {{
            padding: 0.75rem 1rem;
            border-radius: 14px;
            font-size: 0.92rem;
            line-height: 1.5;
            word-break: break-word;
        }}
        .user .msg-bubble-box {{
            background: linear-gradient(135deg, var(--golo-blue), var(--golo-blue-dark));
            color: #ffffff;
            border-bottom-right-radius: 4px;
        }}
        .ai .msg-bubble-box {{
            background: var(--bg-card);
            color: var(--text-main);
            border: 1px solid var(--border-ui);
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}

        .ai-source-badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--golo-blue);
            background: rgba(37, 99, 235, 0.08);
            padding: 2px 7px;
            border-radius: 4px;
            margin-bottom: 4px;
        }}

        /* Query Input Bar */
        .chat-input-toolbar {{
            padding: 0.85rem 1rem;
            background: var(--bg-surface);
            border-top: 1px solid var(--border-ui);
            position: relative;
        }}

        .input-capsule {{
            display: flex;
            align-items: center;
            background: var(--bg-card);
            border: 1px solid var(--border-ui);
            border-radius: 999px;
            padding: 4px 6px 4px 14px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        .input-capsule:focus-within {{
            border-color: var(--golo-blue);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
        }}

        .query-input-field {{
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-main);
            font-size: 0.92rem;
            font-family: var(--font-body);
            outline: none;
            padding: 6px 0;
        }}

        .btn-mic-record {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: transparent;
            border: none;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
            margin-right: 4px;
        }}
        .btn-mic-record:hover {{
            background: var(--bg-card-hover);
            color: var(--golo-blue);
        }}
        .btn-mic-record.recording-active {{
            background: var(--golo-red);
            color: #ffffff;
            animation: pulseRec 1.2s infinite;
        }}
        @keyframes pulseRec {{
            0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
            70% {{ transform: scale(1.1); box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
            100% {{ transform: scale(1); }}
        }}

        .btn-send-query {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--golo-blue);
            color: #ffffff;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-send-query:hover {{
            background: var(--golo-blue-dark);
            transform: scale(1.05);
        }}
        .btn-send-query:disabled {{
            opacity: 0.4;
            cursor: not-allowed;
            transform: none;
        }}

        .voice-feedback-bar {{
            display: none;
            padding: 6px 12px;
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid var(--golo-red);
            border-radius: 8px;
            font-size: 0.8rem;
            color: var(--golo-red);
            font-weight: 600;
            margin-bottom: 8px;
            text-align: center;
        }}

        .minibar-dock {{
            position: fixed;
            bottom: 24px;
            right: 98px;
            background: var(--bg-surface);
            border: 1px solid var(--border-ui);
            padding: 10px 18px;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
            display: none;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            z-index: 9997;
        }}
        .minibar-dock.visible {{
            display: flex;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .hero-headline {{ font-size: 2.1rem; }}
            .chat-drawer {{
                width: 100vw;
                height: 100vh;
                max-height: 100vh;
                bottom: 0;
                right: 0;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>

    <div class="cyber-grid"></div>

    <!-- Navigation Bar -->
    <header class="gaming-nav">
        <a href="#" class="brand-cluster">
            <img src="logo.png" alt="Golo Logo" class="brand-logo-img" onerror="this.src='logo.jpg'">
            <span class="brand-badge">RAG NLP Model v2.5</span>
        </a>

        <div class="nav-controls">
            <button class="btn-theme-quick" onclick="toggleTheme()" id="btnQuickTheme" title="Toggle Light/Dark Mode">🌙</button>

            <button class="btn-open-assistant-hero" onclick="openAssistantModal()">
                <span>💬 Launch AI Assistant</span>
            </button>
        </div>
    </header>

    <!-- FULL-WIDTH INTRODUCTION HERO BANNER (USING OFFICIAL GOLO HERO IMAGE) -->
    <main class="hero-allover-section">
        <!-- Official Golo Hero Graphic as Full-Width Background -->
        <img src="golo_official_hero.jpg" alt="Golo Retail Platform & AI Assistant" class="hero-backdrop-image">
        
        <!-- Luminous Scrim Gradient Layer for Light/Dark mode readability -->
        <div class="hero-scrim-overlay"></div>

        <!-- Foreground Content Layer -->
        <div class="hero-content-wrapper">
            <!-- Centered 3D Rotating "AI" Cube with Glow -->
            <div class="cube-stage" onclick="openAssistantModal()" title="Click the 3D AI Core to Open Assistant">
                <div class="cube-aura"></div>
                <div class="cube-3d">
                    <div class="cube-face cube-face-front">AI</div>
                    <div class="cube-face cube-face-back">AI</div>
                    <div class="cube-face cube-face-right">AI</div>
                    <div class="cube-face cube-face-left">AI</div>
                    <div class="cube-face cube-face-top">AI</div>
                    <div class="cube-face cube-face-bottom">AI</div>
                </div>
            </div>
            <div class="cube-trigger-label">✦ CLICK 3D AI CORE ✦</div>

            <div class="hero-tag-wrap">
                <span>⚡ NEXAPRIME RETAIL INTELLIGENCE • SMARTER INSIGHTS FOR STRONGER MERCHANTS</span>
            </div>

            <h1 class="hero-headline">Golo Grounded AI Platform Guide</h1>
            <p class="hero-desc">
                AI-powered tools to help you track, manage, and grow. Deterministic RAG & NLP guidance for neighborhood shoppers, retail merchants, and platform administrators.
            </p>

            <!-- Hero Quick Query Search Bar with Voice Microphone Recording -->
            <div class="hero-search-capsule">
                <input type="text" class="hero-search-input" id="heroSearchInput" placeholder="Ask any question about Golo (e.g. how to log out, orders, vouchers)...">
                
                <button class="btn-hero-mic" id="btnHeroMic" onclick="toggleHeroVoiceRecording()" title="Speak Voice Question">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                        <line x1="12" y1="19" x2="12" y2="23"></line>
                        <line x1="8" y1="23" x2="16" y2="23"></line>
                    </svg>
                </button>

                <button class="btn-hero-submit" onclick="submitHeroQuery()">
                    <span>Ask AI</span>
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </button>
            </div>

            <!-- Popular Starting Questions (Official Documentation) -->
            <div class="chips-section">
                <span class="chips-title">Popular Starting Questions (Official Documentation)</span>
                <div class="chips-cluster">
                    <button class="hero-chip" onclick="askQuestion('What is GOLO and how does it work?')">
                        <span>💡</span> What is GOLO & how does it work?
                    </button>
                    <button class="hero-chip" onclick="askQuestion('How do I log out of my GOLO account?')">
                        <span>🚪</span> How do I log out of my account?
                    </button>
                    <button class="hero-chip" onclick="askQuestion('How do I claim an offer voucher?')">
                        <span>🎟️</span> How do I claim an offer voucher?
                    </button>
                    <button class="hero-chip" onclick="askQuestion('What is a Credit Note and does GOLO provide cash refunds?')">
                        <span>💳</span> What is the Refund & Credit Note Policy?
                    </button>
                    <button class="hero-chip" onclick="askQuestion('How does merchant verification KYC work?')">
                        <span>🛡️</span> How does KYC verification work?
                    </button>
                    <button class="hero-chip" onclick="askQuestion('How can I register as a merchant on GOLO?')">
                        <span>🏪</span> How to register as a merchant?
                    </button>
                </div>
            </div>
        </div>
    </main>

    <!-- Floating Launcher Trigger Button -->
    <button class="chat-floating-button" id="chatLauncherBtn" onclick="toggleAssistantModal()" title="Ask Golo AI">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
        </svg>
        <div class="beacon-dot"></div>
    </button>

    <!-- Minimized Dock -->
    <div class="minibar-dock" id="minibarDock" onclick="openAssistantModal()">
        <span style="width:8px; height:8px; border-radius:50%; background:var(--golo-green);"></span>
        <span style="font-weight:700; font-size:0.88rem;">Golo AI Active</span>
        <span style="font-size:0.78rem; color:var(--text-muted);">(Click to restore)</span>
    </div>

    <!-- AI Assistant Window (Screen Viewport Safe + Dedicated Back Button + Interactive Robot Character) -->
    <div class="chat-drawer" id="chatAssistantDrawer">
        <!-- Header with Back Button and Upper-Left Dynamic Robot Character -->
        <div class="chat-header">
            <div class="header-left-cluster">
                <!-- Dedicated Back Button to Return to Main Portal Screen -->
                <button class="btn-back-header" onclick="closeAssistantModal()" title="Back to Portal">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="19" y1="12" x2="5" y2="12"></line>
                        <polyline points="12 19 5 12 12 5"></polyline>
                    </svg>
                    <span>Back</span>
                </button>

                <!-- Dynamic State-Driven Golo Robot Actor -->
                <div class="robot-actor-box" id="robotActor" data-robot-state="idle" title="Golo AI Assistant Robot">
                    <!-- Head Processing Ring & Alert Aura -->
                    <div class="robot-antenna-aura" id="robotAntennaAura"></div>

                    <!-- Robot Avatar Capsule -->
                    <div class="robot-avatar-capsule">
                        <img src="golo_robot_avatar.png" alt="Golo Robot" class="robot-avatar-img" id="robotAvatarImg">
                        <div class="robot-reaction-icon" id="robotReactionIcon">🤖</div>
                    </div>

                    <!-- Mini Holographic Keyboard (typing motion) -->
                    <div class="robot-holo-keys">
                        <span class="holo-dot"></span>
                        <span class="holo-dot"></span>
                        <span class="holo-dot"></span>
                    </div>

                    <!-- Robot Name & Live Status Cluster -->
                    <div class="robot-actor-text">
                        <span class="robot-actor-name">Golo Bot</span>
                        <span class="robot-actor-status" id="robotActorStatus">● Ready</span>
                    </div>
                </div>
            </div>

            <div class="header-actions-group">
                <button class="header-icon-btn" onclick="toggleTheme()" title="Toggle Dark/Light Mode">🌓</button>
                <button class="header-icon-btn" onclick="toggleMaximizeDrawer()" title="Maximize / Restore" id="btnMaxToggle">⛶</button>
                <button class="header-icon-btn" onclick="minimizeAssistantModal()" title="Minimize to Dock">─</button>
                <button class="header-icon-btn" onclick="closeAssistantModal()" title="Close">✕</button>
            </div>
        </div>

        <!-- Chat Messages Conversation Stream -->
        <div class="chat-body-stream" id="chatMessageStream">
            <!-- Messages injected dynamically -->
        </div>

        <!-- Input Bar with Search Field, Microphone Button & Send Button -->
        <div class="chat-input-toolbar">
            <div class="voice-feedback-bar" id="voiceFeedbackBar">🎙️ Listening... Speak your question now</div>
            <div class="input-capsule">
                <input type="text" class="query-input-field" id="userQueryInputField" placeholder="Ask any GOLO question..." autocomplete="off">
                
                <!-- Microphone Voice Recording Button -->
                <button class="btn-mic-record" id="btnMicRecord" onclick="toggleVoiceRecording()" title="Record Voice Question">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                        <line x1="12" y1="19" x2="12" y2="23"></line>
                        <line x1="8" y1="23" x2="16" y2="23"></line>
                    </svg>
                </button>

                <!-- Send Button -->
                <button class="btn-send-query" id="btnSendQuery" onclick="dispatchUserQuery()" disabled title="Send Question">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <!-- Complete 163 FAQs Embedded Dataset & Client-Side Engine -->
    <script>
        const ALL_GOLO_FAQS = {faqs_json};

        let isDrawerOpen = false;
        let isMaximized = false;
        let isRecording = false;
        let speechRecognizer = null;
        let activeTheme = localStorage.getItem('golo_theme') || 'light'; // DEFAULT LIGHT MODE
        let typingTimeout = null;

        // DOM Elements
        const drawer = document.getElementById('chatAssistantDrawer');
        const minibar = document.getElementById('minibarDock');
        const stream = document.getElementById('chatMessageStream');
        const inputField = document.getElementById('userQueryInputField');
        const btnSend = document.getElementById('btnSendQuery');
        const btnMic = document.getElementById('btnMicRecord');
        const voiceBar = document.getElementById('voiceFeedbackBar');
        const btnQuickTheme = document.getElementById('btnQuickTheme');
        const btnMaxToggle = document.getElementById('btnMaxToggle');
        const heroSearchInput = document.getElementById('heroSearchInput');
        const btnHeroMic = document.getElementById('btnHeroMic');
        
        // Robot Actor Elements
        const robotActor = document.getElementById('robotActor');
        const robotActorStatus = document.getElementById('robotActorStatus');
        const robotReactionIcon = document.getElementById('robotReactionIcon');

        // =========================================================================
        // DYNAMIC ROBOT STATE ENGINE
        // States: 'idle' | 'typing' | 'processing' | 'happy' | 'error'
        // =========================================================================
        function setRobotState(state, statusText = null) {{
            if (!robotActor) return;
            robotActor.setAttribute('data-robot-state', state);

            switch(state) {{
                case 'typing':
                    robotReactionIcon.innerText = '⌨️';
                    robotActorStatus.innerText = statusText || '⌨️ Typing...';
                    break;
                case 'processing':
                    robotReactionIcon.innerText = '🧠';
                    robotActorStatus.innerText = statusText || '🧠 Thinking...';
                    break;
                case 'happy':
                    robotReactionIcon.innerText = '✨';
                    robotActorStatus.innerText = statusText || '✨ Insight found!';
                    // Auto-revert to idle after 4 seconds
                    setTimeout(() => {{
                        if (robotActor.getAttribute('data-robot-state') === 'happy') {{
                            setRobotState('idle');
                        }}
                    }}, 4000);
                    break;
                case 'error':
                    robotReactionIcon.innerText = '⚠️';
                    robotActorStatus.innerText = statusText || '⚠️ Not app related';
                    // Auto-revert to idle after 5 seconds
                    setTimeout(() => {{
                        if (robotActor.getAttribute('data-robot-state') === 'error') {{
                            setRobotState('idle');
                        }}
                    }}, 5000);
                    break;
                case 'idle':
                default:
                    robotReactionIcon.innerText = '🤖';
                    robotActorStatus.innerText = '● Ready';
                    break;
            }}
        }}

        // Theme Initialization (Default Light)
        function initThemeSettings() {{
            setThemeMode(activeTheme);
        }}

        function setThemeMode(mode) {{
            activeTheme = mode;
            document.documentElement.setAttribute('data-theme', mode);
            localStorage.setItem('golo_theme', mode);
            btnQuickTheme.innerText = mode === 'light' ? '🌙' : '☀️';
        }}

        function toggleTheme() {{
            const next = activeTheme === 'light' ? 'dark' : 'light';
            setThemeMode(next);
        }}

        // Assistant Modal Controls
        function openAssistantModal() {{
            isDrawerOpen = true;
            drawer.classList.add('open');
            minibar.classList.remove('visible');
            if (stream.children.length === 0) {{
                renderInitialGreeting();
            }}
            setTimeout(() => inputField.focus(), 150);
            scrollMessagesBottom();
        }}

        function closeAssistantModal() {{
            isDrawerOpen = false;
            drawer.classList.remove('open');
            minibar.classList.remove('visible');
        }}

        function minimizeAssistantModal() {{
            isDrawerOpen = false;
            drawer.classList.remove('open');
            minibar.classList.add('visible');
        }}

        function toggleAssistantModal() {{
            if (isDrawerOpen) closeAssistantModal();
            else openAssistantModal();
        }}

        function toggleMaximizeDrawer() {{
            isMaximized = !isMaximized;
            if (isMaximized) {{
                drawer.classList.add('maximized');
                btnMaxToggle.innerText = '❐';
            }} else {{
                drawer.classList.remove('maximized');
                btnMaxToggle.innerText = '⛶';
            }}
            scrollMessagesBottom();
        }}

        function askQuestion(q) {{
            openAssistantModal();
            inputField.value = q;
            dispatchUserQuery();
        }}

        function submitHeroQuery() {{
            const val = heroSearchInput.value.trim();
            if (!val) return;
            askQuestion(val);
            heroSearchInput.value = '';
        }}

        heroSearchInput.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter') {{
                submitHeroQuery();
            }}
        }});

        // Live Typing Detection -> Sets Robot to 'typing' state
        function handleUserTypingEvent() {{
            setRobotState('typing');
            if (typingTimeout) clearTimeout(typingTimeout);
            typingTimeout = setTimeout(() => {{
                // If user stops typing and hasn't submitted yet
                const curState = robotActor.getAttribute('data-robot-state');
                if (curState === 'typing') {{
                    setRobotState('idle');
                }}
            }}, 1200);
        }}

        inputField.addEventListener('input', () => {{
            btnSend.disabled = inputField.value.trim().length === 0;
            handleUserTypingEvent();
        }});

        heroSearchInput.addEventListener('input', () => {{
            handleUserTypingEvent();
        }});

        inputField.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' && !e.shiftKey) {{
                e.preventDefault();
                dispatchUserQuery();
            }}
        }});

        // Web Speech API Voice Recording Feature
        function initSpeechEngine() {{
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                const SpeechClass = window.SpeechRecognition || window.webkitSpeechRecognition;
                speechRecognizer = new SpeechClass();
                speechRecognizer.continuous = false;
                speechRecognizer.interimResults = true;
                speechRecognizer.lang = 'en-US';

                speechRecognizer.onstart = () => {{
                    isRecording = true;
                    btnMic.classList.add('recording-active');
                    btnHeroMic.classList.add('recording-active');
                    voiceBar.style.display = 'block';
                    setRobotState('typing', '🎙️ Listening...');
                }};

                speechRecognizer.onresult = (e) => {{
                    let transcript = '';
                    for (let i = e.resultIndex; i < e.results.length; i++) {{
                        transcript += e.results[i][0].transcript;
                    }}
                    inputField.value = transcript;
                    heroSearchInput.value = transcript;
                    btnSend.disabled = transcript.trim().length === 0;
                    handleUserTypingEvent();
                }};

                speechRecognizer.onerror = () => stopSpeech();
                speechRecognizer.onend = () => stopSpeech();
            }}
        }}

        function toggleVoiceRecording() {{
            if (!speechRecognizer) initSpeechEngine();
            if (!speechRecognizer) {{
                alert('Speech recognition is not supported on this browser. Please type your query.');
                return;
            }}
            if (isRecording) {{
                speechRecognizer.stop();
                stopSpeech();
            }} else {{
                speechRecognizer.start();
            }}
        }}

        function toggleHeroVoiceRecording() {{
            openAssistantModal();
            toggleVoiceRecording();
        }}

        function stopSpeech() {{
            isRecording = false;
            btnMic.classList.remove('recording-active');
            btnHeroMic.classList.remove('recording-active');
            voiceBar.style.display = 'none';
            setRobotState('idle');
        }}

        // Initial Greeting with Curated 6 Introductory FAQs
        function renderInitialGreeting() {{
            const welcomeText = "Welcome to the GOLO AI Assistant! 🛍️ I am your grounded intelligence guide for the GOLO hyper-local platform and NexaPrime retail policies. What can I assist you with today?";
            appendMessage('ai', welcomeText, 'Official Golo Model');

            const chipsDiv = document.createElement('div');
            chipsDiv.className = 'chips-cluster';
            chipsDiv.style.marginTop = '0.5rem';

            const quickFaqs = [
                "What is GOLO?",
                "How do I log out of my GOLO account?",
                "How do I claim an offer voucher?",
                "How can I register as a merchant?",
                "What is a Credit Note?",
                "How does KYC verification work?"
            ];

            quickFaqs.forEach(q => {{
                const chip = document.createElement('button');
                chip.className = 'hero-chip';
                chip.innerHTML = `<span>💬</span> ${{q}}`;
                chip.onclick = () => {{
                    chipsDiv.remove();
                    askQuestion(q);
                }};
                chipsDiv.appendChild(chip);
            }});

            stream.appendChild(chipsDiv);
            scrollMessagesBottom();
        }}

        function appendMessage(sender, text, source = null) {{
            const row = document.createElement('div');
            row.className = `message-row ${{sender}}`;

            let formatted = text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\\n/g, '<br>');

            let badgeHtml = '';
            if (source && sender === 'ai') {{
                badgeHtml = `<span class="ai-source-badge">⚡ ${{source}}</span>`;
            }}

            row.innerHTML = `
                ${{badgeHtml}}
                <div class="msg-bubble-box">${{formatted}}</div>
            `;
            stream.appendChild(row);
            scrollMessagesBottom();
        }}

        function scrollMessagesBottom() {{
            setTimeout(() => {{
                stream.scrollTop = stream.scrollHeight;
            }}, 50);
        }}

        // Dual-Path Query Dispatcher: Live FastAPI RAG Backend -> Client Fallback Engine
        async function dispatchUserQuery() {{
            const query = inputField.value.trim();
            if (!query) return;

            appendMessage('user', query);
            inputField.value = '';
            btnSend.disabled = true;

            // 1. SET ROBOT TO PROCESSING / THINKING STATE
            setRobotState('processing', '🧠 Processing query...');

            const session_id = sessionStorage.getItem('golo_session_id') || ('sess_' + Math.random().toString(36).substring(2, 9));
            sessionStorage.setItem('golo_session_id', session_id);
            const merchant_id = localStorage.getItem('golo_merchant_id') || 'MRC-DEMO';

            // 2. Try Live FastAPI Server with RAG Engine
            try {{
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 3800);

                const res = await fetch('http://localhost:8000/chat', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ query, session_id, merchant_id }}),
                    signal: controller.signal
                }});
                clearTimeout(timeoutId);

                if (res.ok) {{
                    const data = await res.json();
                    appendMessage('ai', data.response, data.category || 'Golo AI');

                    // Check if response is out-of-scope refusal
                    if (data.source === 'out_of_scope' || data.category === 'out_of_scope') {{
                        setRobotState('error', '⚠️ Not app related');
                    }} else {{
                        setRobotState('happy', '✨ Insight found!');
                    }}
                    return;
                }}
            }} catch (err) {{
                // Server unavailable or timeout, fallback to Client RAG Engine
            }}

            // 3. Embedded Client-Side Engine (Semantic match across 163 FAQs)
            setTimeout(() => {{
                const clientRes = matchClientFaq(query);
                appendMessage('ai', clientRes.answer, clientRes.source);

                if (clientRes.source === 'Scope Guardrail') {{
                    setRobotState('error', '⚠️ Not app related');
                }} else {{
                    setRobotState('happy', '✨ Insight found!');
                }}
            }}, 350);
        }}

        function matchClientFaq(query) {{
            const qLower = query.toLowerCase().trim();

            // Strict Out-of-Scope check
            const outOfScopeTerms = ['cricket', 'football', 'world cup', 'weather', 'recipe', 'movie', 'president', 'sing a song', 'joke'];
            if (outOfScopeTerms.some(t => qLower.includes(t)) && !qLower.includes('golo')) {{
                return {{
                    answer: "It is not our app related question. Please try again. I am the Golo Merchant AI Assistant, specialized exclusively in guiding you through the Golo web application, product listings, orders, payments, KYC verification, and store settings. 😊",
                    source: "Scope Guardrail"
                }};
            }}

            // Logout intent fast path
            if (qLower.includes('logout') || qLower.includes('log out') || qLower.includes('sign out') || qLower.includes('signout')) {{
                const logoutFaq = ALL_GOLO_FAQS.find(f => f.id === 163);
                if (logoutFaq) {{
                    return {{ answer: logoutFaq.answer, source: logoutFaq.category }};
                }}
            }}

            // Domain check
            const appTerms = [
                'golo', 'merchant', 'product', 'products', 'order', 'orders', 'payment', 'payout',
                'voucher', 'vouchers', 'deal', 'deals', 'offer', 'offers', 'wallet', 'credit note',
                'kyc', 'verification', 'store', 'shop', 'dashboard', 'delivery', 'pickup', 'refund',
                'cancellation', 'subscription', 'wishlist', 'loyalty', 'points', 'stars', 'nexaprime',
                'account', 'admin', 'coupon', 'help', 'support', 'logout', 'login', 'password', 'profile'
            ];
            const isRelevant = appTerms.some(term => qLower.includes(term));
            if (!isRelevant) {{
                return {{
                    answer: "It is not our app related question. Please try again. I am the Golo Merchant AI Assistant, specialized exclusively in guiding you through the Golo web application, product listings, orders, payments, KYC verification, and store settings. 😊",
                    source: "Scope Guardrail"
                }};
            }}

            // Semantic scoring across 163 FAQs
            let best = null;
            let maxScore = 0;
            const words = qLower.replace(/[^\\w\\s]/g, '').split(/\\s+/);

            for (let f of ALL_GOLO_FAQS) {{
                let score = 0;
                const fqLower = f.question.toLowerCase();
                if (qLower.includes(fqLower)) score += 15;
                for (let tag of f.tags) {{
                    if (words.includes(tag.toLowerCase())) score += 3;
                    if (qLower.includes(tag.toLowerCase())) score += 2;
                }}
                if (score > maxScore) {{
                    maxScore = score;
                    best = f;
                }}
            }}

            if (best && maxScore >= 2) {{
                return {{ answer: best.answer, source: best.category }};
            }}

            return {{
                answer: "For this inquiry regarding the GOLO platform, please check your **Dashboard** settings or submit a ticket to **support@golo.com**. Our operations team will guide you step by step.",
                source: "GOLO Knowledge Base"
            }};
        }}

        // Initialize on DOM load
        window.addEventListener('DOMContentLoaded', () => {{
            initThemeSettings();
            initSpeechEngine();
        }});
    </script>
</body>
</html>
"""

target_path = r'c:\Users\Windows\Downloads\golo\golo-ai-assistant\frontend\index.html'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html_code)

print(f"Successfully generated {target_path} with official hero image & 5-state animated robot!")
