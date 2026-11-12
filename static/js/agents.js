// AI PLACEMENT PRO - AI Placement Agents Client Controller

const AGENT_CONFIGS = {
  aptitude: {
    name: 'Aptitude Agent',
    icon: 'fa-calculator',
    gradient: 'linear-gradient(135deg, var(--primary), var(--secondary))',
    welcome: 'Hello! I am your Aptitude Preparation Agent. I coach you in **Quantitative Aptitude, Logical Reasoning, and Verbal Ability** with step-by-step mathematical solutions and timed shortcuts. Ask for practice questions or submit your solution for review!'
  },
  coding: {
    name: 'Coding Agent',
    icon: 'fa-code',
    gradient: 'linear-gradient(135deg, var(--accent-cyan), #3b82f6)',
    welcome: 'Welcome to the Algorithmic Lab! I am your Coding Agent. I assist with **Data Structures & Algorithms, Big-O Complexity, C, Python, Java**, and code debugging. Run code on the left or ask me to explain any algorithmic concept.'
  },
  technical: {
    name: 'Technical Interview Agent',
    icon: 'fa-server',
    gradient: 'linear-gradient(135deg, var(--accent-green), #059669)',
    welcome: 'Good day! I am your Technical Interviewer. I evaluate your depth in **Operating Systems, DBMS, Computer Networks, and OOP**. Answer as you would in a real interview, and I will score your technical correctness and suggest refinements.'
  },
  hr: {
    name: 'HR Interview Agent',
    icon: 'fa-user-tie',
    gradient: 'linear-gradient(135deg, var(--accent-rose), #e11d48)',
    welcome: 'Welcome! I am your HR and Behavioral Interview Coach. I help you craft winning responses using the **STAR Framework**, polish your **"Tell Me About Yourself" elevator pitch**, and tackle tricky behavioral scenarios.'
  }
};

async function loadAgentChat(agentType) {
  const container = document.getElementById(`chat-messages-${agentType}`);
  if (!container) return;

  try {
    const res = await fetch(`/api/agent/history/${agentType}`);
    const data = await res.json();
    container.innerHTML = '';

    const cfg = AGENT_CONFIGS[agentType] || AGENT_CONFIGS.aptitude;

    // Welcome message
    appendMessageToChat(agentType, 'agent', cfg.welcome);

    if (data.status === 'success' && data.messages.length > 0) {
      data.messages.forEach(msg => {
        appendMessageToChat(agentType, msg.sender, msg.message);
      });
    }

    scrollChatToBottom(agentType);
  } catch (err) {
    console.error(`Error loading ${agentType} chat history`, err);
  }
}

function appendMessageToChat(agentType, sender, messageText) {
  const container = document.getElementById(`chat-messages-${agentType}`);
  if (!container) return;

  const cfg = AGENT_CONFIGS[agentType] || AGENT_CONFIGS.aptitude;
  const msgEl = document.createElement('div');
  msgEl.className = `chat-msg ${sender}`;

  const avatarHtml = sender === 'user'
    ? `<div class="msg-avatar"><i class="fa-solid fa-user"></i></div>`
    : `<div class="msg-avatar" style="background: ${cfg.gradient};"><i class="fa-solid ${cfg.icon}"></i></div>`;

  const parsedContent = formatMarkdown(messageText);

  msgEl.innerHTML = `
    ${avatarHtml}
    <div class="msg-bubble">${parsedContent}</div>
  `;

  container.appendChild(msgEl);
  scrollChatToBottom(agentType);
}

async function sendChatMessage(agentType) {
  const inputEl = document.getElementById(`chat-input-${agentType}`);
  if (!inputEl) return;

  const text = inputEl.value.trim();
  if (!text) return;

  // Append user message immediately
  appendMessageToChat(agentType, 'user', text);
  inputEl.value = '';

  // Show typing indicator
  const typingId = showTypingIndicator(agentType);

  try {
    const res = await fetch('/api/agent/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent_type: agentType, message: text })
    });
    const data = await res.json();
    removeTypingIndicator(typingId);

    if (data.status === 'success') {
      appendMessageToChat(agentType, 'agent', data.reply);
      if (data.note) {
        // Optional subtle badge
      }
    } else {
      appendMessageToChat(agentType, 'agent', `⚠️ Error: ${data.message || 'Failed to generate response'}`);
    }
  } catch (err) {
    removeTypingIndicator(typingId);
    appendMessageToChat(agentType, 'agent', '⚠️ Connection error. Please verify the backend is running.');
  }
}

function sendQuickPrompt(agentType, promptText) {
  const inputEl = document.getElementById(`chat-input-${agentType}`);
  if (inputEl) {
    inputEl.value = promptText;
    sendChatMessage(agentType);
  }
}

