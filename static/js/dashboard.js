// AI PLACEMENT PRO - Bento Dashboard Controller & Chart.js Styling

let weeklyChartInstance = null;

async function loadDashboard() {
  try {
    const res = await fetch('/api/dashboard');
    const data = await res.json();
    if (data.status !== 'success') return;

    const m = data.metrics;

    // 1. Bento Stat Cards
    const elHoursTicket = document.getElementById('dash-total-hours-ticket');
    if (elHoursTicket) elHoursTicket.innerText = `${m.total_learning_hours}h`;

    const elStreakSub = document.getElementById('dash-streak-sub');
    if (elStreakSub) elStreakSub.innerText = `${m.streak_days} Days Streak 🔥`;

    const elSolvedBig = document.getElementById('dash-solved-big');
    if (elSolvedBig) elSolvedBig.innerText = `${m.coding_solved || 12}k+`;

    const elHoursBig = document.getElementById('dash-hours-big');
    if (elHoursBig) elHoursBig.innerText = `${Math.round(m.total_learning_hours * 2.8 + 24)}k`;

    // Legacy fallbacks if present
    if (document.getElementById('dash-readiness-val')) document.getElementById('dash-readiness-val').innerText = `${m.overall_readiness}%`;
    if (document.getElementById('dash-hours-val')) document.getElementById('dash-hours-val').innerText = `${m.total_learning_hours}h`;
    if (document.getElementById('dash-coding-val')) document.getElementById('dash-coding-val').innerText = m.coding_solved;
    if (document.getElementById('dash-streak-val')) document.getElementById('dash-streak-val').innerText = `${m.streak_days} Days`;
    if (document.getElementById('dash-aptitude-val')) document.getElementById('dash-aptitude-val').innerText = `${m.aptitude_score}%`;
    if (document.getElementById('dash-technical-val')) document.getElementById('dash-technical-val').innerText = `${m.technical_score}%`;
    if (document.getElementById('dash-hr-val')) document.getElementById('dash-hr-val').innerText = `${m.hr_score}%`;
    if (document.getElementById('dash-weak-val')) document.getElementById('dash-weak-val').innerText = m.weak_subject || 'All Balanced';

    // 2. Weekly Study Chart (Chart.js styled with warm neo-minimalist palette)
    if (data.weekly_chart) {
      renderWeeklyChart(data.weekly_chart.labels, data.weekly_chart.data);
    }

    // 3. Goals List
    renderDashboardGoals(data.goals);

    // 4. Recent Activity List
    renderDashboardActivities(data.recent_activities);

  } catch (err) {
    console.error('Error loading dashboard data', err);
  }
}

function renderWeeklyChart(labels, dataPoints) {
  const ctx = document.getElementById('weeklyProgressChart');
  if (!ctx) return;

  if (weeklyChartInstance) {
    weeklyChartInstance.destroy();
  }

  const gridColor = 'rgba(20, 20, 20, 0.08)';
  const textColor = '#52504C';

  weeklyChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Study Hours Logged',
        data: dataPoints,
        backgroundColor: '#141414',
        hoverBackgroundColor: '#FF6838',
        borderColor: '#141414',
        borderWidth: 1.5,
        borderRadius: 12,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: '#141414',
          titleColor: '#FFFFFF',
          bodyColor: '#EBF08D',
          borderColor: '#141414',
          borderWidth: 1.5,
          padding: 10,
          displayColors: false,
          callbacks: {
            label: (ctx) => `${ctx.raw} Hours Studied`
          }
        }
      },
      scales: {
        x: {
          grid: { color: gridColor },
          ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', weight: '700' } }
        },
        y: {
          beginAtZero: true,
          grid: { color: gridColor },
          ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', weight: '600' }, callback: (v) => `${v}h` }
        }
      }
    }
  });
}

function renderDashboardGoals(goals) {
  const container = document.getElementById('dashboard-goals-list');
  if (!container) return;

  if (!goals || goals.length === 0) {
    container.innerHTML = `<p style="font-size:0.82rem; color: var(--ink-dim); text-align:center; padding: 14px;">No active goals yet. Click '+ Progress' to set one!</p>`;
    return;
  }

  container.innerHTML = goals.map(g => `
    <div class="activity-ledger-item">
      <div class="activity-ledger-left">
        <input type="checkbox" style="width: 18px; height: 18px; accent-color: #141414; cursor: pointer;" ${g.is_completed ? 'checked' : ''} onchange="toggleGoalComplete(${g.id})">
        <div class="activity-ledger-text">
          <h5 style="${g.is_completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}">${escapeHtml(g.title)}</h5>
          <p>${g.goal_type.toUpperCase()} • Target: ${g.target_value} ${g.unit}</p>
        </div>
      </div>
      <span class="activity-ledger-badge">${g.current_value} / ${g.target_value}</span>
    </div>
  `).join('');
}

function renderDashboardActivities(activities) {
  const container = document.getElementById('dashboard-activity-list');
  if (!container) return;

  if (!activities || activities.length === 0) {
    container.innerHTML = `<p style="font-size:0.82rem; color: var(--ink-dim); text-align:center; padding: 14px;">No recent activities logged yet.</p>`;
    return;
  }

  container.innerHTML = activities.slice(0, 4).map(a => `
    <div class="activity-ledger-item">
      <div class="activity-ledger-left">
        <div class="activity-ledger-glyph"><i class="fa-solid ${a.icon || 'fa-check'}"></i></div>
        <div class="activity-ledger-text">
          <h5>${escapeHtml(a.title)}</h5>
          <p>${escapeHtml(a.desc)} • ${formatTimeAgo(a.time)}</p>
        </div>
      </div>
      <span class="activity-ledger-badge" style="background: var(--bg-card-cream);">${a.type.toUpperCase()}</span>
    </div>
  `).join('');
}

async function toggleGoalComplete(goalId) {
  try {
    const res = await fetch(`/api/track/goals/${goalId}/toggle`, { method: 'POST' });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(data.is_completed ? 'Goal completed! Great job!' : 'Goal reopened', 'success');
      loadDashboard();
      if (document.getElementById('view-trackme') && document.getElementById('view-trackme').classList.contains('active')) {
        loadTrackMeStats();
      }
    }
  } catch (err) {
    showToast('Failed to update goal', 'error');
  }
}

function formatTimeAgo(dateString) {
  if (!dateString) return 'Just now';
  const d = new Date(dateString);
  const diffSec = Math.floor((new Date() - d) / 1000);
  if (diffSec < 60) return 'Just now';
  if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`;
  if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`;
  return `${Math.floor(diffSec / 86400)}d ago`;
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
