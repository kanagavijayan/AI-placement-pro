// AI PLACEMENT PRO - Company Preparation Controller

const COMPANY_IDS = ['tcs', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini', 'zoho', 'amazon', 'microsoft'];

async function loadCompanyPrep(selectedCompanyId = 'tcs') {
  renderCompanyTabs(selectedCompanyId);

  const card = document.getElementById('company-detail-card');
  if (!card) return;

  try {
    const res = await fetch(`/api/companies/${selectedCompanyId}`);
    const data = await res.json();
    if (data.status !== 'success' || !data.company) return;

    const comp = data.company;

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap; gap: 14px;">
        <div>
          <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
            <div class="msg-avatar" style="background: rgba(124, 58, 237, 0.2); color: var(--primary-light); font-size: 1.2rem;">
              <i class="fa-solid ${comp.logo_icon || 'fa-building'}"></i>
            </div>
            <div>
              <h3 style="font-size: 1.3rem; font-weight: 800;">${escapeHtml(comp.name)}</h3>
              <span style="font-size: 0.78rem; color: var(--text-dim);">${escapeHtml(comp.category)}</span>
            </div>
          </div>
          <div style="font-size: 0.84rem; color: var(--accent-cyan); font-weight: 600; margin-top: 6px;">
            <i class="fa-solid fa-briefcase"></i> Hiring Profiles & CTC: ${escapeHtml(comp.roles)}
          </div>
        </div>

        <div style="display: flex; gap: 10px;">
          <button class="btn btn-secondary btn-sm" onclick="startCompanyMockExam('${comp.name}', '${comp.id}')">
            <i class="fa-solid fa-pen-to-square"></i> Take Company Mock
          </button>
          <button class="btn btn-primary btn-sm" onclick="askAgentAboutCompany('${comp.name}')">
            <i class="fa-solid fa-comments"></i> Ask AI Interviewer
          </button>
        </div>
      </div>

      <!-- Recruitment Rounds Flow -->
      <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 12px;"><i class="fa-solid fa-layer-group" style="color: var(--primary);"></i> Recruitment Process Breakdown</h4>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px;">
        ${comp.rounds.map(r => `
          <div style="background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span class="nav-badge" style="background: rgba(124, 58, 237, 0.2); color: var(--primary-light);">Round ${r.round_num}</span>
              <span style="font-size: 0.72rem; color: var(--text-dim);"><i class="fa-solid fa-clock"></i> ${escapeHtml(r.duration)}</span>
            </div>
            <h5 style="font-size: 0.9rem; font-weight: 700; margin-bottom: 8px;">${escapeHtml(r.title)}</h5>
            <ul style="padding-left: 16px; font-size: 0.78rem; color: var(--text-muted); line-height: 1.5;">
              ${r.components.map(c => `<li>${escapeHtml(c)}</li>`).join('')}
            </ul>
          </div>
        `).join('')}
      </div>

      <!-- Key Tips & Strategy -->
      <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 12px;"><i class="fa-solid fa-lightbulb" style="color: var(--accent-amber);"></i> Key Preparation Insights & Strategies</h4>
      <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <ul style="padding-left: 18px; font-size: 0.82rem; color: var(--text-main); line-height: 1.6;">
          ${comp.key_tips.map(tip => `<li>${escapeHtml(tip)}</li>`).join('')}
        </ul>
      </div>

      <!-- High Yield Drill Topics -->
      <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 12px;"><i class="fa-solid fa-bullseye" style="color: var(--accent-rose);"></i> Priority Drill Topics</h4>
      <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        ${comp.drill_topics.map(t => `<span class="topic-chip" style="padding: 6px 12px; font-size: 0.8rem; background: var(--bg-tertiary);">${escapeHtml(t)}</span>`).join('')}
      </div>
    `;

  } catch (err) {
    console.error('Error loading company data', err);
  }
}

function renderCompanyTabs(activeId) {
  const container = document.getElementById('company-tabs-bar');
  if (!container) return;

  const labels = {
    tcs: 'TCS',
    infosys: 'Infosys',
    wipro: 'Wipro',
    accenture: 'Accenture',
    cognizant: 'Cognizant',
    capgemini: 'Capgemini',
    zoho: 'Zoho',
    amazon: 'Amazon',
    microsoft: 'Microsoft'
  };

  container.innerHTML = COMPANY_IDS.map(id => `
    <button class="prompt-btn ${id === activeId ? 'active' : ''}" style="${id === activeId ? 'background: var(--primary); color: #fff; border-color: var(--primary);' : ''}" onclick="loadCompanyPrep('${id}')">
      ${labels[id] || id.toUpperCase()}
    </button>
  `).join('');
}

function askAgentAboutCompany(companyName) {
  navigateTo('agent-technical');
  const input = document.getElementById('chat-input-technical');
  if (input) {
    input.value = `Can you conduct a mock technical interview round tailored for ${companyName}? What are the primary core topics and coding patterns they focus on?`;
    sendChatMessage('technical');
  }
}

function startCompanyMockExam(companyName, companyId = 'aptitude') {
  navigateTo('mock-tests');
  startMockExam(companyId, `${companyName} Placement Assessment`);
}
