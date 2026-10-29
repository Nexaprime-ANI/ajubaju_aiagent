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
            if ('webkitSpeechRecognition' in wind