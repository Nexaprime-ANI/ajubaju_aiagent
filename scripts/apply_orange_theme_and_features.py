import re

def update_style_css():
    path = "frontend/style.css"
    with open(path, "r", encoding="utf-8") as f:
        css = f.read()

    # 1. Update :root variables
    root_old = r''':root \{.*?--shadow-card-hover: 0 16px 40px rgba\(21, 122, 79, 0\.12\), 0 4px 12px rgba\(0, 0, 0, 0\.03\);\s*\}'''
    root_new = ''':root {
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;

    /* GOLO UI Dominant Warm Orange-Yellow Palette (Matching golowebapp.vercel.app) */
    --color-primary: #F5B849;
    --color-primary-dark: #D99B26;
    --color-primary-light: #F8C76D;
    --color-primary-tint: #FEF8EC;
    --color-primary-border: #FCE4B8;

    --color-secondary: #157A4F;
    --color-secondary-dark: #0E5E3B;
    --color-secondary-light: #1E9E66;
    --color-secondary-tint: #E8F5EF;
    --color-secondary-border: #C1E4D4;

    --color-accent-amber: #F9A641;
    --color-neutral-base: #F8F6F2;
    --color-neutral-border: #E5E1D8;
    --color-card-bg: #FFFFFF;
    --color-card-border: #E8E4DA;

    --color-text-dark: #333333;
    --color-text-sub: #555555;
    --color-text-muted: #777777;
    --color-text-light: #999999;

    /* Accents & System Colours */
    --color-warning: #F9A641;
    --color-warning-bg: #FFF3E0;
    --color-success: #157A4F;
    --color-success-bg: #E8F5EF;
    --color-error: #E04F4D;
    --color-error-bg: #FDF2F2;

    /* Ambient Hero Gradient (golowebapp.vercel.app golden banner) */
    --color-bg-base: #F8F6F2;
    --color-bg-ambient: linear-gradient(180deg, #F9D087 0%, #FBE6BC 25%, #FAF4E8 65%, #F8F6F2 100%);
    --color-brand-gradient: linear-gradient(135deg, #F5B849 0%, #F9A641 50%, #FF9800 100%);
    --color-dashed-border: rgba(245, 184, 73, 0.45);

    /* Shadows with Warm Amber Tone */
    --shadow-search: 0 10px 30px rgba(245, 184, 73, 0.15), 0 2px 8px rgba(0, 0, 0, 0.04);
    --shadow-search-focus: 0 14px 40px rgba(245, 184, 73, 0.28), 0 0 0 3px rgba(245, 184, 73, 0.25);
    --shadow-card: 0 8px 30px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.02);
    --shadow-card-hover: 0 16px 40px rgba(245, 184, 73, 0.20), 0 4px 12px rgba(0, 0, 0, 0.04);
}'''

    css, c1 = re.subn(root_old, root_new, css, flags=re.DOTALL)
    print("Updated :root in style.css:", c1)

    # 2. Update .btn-send
    btn_send_old = r'''\.btn-send \{.*?background:\s*#157A4F;.*?box-shadow:\s*0 4px 12px rgba\(21, 122, 79, 0\.35\);\s*\}'''
    btn_send_new = '''.btn-send {
    background: linear-gradient(135deg, #F5B849 0%, #F9A641 100%);
    color: #1F2937;
    border: none;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 14px rgba(245, 184, 73, 0.45);
}'''
    css, c2 = re.subn(btn_send_old, btn_send_new, css, flags=re.DOTALL)
    print("Updated .btn-send in style.css:", c2)

    # Update .btn-send:hover
    btn_send_hover_old = r'''\.btn-send:hover \{.*?background:\s*#0E5E3B;.*?box-shadow:\s*0 6px 16px rgba\(21, 122, 79, 0\.45\);\s*\}'''
    btn_send_hover_new = '''.btn-send:hover {
    background: #E59819;
    color: #111827;
    transform: scale(1.04);
    box-shadow: 0 6px 18px rgba(245, 184, 73, 0.55);
}'''
    css, c3 = re.subn(btn_send_hover_old, btn_send_hover_new, css, flags=re.DOTALL)
    print("Updated .btn-send:hover in style.css:", c3)

    # 3. Update .btn-signin
    btn_signin_old = r'''\.btn-signin \{.*?background:\s*#0F172A;.*?color:\s*#FFFFFF;.*?\}'''
    btn_signin_new = '''.btn-signin {
    background: #F5B849;
    color: #1F2937;
    border: none;
    padding: 8px 18px;
    border-radius: 8px;
    font-family: var(--font-sans);
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 3px 10px rgba(245, 184, 73, 0.35);
}'''
    css, c4 = re.subn(btn_signin_old, btn_signin_new, css, flags=re.DOTALL)
    print("Updated .btn-signin in style.css:", c4)

    # 4. Update .headline-purple
    head_old = r'''\.headline-purple \{.*?color:\s*#157A4F;.*?\}'''
    head_new = '''.headline-purple {
    color: #D97706;
    background: linear-gradient(135deg, #B45309 0%, #D97706 45%, #F5B849 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}'''
    css, c5 = re.subn(head_old, head_new, css, flags=re.DOTALL)
    print("Updated .headline-purple in style.css:", c5)

    # 5. Update user chat bubble & avatar
    chat_user_old = r'''\.chat-avatar\.user-av \{.*?background:\s*#333333;.*?color:\s*#FFFFFF;\s*\}'''
    chat_user_new = '''.chat-avatar.user-av {
    background: #333333;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 0.95rem;
    font-family: var(--font-sans);
    letter-spacing: 0.5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
}'''
    css, c6 = re.subn(chat_user_old, chat_user_new, css, flags=re.DOTALL)
    print("Updated .chat-avatar.user-av in style.css:", c6)

    # User chat bubble
    bubble_user_old = r'''\.chat-msg\.user \.chat-bubble \{.*?background:\s*#157A4F;.*?\}'''
    bubble_user_new = '''.chat-msg.user .chat-bubble {
    background: #F5B849;
    color: #1F2937;
    font-weight: 500;
    border-radius: 14px 14px 2px 14px;
    box-shadow: 0 2px 10px rgba(245, 184, 73, 0.25);
}'''
    css, c7 = re.subn(bubble_user_old, bubble_user_new, css, flags=re.DOTALL)
    print("Updated .chat-msg.user .chat-bubble in style.css:", c7)

    # 6. Top hero dashed border and card borders
    css = re.sub(r'border: 1.5px dashed var\(--color-dashed-border\);', 'border: 1.5px dashed var(--color-dashed-border);', css)

    with open(path, "w", encoding="utf-8") as f:
        f.write(css)
    print("frontend/style.css written successfully.")


