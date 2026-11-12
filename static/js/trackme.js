// AI PLACEMENT PRO - Track Me Engine Controller

let timerInterval = null;
let timerSeconds = 0;
let isTimerRunning = false;
let activeSessionSubject = "Data Structures & Algorithms";

// 1. Timer Control: Start / Stop
function toggleTimer() {
  if (!isTimerRunning) {
    startTimer();
  } else {
    // If already running, prompt to pause or stop
    stopAndSaveTimer();
  }
}

function quickStartTracking() {
  navigateTo('trackme');
  if (!isTimerRunning) {
    startTimer();
  }
}

function startTimer() {
  const subjectSelect = document.getElementById('timer-subject-select');
  if (subjectSelect) {
    activeSessionSubject = subjectSelect.value;
  }

  isTimerRunning = true;
  timerInterval = setInterval(() => {
    timerSeconds++;
    updateTimerDisplays();
  }, 1000);

  // Update UI buttons
  const btnToggle = document.getElementById('btn-timer-toggle');
  const btnStop = document.getElementById('btn-timer-stop');
  const timerClock = document.getElementById('main-timer-clock');
  const headerPill = document.getElementById('header-timer-pill');

  if (btnToggle) {
    btnToggle.innerHTML = '<i class="fa-solid fa-pause"></i> PAUSE';
    btnToggle.className = 'btn-pill-cream';
  }
  if (btnStop) btnStop.style.display = 'inline-flex';
  if (timerClock) timerClock.classList.add('running');
  if (headerPill) headerPill.style.display = 'flex';

  const taskbarChip = document.getElementById('taskbar-timer-chip');
  if (taskbarChip) taskbarChip.style.display = 'flex';

  showToast(`Timer started for ${activeSessionSubject}!`, 'success');
}

function updateTimerDisplays() {
  const formatted = formatSeconds(timerSeconds);
  const mainClock = document.getElementById('main-timer-clock');
  const headerClock = document.getElementById('header-timer-clock');
  const headerSubj = document.getElementById('header-timer-subject');
  const taskbarClock = document.getElementById('taskbar-timer-clock');

  if (mainClock) mainClock.innerText = formatted;
  if (headerClock) headerClock.innerText = formatted;
  if (headerSubj) headerSubj.innerText = `(${activeSessionSubject})`;
  if (taskbarClock) taskbarClock.innerText = formatted;
}

async function stopAndSaveTimer() {
  if (timerSeconds < 3) {
    if (!confirm("This session is less than 3 seconds. Stop timer without saving?")) return;
    resetTimerState();
    return;
  }

  const durationSec = timerSeconds;
  const subject = activeSessionSubject;
  const notes = `Focused study session on ${subject} tracked via Track Me timer.`;

  try {
    const res = await fetch('/api/track/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subject: subject,
        duration_seconds: durationSec,
        notes: notes
      })
    });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(data.message, 'success');
      resetTimerState();
      loadTrackMeStats();
      loadDashboard();
    } else {
      showToast(data.message || 'Failed to save session', 'error');
    }
  } catch (err) {
    showToast('Failed to save study session', 'error');
  }
}

function resetTimerState() {
  clearInterval(timerInterval);
  timerInterval = null;
  timerSeconds = 0;
  isTimerRunning = false;

  const btnToggle = document.getElementById('btn-timer-toggle');
  const btnStop = document.getElementById('btn-timer-stop');
  const timerClock = document.getElementById('main-timer-clock');
  const headerPill = document.getElementById('header-timer-pill');

  if (btnToggle) {
    btnToggle.innerHTML = '<i class="fa-solid fa-play"></i> START TRACKING';
    btnToggle.className = 'btn-pill-dark';
  }
  if (btnStop) btnStop.style.display = 'none';
  if (timerClock) {
    timerClock.innerText = '00:00:00';
    timerClock.classList.remove('running');
  }
  if (headerPill) headerPill.style.display = 'none';
  const taskbarChip = document.getElementById('taskbar-timer-chip');
  if (taskbarChip) taskbarChip.style.display = 'none';
}

