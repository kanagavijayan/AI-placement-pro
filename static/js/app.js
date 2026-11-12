// AI PLACEMENT PRO - Core Application Controller

// View titles & subtitles
const VIEW_METADATA = {
  'dashboard': { title: 'Student Dashboard', subtitle: 'Real-time placement preparedness & learning performance' },
  'agents-hub': { title: 'AI Placement Agents', subtitle: '4 Specialized Autonomous Preparation Tutors' },
  'agent-aptitude': { title: 'Aptitude Practice Agent', subtitle: 'Quantitative Math, Logical Reasoning & Verbal Ability' },
  'agent-coding': { title: 'Coding Practice Agent', subtitle: 'Data Structures, Algorithms & Debugging Coach' },
  'agent-technical': { title: 'Technical Interview Agent', subtitle: 'Simulate Software Engineering Technical Rounds' },
  'agent-hr': { title: 'HR & Behavioral Agent', subtitle: 'STAR Method, Self-Intro & Culture Fit Coaching' },
  'trackme': { title: 'Track Me – Personal Progress', subtitle: 'Live Study Timer, Goal Setter, Streaks & SQLite Persistence' },
  'study-planner': { title: 'AI Study Planner', subtitle: 'Personalized Adaptive Diagnostic & Learning Roadmaps' },
  'mock-tests': { title: 'Mock Test System', subtitle: 'Timed Assessments, Instant Evaluation & Step-by-Step Explanations' },
  'resume-builder': { title: 'AI Resume Builder', subtitle: 'ATS-Friendly Formats, AI Bullet Optimizer & PDF Export' },
  'company-prep': { title: 'Company Preparation', subtitle: 'Recruitment Patterns & Syllabi for Top Tech Employers' },
  'my-profile': { title: 'Student Profile', subtitle: 'Academic Credentials, Dream Targets & Portfolio Details' },
  'settings': { title: 'Settings', subtitle: 'Gemini AI Key, Appearance & Security Configuration' }
};

// Global Toast System
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icon = type === 'success' ? 'fa-circle-check' : (type === 'error' ? 'fa-triangle-exclamation' : 'fa-circle-info');
  toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Navigation Handler
function navigateTo(viewId) {
  // Update taskbar active class
  const navLinks = document.querySelectorAll('.left-taskbar-dock .taskbar-link, .right-taskbar-dock .taskbar-link, .nav-links-scroll .nav-pill-link');
  navLinks.forEach(link => {
    const text = link.innerText.toLowerCase();
    if (viewId === 'dashboard' && text.includes('dashboard')) link.classList.add('active');
    else if (viewId === 'agents-hub' && text.includes('ai agents')) link.classList.add('active');
    else if (viewId === 'agent-aptitude' && text.includes('aptitude')) link.classList.add('active');
    else if (viewId === 'agent-coding' && (text.includes('coding') || text.includes('code'))) link.classList.add('active');
    else if (viewId === 'agent-technical' && text.includes('technical')) link.classList.add('active');
    else if (viewId === 'agent-hr' && text.includes('hr')) link.classList.add('active');
    else if (viewId === 'trackme' && text.includes('track me')) link.classList.add('active');
    else if (viewId === 'study-planner' && text.includes('planner')) link.classList.add('active');
    else if (viewId === 'mock-tests' && text.includes('mock tests')) link.classList.add('active');
    else if (viewId === 'resume-builder' && text.includes('resume')) link.classList.add('active');
    else if (viewId === 'company-prep' && text.includes('companies')) link.classList.add('active');
    else if (viewId === 'my-profile' && text.includes('profile')) link.classList.add('active');
    else if (viewId === 'settings' && text.includes('settings')) link.classList.add('active');
    else link.classList.remove('active');
  });

  // Switch content views
  const views = document.querySelectorAll('.content-view');
  views.forEach(v => v.classList.remove('active'));

  const targetView = document.getElementById(`view-${viewId}`);
  if (targetView) {
    targetView.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Update header text
  const meta = VIEW_METADATA[viewId] || { title: 'AI PLACEMENT PRO', subtitle: 'Placement Training Platform' };
  document.getElementById('top-header-title').innerText = meta.title;
  document.getElementById('top-header-subtitle').innerText = meta.subtitle;

  // View-specific initializers
  if (viewId === 'dashboard') loadDashboard();
  if (viewId.startsWith('agent-')) loadAgentChat(viewId.replace('agent-', ''));
  if (viewId === 'trackme') loadTrackMeStats();
  if (viewId === 'study-planner') generateAIStudyPlan();
  if (viewId === 'resume-builder') loadResume();
  if (viewId === 'company-prep') loadCompanyPrep('tcs');
  if (viewId === 'my-profile') loadProfile();

  // Close mobile sidebar if open
  const sidebar = document.getElementById('app-sidebar');
  if (sidebar && sidebar.classList.contains('open')) {
    sidebar.classList.remove('open');
  }
}

// Mobile sidebar toggle
function toggleMobileSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

// Light / Dark Theme Toggle
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('placement_theme', newTheme);

  const icon = document.getElementById('theme-toggle-icon');
  const btnIcon = document.getElementById('settings-theme-btn-icon');
  if (icon) icon.className = newTheme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
  if (btnIcon) btnIcon.className = newTheme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';

  showToast(`Switched to ${newTheme} mode`, 'info');
}

// Check logged in user
async function checkCurrentUser() {
  try {
    const res = await fetch('/api/me');
    const data = await res.json();
    if (data.status === 'success') {
      const u = data.user;
      document.getElementById('sidebar-user-name').innerText = u.full_name || u.username;
      document.getElementById('sidebar-user-role').innerText = u.role.toUpperCase();
      const initials = (u.full_name || u.username).substring(0, 2).toUpperCase();
      document.getElementById('sidebar-user-avatar').innerText = initials;
      document.getElementById('dash-greeting-name').innerText = u.full_name || u.username;
      if (u.target_company) document.getElementById('dash-target-company').innerText = u.target_company;
      if (u.target_package) document.getElementById('dash-target-package').innerText = u.target_package;
    }
  } catch (err) {
    console.error('Session check failed', err);
  }
}

// Logout
async function handleLogout() {
  try {
    await fetch('/api/logout');
    window.location.href = '/auth';
  } catch (err) {
    window.location.href = '/auth';
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('placement_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  const icon = document.getElementById('theme-toggle-icon');
  if (icon) icon.className = savedTheme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';

  checkCurrentUser();
  loadDashboard();
});
