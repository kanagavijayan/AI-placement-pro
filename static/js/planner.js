// AI PLACEMENT PRO - AI Personalized Study Planner Controller

async function generateAIStudyPlan() {
  const loading = document.getElementById('planner-loading');
  const content = document.getElementById('planner-content');
  if (!content) return;

  if (loading) loading.style.display = 'block';
  content.innerHTML = '';

  try {
    const res = await fetch('/api/planner/generate');
    const data = await res.json();
    if (loading) loading.style.display = 'none';

    if (data.status === 'success' && data.plan) {
      const p = data.plan;
      const parsedHtml = formatMarkdown(p.plan_markdown);

      content.innerHTML = `
        <div style="background: rgba(124, 58, 237, 0.08); border: 1px solid var(--border-glow); border-radius: 12px; padding: 16px 20px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">
          <div>
            <span style="font-weight: 700; color: #fff;">Placement Preparedness Index: ${p.performance.overall_readiness}%</span>
            <div style="font-size: 0.75rem; color: var(--accent-amber); margin-top: 2px;">
              <i class="fa-solid fa-triangle-exclamation"></i> Weakest Subject: <strong>${p.performance.weak_subject}</strong> (${p.performance.weak_score}%)
            </div>
          </div>
          <button class="btn btn-primary btn-sm" onclick="startWeakAreaSession('${p.performance.weak_subject}')">
            <i class="fa-solid fa-play"></i> Start ${p.performance.weak_subject} Session
          </button>
        </div>
        ${parsedHtml}
      `;
    } else {
      content.innerHTML = `<p style="color: #f87171;">Failed to generate plan. Please try again.</p>`;
    }
  } catch (err) {
    if (loading) loading.style.display = 'none';
    content.innerHTML = `<p style="color: #f87171;">Connection error while generating study plan.</p>`;
  }
}

function startWeakAreaSession(subject) {
  navigateTo('trackme');
  const sel = document.getElementById('timer-subject-select');
  if (sel) {
    for (let i = 0; i < sel.options.length; i++) {
      if (sel.options[i].value.toLowerCase().includes(subject.toLowerCase().split(' ')[0])) {
        sel.selectedIndex = i;
        break;
      }
    }
  }
  startTimer();
}
