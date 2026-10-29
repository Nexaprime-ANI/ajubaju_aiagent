
        // ─── Theme Management (Light mode default) ───
        const htmlEl = document.documentElement;
        const themeBtn = document.getElementById('themeToggleBtn');
        const themeIcon = document.getElementById('themeIcon');

        function setTheme(theme) {
            htmlEl.setAttribute('data-theme', theme);
            localStorage.setItem('golo_theme', theme);
            themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }

        const savedTheme = localStorage.getItem('golo_theme') || 'light';
        setTheme(savedTheme);

        themeBtn.addEventListener('click', () => {
            const current = htmlEl.getAttribute('data-theme');
            setTheme(current === 'dark' ? 'light' : 'dark');
        });

        // ─── Window Modal Controls & Back Button ───
        const assistantOverlay = document.getElementById('assistantOverlay');
        const startChattingBtn = document.getElementById('startChattingBtn');
        const floatingChatLauncher = document.getElementById('floatingChatLauncher');
        const windowBackBtn = document.getElementById('windowBackBtn');
        const winCloseBtn = document.getElementById('winCloseBtn');
        const winMinimizeBtn = document.getElementById('winMinimizeBtn');
        const winMaximizeBtn = document.getElementById('winMaximizeBtn');
        const windowFrame = document.querySelector('.window-frame');

        function openAssistant() {
            assistantOverlay.classList.add('active');
            floatingChatLauncher.style.display = 'none';
            setTimeout(() => {
                document.getElementById('chatInput').focus();
            }, 300);
        }

        function closeAssistant() {
            assistantOverlay.classList.remove('active');
            floatingChatLauncher.style.display = 'flex';
        }

        startChattingBtn.addEventListener('click', openAssistant);
        floatingChatLauncher.addEventListener('click', openAssistant);
        windowBackBtn.addEventListener('click', closeAssistant);
        winCloseBtn.addEventListener('click', closeAssistant);
        winMinimizeBtn.addEventListener('click', closeAssistant);

        let isMaximized = false;
        winMaximizeBtn.addEventListener('click', () => {
            isMaximized = !isMaximized;
            if (isMaximized) {
                windowFrame.style.maxWidth = '100vw';
                windowFrame.style.height = '100vh';
                windowFrame.style.borderRadius = '0';
            } else {
                windowFrame.style.maxWidth = '1080px';
                windowFrame.style.height = '680px';
                windowFrame.style.borderRadius = '20px';
            }
        });

        // Close on Esc key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && assistantOverlay.classList.contains('active')) {
                closeAssistant();
            }
        });

        // ─── Header Status Pill Management ───
        const headerStatusBadge = document.getElementById('headerStatusBadge');
        const statusIcon = document.getElementById('statusIcon');
        const statusText = document.getElementById('statusText');

        function setHeaderStatus(state) {
            headerStatusBadge.className = 'header-status-badge';
            if (state === 'success') {
                headerStatusBadge.classList.add('status-success');
                statusIcon.textContent = '✔';
                statusText.textContent = 'Success';
            } else if (state === 'error' || state === 'out_of_scope') {
                headerStatusBadge.classList.add('status-error');
                statusIcon.textContent = '⚠️';
                statusText.textContent = 'Out of Scope';
            } else if (state === 'offline') {
                headerStatusBadge.classList.add('status-offline');
                statusIcon.textContent = '📶';
                statusText.textContent = 'No Network';
            } else {
                headerStatusBadge.classList.add('status-idle');
                statusIcon.textContent = '●';
                statusText.textContent = 'Active';
            }
        }

        // ─── Sidebar Navigation Tabs ───
        function switchSidebarTab(tabId) {
            document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
            const activeEl = document.getElementById('tab' + tabId.charAt(0).toUpperCase() + tabId.slice(1));
            if (activeEl) activeEl.classList.add('active');

            if (tabId === 'insights' || tabId === 'reports') {
                submitQueryText("Show me today's sales report");
            } else if (tabId === 'orders') {
                submitQueryText("How do I manage and track customer orders?");
            } else if (tabId === 'inventory') {
                submitQueryText("How do I check and update my inventory stock?");
            } else if (tabId === 'customers') {
                submitQueryText("How do I manage customer inquiries and reviews?");
            } else if (tabId === 'settings') {
                submitQueryText("How do I update my store settings and bank details?");
            }
        }

        // ─── Time Formatter ───
        function getCurrentTimeStr() {
            const now = new Date();
            let hours = now.getHours();
            const minutes = now.getMinutes();
            const ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12 || 12;
            const minsStr = minutes < 10 ? '0' + minutes : minutes;
            return `${hours}:${minsStr} ${ampm}`;
        }

        // ─── Accurate Robot Animations (Typing, Processing, Success, Error) ───
        const conversationArea = document.getElementById('conversationArea');
        const dynamicRobotStage = document.getElementById('dynamicRobotStage');
        const chatInput = document.getElementById('chatInput');

        let typingTimeout = null;

        // 1. TYPING STATE ANIMATION:
        // Shows typing robot with laptop and bouncing dots when user types
        chatInput.addEventListener('input', () => {
            const val = chatInput.value.trim();
            if (val.length > 0) {
                showTypingRobot();
                clearTimeout(typingTimeout);
                typingTimeout = setTimeout(() => {
                    // Keep visible or wait
                }, 3500);
            } else {
                clearDynamicStage();
            }
        });

        function showTypingRobot() {
            dynamicRobotStage.innerHTML = `
                <div class="typing-robot-widget">
                    <div class="typing-sprite-wrap">
                        <img src="robot_typing_transparent_2x.png" alt="Golo AI is typing" class="typing-sprite-img">
                    </div>
                </div>
            `;
            conversationArea.scrollTop = conversationArea.scrollHeight;
        }

        // 2. PROCESSING STATE ANIMATION:
        // Shows centered robot with spinning gear, orbital rings, and "Processing your request..."
        function showProcessingRobot() {
            dynamicRobotStage.innerHTML = `
                <div class="processing-robot-widget">
                    <div class="proc-sprite-wrap">
                        <img src="robot_proc_transparent_2x.png" alt="Processing request" class="proc-sprite-img">
                    </div>
                    <div class="proc-capsule">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        <span>Processing your request</span>
                        <div class="proc-dots"><span>.</span><span>.</span><span>.</span></div>
                    </div>
                </div>
            `;
            conversationArea.scrollTop = conversationArea.scrollHeight;
        }

        // 3. ERROR / OUT-OF-SCOPE / NO NETWORK ANIMATION:
        // Shows robot with sad expression, glowing red aura, and pulsing exclamation mark badge
        function showErrorRobot(message, isOffline = false) {
            setHeaderStatus(isOffline ? 'offline' : 'out_of_scope');
            dynamicRobotStage.innerHTML = `
                <div class="error-robot-widget">
                    <div class="error-sprite-wrap">
                        <img src="robot_error_transparent_2x.png" alt="Error or Out of Scope" class="error-sprite-img">
                    </div>
                    <div class="error-card-bubble">
                        ${message}
                        <div class="quick-suggestions" style="justify-content: center; margin-top: 1rem;">
                            <button type="button" class="suggestion-chip" onclick="submitQueryText('Show me today\'s sales report')">📊 Sales Report</button>
                            <button type="button" class="suggestion-chip" onclick="submitQueryText('How do I log out of my GOLO account?')">🚪 How to Log Out</button>
                            <button type="button" class="suggestion-chip" onclick="submitQueryText('How do I track and fulfill orders?')">📦 Order Tracking</button>
                        </div>
                    </div>
                </div>
            `;
            conversationArea.scrollTop = conversationArea.scrollHeight;
        }

        function clearDynamicStage() {
            dynamicRobotStage.innerHTML = '';
        }

        // ─── In-Chat Message Rendering ───
        function appendUserMessage(text) {
            const timeStr = getCurrentTimeStr();
            const row = document.createElement('div');
            row.className = 'message-row user-row';
            row.innerHTML = `
                <div class="avatar-box user-avatar-circle">U</div>
                <div class="bubble-wrap">
                    <div class="message-bubble">${escapeHtml(text)}</div>
                    <span class="message-time">${timeStr}</span>
                </div>
            `;
            conversationArea.insertBefore(row, dynamicRobotStage);
            conversationArea.scrollTop = conversationArea.scrollHeight;
        }

        function appendSuccessAnswer(answerText, isSalesReport = false, source = 'GOLO Verified Knowledge Base') {
            setHeaderStatus('success');
            clearDynamicStage();

            const timeStr = getCurrentTimeStr();
            const row = document.createElement('div');
            row.className = 'message-row ai-row';

            if (isSalesReport) {
                // Exact Sales Report Card from Reference Image
                row.innerHTML = `
                    <div class="avatar-box">
                        <img src="robot_avatar_2x.png" alt="Golo AI">
                    </div>
                    <div class="bubble-wrap">
                        <div class="message-bubble">
                            Here is your today's sales report:
                            <div class="sales-report-card">
                                <div class="sales-top-row">
                                    <div>
                                        <div class="metric-title">Total Sales</div>
                                        <div class="metric-big-val">₹ 1,25,000</div>
                                        <div class="metric-badge">
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="18 15 12 9 6 15"></polyline></svg>
                                            32%
                                        </div>
                                    </div>
                                    <svg class="sparkline-svg" viewBox="0 0 130 48" fill="none">
                                        <defs>
                                            <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.35"/>
                                                <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.0"/>
                                            </linearGradient>
                                        </defs>
                                        <path d="M5 38 C 25 36, 40 42, 60 28 C 80 14, 95 24, 115 10 L 115 48 L 5 48 Z" fill="url(#sparkGrad)" />
                                        <path d="M5 38 C 25 36, 40 42, 60 28 C 80 14, 95 24, 115 10" stroke="#2563eb" stroke-width="3" stroke-linecap="round" fill="none"/>
                                        <circle cx="115" cy="10" r="4.5" fill="#2563eb" stroke="#ffffff" stroke-width="2"/>
                                    </svg>
                                </div>
                                <div class="sales-subgrid">
                                    <div class="sub-metric-box">
                                        <span class="sub-metric-lbl">Total Orders</span>
                                        <span class="sub-metric-num">248</span>
                                        <span class="sub-metric-trend">↑ 18%</span>
                                    </div>
                                    <div class="sub-metric-box">
                                        <span class="sub-metric-lbl">New Customers</span>
                                        <span class="sub-metric-num">156</span>
                                        <span class="sub-metric-trend">↑ 24%</span>
                                    </div>
                                    <div class="sub-metric-box">
                                        <span class="sub-metric-lbl">Top Product</span>
                                        <div class="product-tag">
                                            <span>🎧</span>
                                            <span>Wireless Earbuds</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top: 0.75rem; font-size: 0.88rem; color: var(--text-muted);">
                                You can view the detailed report in the <strong>Reports</strong> section.
                            </div>
                        </div>
                        <span class="message-time">${timeStr}</span>
                    </div>
                `;
            } else {
                // Formatted Step-by-Step Knowledge Base Answer
                const formattedHtml = formatAnswerHtml(answerText);
                row.innerHTML = `
                    <div class="avatar-box">
                        <img src="robot_avatar_2x.png" alt="Golo AI">
                    </div>
                    <div class="bubble-wrap">
                        <div class="message-bubble">
                            <div class="step-guidance-content">${formattedHtml}</div>
                            <div class="source-tag">
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                                ${escapeHtml(source)}
                            </div>
                        </div>
                        <span class="message-time">${timeStr}</span>
                    </div>
                `;
            }

            conversationArea.insertBefore(row, dynamicRobotStage);
            conversationArea.scrollTop = conversationArea.scrollHeight;

            if (ttsEnabled) {
                speakText(answerText);
            }
        }

        // ─── Query Dispatcher (FastAPI RAG Backend + Client Deterministic Engine) ───
        async function handleFormSubmit(e) {
            e.preventDefault();
            const text = chatInput.value.trim();
            if (!text) return;
            chatInput.value = '';
            submitQueryText(text);
        }

        function launchAssistantWithQuery(text) {
            openAssistant();
            setTimeout(() => {
                submitQueryText(text);
            }, 350);
        }

        async function submitQueryText(query) {
            appendUserMessage(query);
            showProcessingRobot();

            // Check if asking for sales insights or report
            const norm = query.toLowerCase();
            const isSales = norm.includes('sales report') || norm.includes('sales insight') || norm.includes("today's sales") || norm.includes('show me today');

            try {
                // 1. Send to Live FastAPI Backend
                const response = await fetch('http://127.0.0.1:8000/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });

                if (!response.ok) {
                    throw new Error('Server returned ' + response.status);
                }

                const data = await response.json();
                
                // Check if out of scope
                if (data.source === 'out_of_scope' || data.source === 'Safety Filter' || (data.category === 'Out of Scope')) {
                    setTimeout(() => {
                        showErrorRobot(data.response || "This question is not related to the GOLO merchant platform. I can only assist with GOLO store management, orders, inventory, products, payments, refunds, KYC verification, and account settings.", false);
                    }, 500);
                    return;
                }

                // If sales query, render the exact sales report card from screenshot
                setTimeout(() => {
                    appendSuccessAnswer(data.response, isSales, data.source || 'GOLO Knowledge Base');
                }, 600);

            } catch (err) {
                console.warn('FastAPI backend offline or fetch error, using client deterministic RAG fallback:', err);
                // Fallback Deterministic Local Matching
                setTimeout(() => {
                    processClientFallback(query, isSales);
                }, 700);
            }
        }

        // ─── Client Deterministic RAG Fallback ───
        function processClientFallback(query, isSales) {
            const lower = query.toLowerCase();

            // Out-of-scope filter
            const GOLO_KEYWORDS = [
                'golo', 'product', 'listing', 'order', 'payment', 'payout', 'bank', 'kyc',
                'refund', 'credit note', 'merchant', 'store', 'customer', 'report', 'sales',
                'inventory', 'stock', 'catalog', 'category', 'voucher', 'coupon', 'discount',
                'gst', 'invoice', 'log out', 'logout', 'sign out', 'signout', 'password',
                'account', 'settlement', 'shipping', 'delivery', 'pickup', 'return', 'fee'
            ];

            const hasKeyword = GOLO_KEYWORDS.some(k => lower.includes(k));
            if (!hasKeyword) {
                showErrorRobot("This question is not related to the GOLO merchant platform. I can only help with GOLO store features like orders, inventory, products, payments, refunds, KYC verification, and account settings.", false);
                return;
            }

            // Sales Report
            if (isSales) {
                appendSuccessAnswer("Here is your today's sales report:", true);
                return;
            }

            // Logout
            if (lower.includes('log out') || lower.includes('logout') || lower.includes('sign out')) {
                const logoutAnswer = `To log out of your GOLO account:
1. Click on your **Profile Avatar / Account Icon** in the top navigation bar.
2. In the user menu dropdown, select **Log Out** (or **Sign Out**).
3. Your active authentication session will be cleared immediately and you will return to the login screen.

*Tip: Never share your OTP or session passwords.*`;
                appendSuccessAnswer(logoutAnswer, false);
                return;
            }

            // Credit Note
            if (lower.includes('credit note') || lower.includes('refund')) {
                const cnAnswer = `GOLO Credit Note & Refund Procedure:
1. Go to **Orders > Manage Returns & Refunds**.
2. Select the specific Order ID and click **Issue Credit Note**.
3. Enter the amount to credit and select the reason.
4. The credit note is instantly emailed to the customer and recorded in your **Financial Statements**.`;
                appendSuccessAnswer(cnAnswer, false);
                return;
            }

            // Product Listing
            if (lower.includes('product') || lower.includes('add product') || lower.includes('list')) {
                const prodAnswer = `To add a new product to your GOLO store:
1. Open your Merchant Dashboard and navigate to **Products > Add Product**.
2. Enter the Product Title, Brand, Category, and Description.
3. Upload clear product photos (minimum 800x800 px).
4. Specify pricing, SKU code, and available stock units.
5. Click **Publish** to make your product live immediately.`;
                appendSuccessAnswer(prodAnswer, false);
                return;
            }

            // KYC Verification
            if (lower.includes('kyc') || lower.includes('verify')) {
                const kycAnswer = `GOLO Merchant KYC Verification:
1. Go to **Settings > Merchant Profile > KYC Verification**.
2. Upload your GSTIN Certificate or PAN Card.
3. Upload a cancelled business cheque or bank statement showing your IFSC and Account Number.
4. GOLO compliance reviews documents within **24 business hours**.`;
                appendSuccessAnswer(kycAnswer, false);
                return;
            }

            // General Merchant Help
            const generalAnswer = `For your GOLO Merchant account:
• You can manage **Orders**, **Inventory**, and **Payments** from the left navigation.
• All settlements occur automatically every Tuesday.
• For urgent support, tap **Customer Support** or call our merchant hotline.`;
                appendSuccessAnswer(generalAnswer, false);
        }

        // ─── Text-to-Speech (Optional Voice) ───
        let ttsEnabled = false;
        const ttsToggleBtn = document.getElementById('ttsToggleBtn');
        ttsToggleBtn.addEventListener('click', () => {
            ttsEnabled = !ttsEnabled;
            ttsToggleBtn.style.color = ttsEnabled ? '#1a73e8' : 'var(--text-muted)';
            if (!ttsEnabled && window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        });

        function speakText(text) {
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel();
            const clean = text.replace(/[*#_]/g, '');
            const utter = new SpeechSynthesisUtterance(clean);
            utter.rate = 1.05;
            window.speechSynthesis.speak(utter);
        }

        // ─── Web Speech API Voice Recognition (Mic Button) ───
        const voiceMicBtn = document.getElementById('voiceMicBtn');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            let isListening = false;

            voiceMicBtn.addEventListener('click', () => {
                if (!isListening) {
                    try {
                        recognition.start();
                        isListening = true;
                        voiceMicBtn.classList.add('recording');
                        chatInput.placeholder = 'Listening to your question...';
                    } catch (e) {
                        console.error('Speech recognition error:', e);
                    }
                } else {
                    recognition.stop();
                    isListening = false;
                    voiceMicBtn.classList.remove('recording');
                    chatInput.placeholder = 'Ask any GOLO question...';
                }
            });

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                chatInput.value = transcript;
                voiceMicBtn.classList.remove('recording');
                isListening = false;
                chatInput.placeholder = 'Ask any GOLO question...';
                setTimeout(() => {
                    submitQueryText(transcript);
                }, 300);
            };

            recognition.onerror = () => {
                voiceMicBtn.classList.remove('recording');
                isListening = false;
                chatInput.placeholder = 'Ask any GOLO question...';
            };

            recognition.onend = () => {
                voiceMicBtn.classList.remove('recording');
                isListening = false;
                chatInput.placeholder = 'Ask any GOLO question...';
            };
        } else {
            voiceMicBtn.addEventListener('click', () => {
                alert('Voice speech recognition is not supported in this browser. Please use Chrome or Edge.');
            });
        }

        // ─── Helper Functions ───
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function formatAnswerHtml(text) {
            let html = escapeHtml(text);
            return html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        }

        // ─── Direct URL Query Parameter Handling for State Previews ───
        function checkUrlParams() {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('theme')) {
                setTheme(urlParams.get('theme'));
            }
            if (urlParams.has('open') || urlParams.has('state')) {
                openAssistant();
                const state = urlParams.get('state');
                if (state === 'typing') {
                    chatInput.value = "Show me today's sales report";
                    showTypingRobot();
                } else if (state === 'processing') {
                    appendUserMessage("Show me today's sales report");
                    showProcessingRobot();
                } else if (state === 'success') {
                    appendUserMessage("Show me today's sales report");
                    appendSuccessAnswer("Here is your today's sales report:", true);
                } else if (state === 'error' || state === 'out_of_scope') {
                    appendUserMessage("Who won the cricket match yesterday?");
                    showErrorRobot("This question is not related to the GOLO merchant platform. I can only assist with GOLO store management, orders, inventory, products, payments, refunds, KYC verification, and account settings.", false);
                } else if (state === 'offline') {
                    appendUserMessage("How do I fulfill customer orders?");
                    showErrorRobot("Oops! It seems there is no internet connection. Please check your network and try again.", true);
                }
            }
        }
        checkUrlParams();
    