def update_index_html():
    path = "frontend/index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Replace Language Modal
    modal_old = r'''<!-- ===============================================================\s*LANGUAGE SELECTOR MODAL \(105 LANGUAGES\)\s*=============================================================== -->.*?</div>\s*</div>\s*<!-- ===============================================================\s*BENCHMARK'''
    
    modal_new = '''<!-- ===============================================================
         LANGUAGE SELECTOR MODAL (English, Hindi, Marathi)
         =============================================================== -->
    <div class="results-overlay" id="languageOverlay" onclick="closeLanguageModal(event)">
        <div class="signin-modal" style="max-width: 560px; width: 95%;" onclick="event.stopPropagation()">
            <button class="btn-close-modal" onclick="closeLanguageModal()">✕</button>
            <div class="signin-header" style="text-align: left; margin-bottom: 1.25rem;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    <span style="font-size: 1.6rem;">🌐</span>
                    <h2 style="font-size: 1.35rem; font-weight: 800; color: #1F2937; margin: 0;">Language Preferences</h2>
                </div>
                <p style="color: #64748B; font-size: 0.9rem; margin-top: 4px; line-height: 1.5;">
                    Select your active language. GoLo AI will answer all your questions in your preferred language.
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.25rem;" id="languageGrid">
                <!-- Populated dynamically via script.js (English, Hindi, Marathi) -->
            </div>

            <div style="background: #FEF8EC; border: 1.5px solid #FCE4B8; padding: 14px 16px; border-radius: 12px; font-size: 0.88rem; color: #4B5563; margin-bottom: 1.5rem;" id="langSampleDisplay">
                <div style="font-weight: 700; color: #B87B10; margin-bottom: 4px;" id="langSelectedHeader">Selected Language: English</div>
                <div style="font-style: italic; color: #374151;" id="langSelectedQuote">"Ask anything. Get instant intelligent answers."</div>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 10px; align-items: center;">
                <button type="button" class="btn-cancel-lang" onclick="closeLanguageModal()" style="background: transparent; border: 1px solid #D1D5DB; color: #4B5563; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer;">Cancel</button>
                <button type="button" class="btn-save-lang" id="btnSaveLanguage" onclick="saveSelectedLanguage()" style="background: #F5B849; color: #1F2937; border: none; padding: 10px 24px; border-radius: 8px; font-weight: 700; font-size: 0.95rem; cursor: pointer; box-shadow: 0 4px 12px rgba(245, 184, 73, 0.4); display: inline-flex; align-items: center; gap: 8px;">
                    <span>💾 Save Language</span>
                </button>
            </div>
        </div>
    </div>

    <!-- ===============================================================
         BENCHMARK'''

    html, c1 = re.subn(modal_old, modal_new, html, flags=re.DOTALL)
    print("Updated Language Modal in index.html:", c1)

    # 2. Update Pillar 4 text
    pillar_old = r'''<!-- Pillar 4: Global Languages -->.*?<h4 class="pillar-title">Global Languages</h4>\s*<p class="pillar-desc">.*?</p>\s*</div>'''
    pillar_new = '''<!-- Pillar 4: Active Language Preferences -->
                            <div class="pillar-item" onclick="openLanguageModal()" style="cursor: pointer;" title="Select Language Preferences">
                                <div class="pillar-icon-circle">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                        <rect x="2" y="4" width="20" height="16" rx="4" fill="#F5B849"/>
                                        <text x="6" y="15.5" fill="#1F2937" font-family="'Inter', -apple-system, sans-serif" font-size="9" font-weight="700">A</text>
                                        <path d="M14 8h5M16.5 8v2M14 11h5M18 11c-.5 2.5-2 4.5-4 5.5M15.5 13.5c1 1.5 2 2.5 3.5 3" stroke="#1F2937" stroke-width="1.2" stroke-linecap="round"/>
                                    </svg>
                                </div>
                                <h4 class="pillar-title">Active Languages</h4>
                                <p class="pillar-desc">Native support for English, Hindi (हिन्दी), and Marathi (मराठी) with step-by-step reasoning.</p>
                            </div>'''

    html, c2 = re.subn(pillar_old, pillar_new, html, flags=re.DOTALL)
    print("Updated Pillar 4 in index.html:", c2)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("frontend/index.html written successfully.")