async function clearAgentChat(agentType) {
  if (!confirm(`Are you sure you want to clear your ${agentType.toUpperCase()} conversation history?`)) return;

  try {
    await fetch(`/api/agent/clear/${agentType}`, { method: 'POST' });
    const container = document.getElementById(`chat-messages-${agentType}`);
    if (container) container.innerHTML = '';
    const cfg = AGENT_CONFIGS[agentType] || AGENT_CONFIGS.aptitude;
    appendMessageToChat(agentType, 'agent', cfg.welcome);
    showToast(`Conversation history cleared`, 'info');
  } catch (err) {
    showToast('Failed to clear chat', 'error');
  }
}

function showTypingIndicator(agentType) {
  const container = document.getElementById(`chat-messages-${agentType}`);
  if (!container) return null;

  const id = `typing-${Date.now()}`;
  const el = document.createElement('div');
  el.id = id;
  el.className = 'chat-msg agent';
  el.innerHTML = `
    <div class="msg-avatar" style="background: var(--bg-tertiary);"><i class="fa-solid fa-ellipsis fa-beat"></i></div>
    <div class="msg-bubble" style="color: var(--text-muted); font-style: italic;">
      ${agentType.toUpperCase()} Agent is analyzing your query...
    </div>
  `;
  container.appendChild(el);
  scrollChatToBottom(agentType);
  return id;
}

function removeTypingIndicator(typingId) {
  if (!typingId) return;
  const el = document.getElementById(typingId);
  if (el) el.remove();
}

function scrollChatToBottom(agentType) {
  const container = document.getElementById(`chat-messages-${agentType}`);
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

// Coding Challenge Simulator
async function runCandidateCode() {
  const code = document.getElementById('coding-editor-textarea').value;
  const lang = document.getElementById('coding-lang-select').value;
  const outBox = document.getElementById('code-execution-output');

  outBox.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Compiling and running ${lang} code against testcases...`;

  try {
    const res = await fetch('/api/coding/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        problem_id: 'TWO_POINTER_PAIR',
        problem_title: 'Target Pair Finder',
        language: lang,
        code: code
      })
    });
    const data = await res.json();
    if (data.status === 'success') {
      const sub = data.submission;
      const isAccepted = sub.status === 'Accepted';
      outBox.innerHTML = `
        <div style="color: ${isAccepted ? '#34d399' : '#f87171'}; font-weight: 700; margin-bottom: 4px;">
          <i class="fa-solid ${isAccepted ? 'fa-circle-check' : 'fa-circle-xmark'}"></i> Status: ${sub.status}
        </div>
        <div>Passed Test Cases: <strong>${sub.passed_testcases} / ${sub.total_testcases}</strong></div>
        <div style="color: var(--text-dim); font-size: 0.72rem; margin-top: 2px;">Runtime: ${sub.runtime_ms} ms | Memory: ${sub.memory_mb} MB | Stored in SQLite</div>
      `;
      showToast(`Code Run: ${sub.status} (${sub.passed_testcases}/${sub.total_testcases})`, isAccepted ? 'success' : 'error');
      loadDashboard();
    }
  } catch (err) {
    outBox.innerHTML = `<span style="color: #f87171;">Execution error. Ensure server is running.</span>`;
  }
}

function loadSampleCode() {
  const codeArea = document.getElementById('coding-editor-textarea');
  codeArea.value = `# Problem: Validate Balanced Parentheses
# Given a string containing '(', ')', '{', '}', '[', ']', determine if input is valid.

def is_valid_brackets(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            continue
    return len(stack) == 0

# Test run
print(is_valid_brackets("{[()]}")) # True
print(is_valid_brackets("{[(])}")) # False
`;
  showToast('Balanced brackets challenge loaded into editor', 'info');
}

// Lightweight safe markdown formatting
function formatMarkdown(text) {
  if (!text) return '';
  let str = text;

  // Code blocks
  str = str.replace(/```([\s\S]*?)```/g, (match, p1) => {
    return `<pre><code>${escapeHtml(p1.trim())}</code></pre>`;
  });

  // Inline code
  str = str.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Headers
  str = str.replace(/^### (.*$)/gim, '<h4 style="font-size:1rem; font-weight:700; margin:10px 0 4px; color:var(--text-main);">$1</h4>');
  str = str.replace(/^## (.*$)/gim, '<h3 style="font-size:1.1rem; font-weight:700; margin:12px 0 6px; color:var(--primary-light);">$1</h3>');

  // Bold
  str = str.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Bullet items
  str = str.replace(/^\s*-\s+(.*$)/gim, '<li style="margin-left: 18px; margin-bottom: 4px;">$1</li>');

  // Blockquotes
  str = str.replace(/^\>\s+(.*$)/gim, '<blockquote style="border-left: 3px solid var(--primary); padding-left: 12px; margin: 8px 0; color: var(--text-muted); font-style: italic;">$1</blockquote>');

  // Line breaks
  str = str.replace(/\n\n/g, '<br><br>');

  return str;
}
