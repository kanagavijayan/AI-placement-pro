// AI PLACEMENT PRO - Resume Builder & ATS Optimizer Controller

let activeBulletTargetField = null;

async function loadResume() {
  try {
    const res = await fetch('/api/resume');
    const data = await res.json();
    if (data.status === 'success' && data.resume) {
      const r = data.resume;
      document.getElementById('res-name').value = r.full_name || '';
      document.getElementById('res-email').value = r.email || '';
      document.getElementById('res-phone').value = r.phone || '';
      document.getElementById('res-linkedin').value = r.linkedin || '';
      document.getElementById('res-github').value = r.github || '';
      document.getElementById('res-summary').value = r.summary || '';

      if (r.projects_json && Array.isArray(r.projects_json) && r.projects_json.length > 0) {
        document.getElementById('res-projects-text').value = r.projects_json.map(p => `${p.title} (${p.tech}): ${p.description}`).join('\n\n');
      }

      if (r.skills_json) {
        if (typeof r.skills_json === 'object') {
          const allSkills = Object.values(r.skills_json).flat();
          document.getElementById('res-skills-input').value = allSkills.join(', ');
        }
      }

      if (r.ats_score) {
        document.getElementById('ats-score-display').innerText = `${r.ats_score}/100`;
      }

      updateResumePreview();
    }
  } catch (err) {
    console.error('Error loading resume', err);
  }
}

function updateResumePreview() {
  const name = document.getElementById('res-name').value || 'CANDIDATE NAME';
  const email = document.getElementById('res-email').value || 'candidate@example.com';
  const phone = document.getElementById('res-phone').value || '+91 98765 43210';
  const linkedin = document.getElementById('res-linkedin').value || 'linkedin.com/in/candidate';
  const github = document.getElementById('res-github').value || 'github.com/candidate';
  const summary = document.getElementById('res-summary').value || 'Software engineering undergraduate with strong problem solving and full-stack fundamentals.';
  const projectsText = document.getElementById('res-projects-text').value || '';
  const skillsText = document.getElementById('res-skills-input').value || 'Python, Java, C++, SQL, Algorithms, Web Development';

  document.getElementById('preview-name').innerText = name.toUpperCase();
  document.getElementById('preview-email').innerText = email;
  document.getElementById('preview-phone').innerText = phone;
  document.getElementById('preview-linkedin').innerText = linkedin;
  document.getElementById('preview-github').innerText = github;
  document.getElementById('preview-summary').innerText = summary;

  // Projects bullets
  const projectBulletsContainer = document.getElementById('preview-project-bullets');
  if (projectsText.trim()) {
    const lines = projectsText.split('\n').filter(l => l.trim().length > 0);
    projectBulletsContainer.innerHTML = lines.map(line => `<li>${escapeHtml(line)}</li>`).join('');
  } else {
    projectBulletsContainer.innerHTML = `<li>Engineered placement training agent with real-time timer analytics and simulated mock tests.</li>`;
  }

  // Skills
  document.getElementById('preview-skills-block').innerHTML = `
    <strong>Core Skills:</strong> ${escapeHtml(skillsText)}
  `;
}

async function saveResumeData() {
  const payload = {
    full_name: document.getElementById('res-name').value,
    email: document.getElementById('res-email').value,
    phone: document.getElementById('res-phone').value,
    linkedin: document.getElementById('res-linkedin').value,
    github: document.getElementById('res-github').value,
    summary: document.getElementById('res-summary').value,
    projects_json: [
      {
        title: "Key Projects",
        tech: "Full Stack & Core CS",
        description: document.getElementById('res-projects-text').value
      }
    ],
    skills_json: {
      items: document.getElementById('res-skills-input').value.split(',').map(s => s.trim())
    },
    ats_score: 88
  };

  try {
    const res = await fetch('/api/resume/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(data.message, 'success');
    }
  } catch (err) {
    showToast('Failed to save resume data', 'error');
  }
}

// AI Bullet Optimizer Modal
function openAIBulletModal(fieldId) {
  activeBulletTargetField = fieldId;
  const currentVal = document.getElementById(fieldId).value;
  document.getElementById('ai-bullet-input').value = currentVal;
  document.getElementById('ai-bullet-output-box').style.display = 'none';
  document.getElementById('btn-apply-bullet').style.display = 'none';

  const modal = document.getElementById('modal-ai-bullet');
  if (modal) modal.classList.add('active');
}

function closeAIBulletModal() {
  const modal = document.getElementById('modal-ai-bullet');
  if (modal) modal.classList.remove('active');
}

async function runAIBulletOptimizer() {
  const text = document.getElementById('ai-bullet-input').value.trim();
  const outBox = document.getElementById('ai-bullet-output-box');
  const applyBtn = document.getElementById('btn-apply-bullet');

  if (!text) {
    showToast('Please enter a statement to optimize', 'error');
    return;
  }

  outBox.style.display = 'block';
  outBox.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> AI is applying action verbs, measurable metrics, and ATS keyword enhancements...`;

  try {
    const res = await fetch('/api/resume/optimize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (data.status === 'success') {
      outBox.innerHTML = formatMarkdown(data.optimized);
      outBox.setAttribute('data-clean-text', data.optimized.replace(/^[•\s*-]+/gm, '').trim());
      applyBtn.style.display = 'inline-flex';
    } else {
      outBox.innerHTML = `<span style="color:#f87171;">${data.message || 'Error optimizing text'}</span>`;
    }
  } catch (err) {
    outBox.innerHTML = `<span style="color:#f87171;">Connection error.</span>`;
  }
}

function applyAIBullet() {
  const outBox = document.getElementById('ai-bullet-output-box');
  const clean = outBox.getAttribute('data-clean-text') || outBox.innerText;

  if (activeBulletTargetField && clean) {
    document.getElementById(activeBulletTargetField).value = clean;
    updateResumePreview();
    closeAIBulletModal();
    showToast('Applied AI enhancement to resume field!', 'success');
  }
}