def update_script_js():
    path = "frontend/script.js"
    with open(path, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. User avatar in chat message: replace 👤 with A
    user_av_old = r'''<div class="chat-avatar user-av">👤</div>'''
    user_av_new = '''<div class="chat-avatar user-av">A</div>'''
    js, c1 = re.subn(user_av_old, user_av_new, js)
    print("Updated chat-avatar user-av in script.js:", c1)

    # 2. Update Language selection & modal logic (Only 3 languages: English, Hindi, Marathi)
    lang_section_old = r'''// ==========================================================================\s*// PILLAR 4 & NAV: GLOBAL LANGUAGES\s*// ==========================================================================.*?function selectLanguage\(langName\) \{.*?setTimeout\(\(\) => closeLanguageModal\(\), 300\);\s*\}'''

    lang_section_new = '''// ==========================================================================
// PILLAR 4 & NAV: ACTIVE LANGUAGE PREFERENCES (ENGLISH, HINDI, MARATHI)
// ==========================================================================
let pendingSelectedLanguage = currentSelectedLanguage || 'English';

const SUPPORTED_LANGUAGES = [
    { code: 'en', name: 'English', native: 'English', flag: '🇬🇧', label: 'Global', greeting: 'Ask anything. Get instant intelligent answers.' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी', flag: '🇮🇳', label: 'राजभाषा', greeting: 'कुछ भी पूछें। समझदार और सटीक उत्तर पाएं।' },
    { code: 'mr', name: 'Marathi', native: 'मराठी', flag: '🇮🇳', label: 'प्रादेशिक', greeting: 'काहीही विचारा. बुद्धिमान आणि अचूक उत्तरे मिळवा.' }
];

const LANGUAGE_LOCALE_MAP = {
    'English': 'en-US',
    'Hindi': 'hi-IN',
    'Marathi': 'mr-IN'
};

async function preloadLanguageList() {
    // Check saved local preference
    const saved = localStorage.getItem('golo_selected_language');
    if (saved && (saved === 'English' || saved === 'Hindi' || saved === 'Marathi')) {
        currentSelectedLanguage = saved;
        pendingSelectedLanguage = saved;
    }
    renderLanguageCards();
    updateLanguageUIState();
}

function renderLanguageCards() {
    const grid = document.getElementById('languageGrid');
    if (!grid) return;

    grid.innerHTML = SUPPORTED_LANGUAGES.map(l => {
        const isSelected = (pendingSelectedLanguage === l.name);
        return `
            <div class="lang-choice-card ${isSelected ? 'active-lang' : ''}" 
                 onclick="choosePendingLanguage('${l.name}')" 
                 style="border: 2px solid ${isSelected ? '#F5B849' : '#E5E7EB'}; background: ${isSelected ? '#FEF8EC' : '#FFFFFF'}; border-radius: 12px; padding: 14px 10px; cursor: pointer; text-align: center; transition: all 0.2s ease; position: relative;">
                ${isSelected ? '<span style="position: absolute; top: 6px; right: 8px; font-size: 0.85rem; color: #D97706; font-weight: 800;">✓</span>' : ''}
                <div style="font-size: 1.8rem; margin-bottom: 4px;">${l.flag}</div>
                <div style="font-weight: 700; font-size: 0.95rem; color: #1F2937;">${l.name}</div>
                <div style="font-size: 0.85rem; color: #6B7280; margin-top: 2px; font-weight: 600;">${l.native}</div>
                <span style="display: inline-block; margin-top: 6px; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 999px; background: ${isSelected ? '#FCE4B8' : '#F3F4F6'}; color: ${isSelected ? '#92400E' : '#4B5563'};">${l.label}</span>
            </div>
        `;
    }).join('');

    const matched = SUPPORTED_LANGUAGES.find(l => l.name === pendingSelectedLanguage) || SUPPORTED_LANGUAGES[0];
    const headerEl = document.getElementById('langSelectedHeader');
    const quoteEl = document.getElementById('langSelectedQuote');
    if (headerEl) headerEl.innerText = `Selected Language: ${matched.name} (${matched.native})`;
    if (quoteEl) quoteEl.innerText = `"${matched.greeting}"`;
}

function choosePendingLanguage(langName) {
    pendingSelectedLanguage = langName;
    renderLanguageCards();
}

function openLanguageModal(event) {
    if (event) event.preventDefault();
    pendingSelectedLanguage = currentSelectedLanguage;
    renderLanguageCards();
    document.getElementById('languageOverlay').style.display = 'flex';
}

function closeLanguageModal(event) {
    if (event && event.target !== event.currentTarget && !event.target.classList.contains('btn-close-modal') && !event.target.classList.contains('btn-cancel-lang')) return;
    document.getElementById('languageOverlay').style.display = 'none';
}

function saveSelectedLanguage() {
    currentSelectedLanguage = pendingSelectedLanguage;
    localStorage.setItem('golo_selected_language', currentSelectedLanguage);
    currentLanguageCode = LANGUAGE_LOCALE_MAP[currentSelectedLanguage] || 'en-US';

    if (speechRecognizer) {
        speechRecognizer.lang = currentLanguageCode;
    }

    updateLanguageUIState();
    document.getElementById('languageOverlay').style.display = 'none';
    showToast(`🌐 Language saved: ${currentSelectedLanguage}. Next answers will be generated in ${currentSelectedLanguage}!`);
}

function updateLanguageUIState() {
    const navBtn = document.getElementById('btnLangSelect');
    if (navBtn) {
        const matched = SUPPORTED_LANGUAGES.find(l => l.name === currentSelectedLanguage) || SUPPORTED_LANGUAGES[0];
        navBtn.innerHTML = `
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #FEF8EC; border: 1.5px solid #FCE4B8; border-radius: 9999px; font-size: 0.88rem; font-weight: 700; color: #92400E; cursor: pointer;">
                <span>${matched.flag}</span>
                <span>${matched.native}</span>
                <span style="font-size: 0.7rem; color: #B45309;">▾</span>
            </span>
        `;
        navBtn.style.width = 'auto';
        navBtn.style.height = 'auto';
        navBtn.style.background = 'transparent';
    }

    const statusNote = document.getElementById('assistantStatusNote');
    if (statusNote) {
        statusNote.innerText = `Active Language: ${currentSelectedLanguage} • Dual-Path RAG • Grounded Output`;
    }
}'''

    js, c2 = re.subn(lang_section_old, lang_section_new, js, flags=re.DOTALL)
    print("Updated language section in script.js:", c2)

    # 3. Enhance generateClientFallbackAnswer for Hindi and Marathi
    fb_old = r'''function generateClientFallbackAnswer\(query\) \{'''
    fb_new = '''function generateClientFallbackAnswer(query) {
    const lang = (currentSelectedLanguage || 'English').toLowerCase();
    const isHi = lang === 'hindi' || lang === 'hi';
    const isMr = lang === 'marathi' || lang === 'mr';

    if (isHi) {
        const ql = query.toLowerCase();
        if (ql.includes('logout') || ql.includes('log out') || ql.includes('sign out')) {
            return { faq_id: 163, category: 'Account FAQ', source: 'faq', answer: '**GOLO खाते से लॉग आउट करने की सुरक्षित प्रक्रिया:**\\n\\n1. **चरण 1:** शीर्ष नेविगेशन बार में अपने **Profile Avatar (Alex Merchant)** पर क्लिक करें।\\n2. **चरण 2:** मेनू में से **Log Out / Sign Out** चुनें।\\n3. **चरण 3:** आपका प्रमाणीकरण सत्र तुरंत समाप्त हो जाएगा।' };
        }
        if (ql.includes('product') || ql.includes('item') || ql.includes('listing')) {
            return { faq_id: 66, category: 'Product FAQ', source: 'faq', answer: '**GOLO पर नया उत्पाद जोड़ने की प्रक्रिया:**\\n\\n1. **चरण 1:** मर्चेंट पोर्टल में **Catalog → Products** खोलें।\\n2. **चरण 2:** **Add Product** बटन दबाएं।\\n3. **चरण 3:** उत्पाद का नाम, श्रेणी, मूल्य और स्टॉक दर्ज करें।\\n4. **चरण 4:** स्पष्ट तस्वीरें अपलोड करके **Publish** पर क्लिक करें।' };
        }
        if (ql.includes('payout') || ql.includes('settlement') || ql.includes('money') || ql.includes('payment')) {
            return { faq_id: 176, category: 'Payment FAQ', source: 'faq', answer: '**GOLO मर्चेंट पेआउट और निपटान चक्र:**\\n\\n• **निपटान चक्र:** T+2 / T+3 कार्य दिवस।\\n• **न्यूनतम पेआउट:** ₹500 शुद्ध आय।\\n• **भुगतान विधि:** सीधे पंजीकृत बैंक खाते में सुरक्षित NEFT/RTGS स्थानांतरण।' };
        }
        if (ql.includes('support') || ql.includes('care') || ql.includes('help') || ql.includes('contact')) {
            return { faq_id: 175, category: 'Customer Support', source: 'customer_support', answer: '**GOLO मर्चेंट कस्टमर सपोर्ट सहायता (२४/७ उपलब्ध):**\\n\\n• **टोल-फ्री:** `1800-267-4656` (सुबह ९:०० से रात ९:०० IST)\\n• **ईमेल:** `support@golo.com`\\n• **लाइव टिकट:** तुरंत समाधान के लिए Create Ticket पर क्लिक करें।' };
        }
        return { faq_id: 1, category: 'General GOLO FAQ', source: 'faq', answer: '**GOLO** एक अग्रणी हाइपर-लोकल खोज और रिटेल बचत प्लेटफ़ॉर्म है, जिसे **NexaPrime Ecosystem** द्वारा संचालित किया जाता है। यह स्थानीय दुकानदारों और ग्राहकों को डिजिटल स्टोरफ़्रंट और क्यूआर कोड वाउचर छूट से जोड़ता है।' };
    }

    if (isMr) {
        const ql = query.toLowerCase();
        if (ql.includes('logout') || ql.includes('log out') || ql.includes('sign out')) {
            return { faq_id: 163, category: 'Account FAQ', source: 'faq', answer: '**GOLO खात्यामधून सुरक्षितपणे लॉग आउट करण्याची प्रक्रिया:**\\n\\n1. **पायरी १:** वरच्या नेव्हिगेशन बारमधील तुमच्या **Profile Avatar (Alex Merchant)** वर क्लिक करा.\\n2. **पायरी २:** मेनूमधून **Log Out / Sign Out** पर्याय निवडा.\\n3. **पायरी ३:** तुमचे प्रमाणीकरण सत्र त्वरित बंद होईल.' };
        }
        if (ql.includes('product') || ql.includes('item') || ql.includes('listing')) {
            return { faq_id: 66, category: 'Product FAQ', source: 'faq', answer: '**GOLO वर नवीन उत्पादन जोडण्याची सोपी पद्धत:**\\n\\n1. **पायरी १:** मर्चंट पोर्टलवर **Catalog → Products** उघडा.\\n2. **पायरी २:** **Add Product** बटण दाबा.\\n3. **पायरी ३:** उत्पादनाचे नाव, श्रेणी, किंमत व उपलब्ध स्टॉक प्रविष्ट करा.\\n4. **पायरी ४:** स्पष्ट फोटो अपलोड करून **Publish** दाबा.' };
        }
        if (ql.includes('payout') || ql.includes('settlement') || ql.includes('money') || ql.includes('payment')) {
            return { faq_id: 176, category: 'Payment FAQ', source: 'faq', answer: '**GOLO मर्चंट्ससाठी पेआउट आणि सेटलमेंट सायकल:**\\n\\n• **सेटलमेंट सायकल:** T+2 / T+3 व्यावसायिक दिवस.\\n• **किमान पेआउट:** ₹500 शुद्ध उत्पन्न.\\n• **पद्धत:** थेट नोंदणीकृत बँक खात्यात NEFT/RTGS द्वारे सुरक्षित ट्रान्सफर.' };
        }
        if (ql.includes('support') || ql.includes('care') || ql.includes('help') || ql.includes('contact')) {
            return { faq_id: 175, category: 'Customer Support', source: 'customer_support', answer: '**GOLO मर्चंट कस्टमर सपोर्ट सहाय्य (२४/७ उपलब्ध):**\\n\\n• **टोल-फ्री:** `1800-267-4656` (सकाळी ९:०० ते रात्री ९:०० IST)\\n• **ईमेल:** `support@golo.com`\\n• **लाइव्ह तिकीट:** तांत्रिक मदतीसाठी Create Ticket बटणावर क्लिक करा.' };
        }
        return { faq_id: 1, category: 'General GOLO FAQ', source: 'faq', answer: '**GOLO** हे एक अग्रगण्य हायपर-लोकल शोध आणि रिटेल सेव्हिंग्स प्लॅटफॉर्म आहे, जे **NexaPrime Ecosystem** द्वारे चालवले जाते. हे स्थानिक दुकानदार आणि ग्राहकांना डिजिटल स्टोअरफ्रंट आणि QR कोड व्हाउचर सवलतींद्वारे जोडते.' };
    }
'''
    js, c3 = re.subn(fb_old, fb_new, js)
    print("Updated fallback answer in script.js:", c3)

    with open(path, "w", encoding="utf-8") as f:
        f.write(js)
    print("frontend/script.js written successfully.")


if __name__ == '__main__':
    update_style_css()
    update_index_html()
    update_script_js()