function formatSeconds(totalSec) {
  const hrs = Math.floor(totalSec / 3600);
  const mins = Math.floor((totalSec % 3600) / 60);
  const secs = totalSec % 60;
  return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// 2. Load Track Me Statistics & SQLite Records
async function loadTrackMeStats() {
  try {
    const [statsRes, goalsRes, progRes] = await Promise.all([
      fetch('/api/track/stats'),
      fetch('/api/track/goals'),
      fetch('/api/track/progress')
    ]);

    const statsData = await statsRes.json();
    const goalsData = await goalsRes.json();
    const progData = await progRes.json();

    if (statsData.status === 'success') {
      // Streak
      const streakEl = document.getElementById('trackme-streak-count');
      if (streakEl) streakEl.innerText = `${statsData.streak} Days`;

      // Badges
      renderBadges(statsData.badges);

      // Recent sessions table
      renderSessionsTable(statsData.recent_sessions);
    }

    if (goalsData.status === 'success') {
      renderTrackMeGoals(goalsData.goals);
    }

    if (progData.status === 'success') {
      renderProgressTable(progData.records);
    }

  } catch (err) {
    console.error('Error loading Track Me data', err);
  }
}

function renderBadges(badges) {
  const container = document.getElementById('trackme-badges-container');
  const countEl = document.getElementById('badges-unlocked-count');
  if (!container) return;

  if (countEl) countEl.innerText = `${badges ? badges.length : 0} Badges Unlocked`;

  if (!badges || badges.length === 0) {
    container.innerHTML = `<p style="font-size:0.8rem; color:var(--text-dim); text-align:center; grid-column: 1/-1;">Log your first study session to unlock badges!</p>`;
    return;
  }

  container.innerHTML = badges.map(b => `
    <div class="badge-card">
      <div class="badge-icon-circle"><i class="fa-solid ${b.badge_icon || 'fa-award'}"></i></div>
      <div class="badge-title">${escapeHtml(b.badge_name)}</div>
      <div class="badge-desc">${escapeHtml(b.badge_desc)}</div>
    </div>
  `).join('');
}

function renderSessionsTable(sessions) {
  const tbody = document.getElementById('trackme-sessions-tbody');
  if (!tbody) return;

  if (!sessions || sessions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:var(--text-dim); padding: 18px;">No study sessions logged yet. Click START TRACKING above to begin!</td></tr>`;
    return;
  }

  tbody.innerHTML = sessions.map(s => `
    <tr>
      <td style="font-weight: 600; color: var(--text-main);">${escapeHtml(s.subject)}</td>
      <td><strong>${s.duration_minutes}</strong> mins</td>
      <td style="color: var(--text-muted);">${escapeHtml(s.notes || 'Timer tracked session')}</td>
      <td style="color: var(--text-dim); font-size: 0.75rem;">${s.started_at}</td>
    </tr>
  `).join('');
}

function renderProgressTable(records) {
  const tbody = document.getElementById('trackme-progress-tbody');
  if (!tbody) return;

  if (!records || records.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--text-dim); padding: 18px;">No manual progress records logged yet. Click 'ADD PROGRESS' to record topics!</td></tr>`;
    return;
  }

  tbody.innerHTML = records.map(r => `
    <tr>
      <td style="font-weight: 600;">${escapeHtml(r.subject)}</td>
      <td>${escapeHtml(r.topic)}</td>
      <td><span class="difficulty-pill ${r.difficulty}">${r.difficulty}</span></td>
      <td><strong>${r.questions_solved}</strong> solved</td>
      <td style="color: var(--text-dim); font-size: 0.75rem;">${r.logged_date}</td>
      <td style="color: var(--text-muted); font-size: 0.78rem;">${escapeHtml(r.notes || '—')}</td>
    </tr>
  `).join('');
}

function renderTrackMeGoals(goals) {
  const container = document.getElementById('trackme-goals-list');
  if (!container) return;

  if (!goals || goals.length === 0) {
    container.innerHTML = `<p style="font-size:0.8rem; color:var(--text-dim); text-align:center; padding: 16px;">No goals defined. Click 'New Goal' to establish daily/weekly placement targets!</p>`;
    return;
  }

  container.innerHTML = goals.map(g => `
    <div class="goal-card">
      <div class="goal-left">
        <input type="checkbox" class="goal-check" ${g.is_completed ? 'checked' : ''} onchange="toggleGoalComplete(${g.id})">
        <div>
          <span class="goal-title ${g.is_completed ? 'completed' : ''}">${escapeHtml(g.title)}</span>
          <div style="font-size: 0.68rem; color: var(--text-dim); text-transform: uppercase;">${g.goal_type} • Target: ${g.target_value} ${g.unit}</div>
        </div>
      </div>
      <span class="goal-badge">${g.current_value} / ${g.target_value}</span>
    </div>
  `).join('');
}

// 3. Modals Management: Add Progress & Create Goal
function openAddProgressModal() {
  const modal = document.getElementById('modal-add-progress');
  if (modal) modal.classList.add('active');
}

function closeAddProgressModal() {
  const modal = document.getElementById('modal-add-progress');
  if (modal) modal.classList.remove('active');
}

async function submitAddProgress(e) {
  e.preventDefault();
  const subject = document.getElementById('prog-subject').value;
  const topic = document.getElementById('prog-topic').value.trim();
  const difficulty = document.getElementById('prog-difficulty').value;
  const questions_solved = document.getElementById('prog-questions').value;
  const notes = document.getElementById('prog-notes').value.trim();

  try {
    const res = await fetch('/api/track/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subject, topic, difficulty, questions_solved, notes })
    });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(data.message, 'success');
      closeAddProgressModal();
      document.getElementById('prog-topic').value = '';
      document.getElementById('prog-notes').value = '';
      loadTrackMeStats();
      loadDashboard();
    } else {
      showToast(data.message || 'Error saving progress', 'error');
    }
  } catch (err) {
    showToast('Failed to save progress record', 'error');
  }
}

function openCreateGoalModal() {
  const modal = document.getElementById('modal-create-goal');
  if (modal) modal.classList.add('active');
}

function closeCreateGoalModal() {
  const modal = document.getElementById('modal-create-goal');
  if (modal) modal.classList.remove('active');
}

async function submitCreateGoal(e) {
  e.preventDefault();
  const title = document.getElementById('goal-title-input').value.trim();
  const goal_type = document.getElementById('goal-type-select').value;
  const target_value = document.getElementById('goal-target-val').value;
  const unit = document.getElementById('goal-unit-select').value;

  try {
    const res = await fetch('/api/track/goals', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, goal_type, target_value, unit })
    });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(data.message, 'success');
      closeCreateGoalModal();
      document.getElementById('goal-title-input').value = '';
      loadTrackMeStats();
      loadDashboard();
    } else {
      showToast(data.message || 'Error creating goal', 'error');
    }
  } catch (err) {
    showToast('Failed to create goal', 'error');
  }
}
