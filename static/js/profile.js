// AI PLACEMENT PRO - Profile & Settings Controller

async function loadProfile() {
  try {
    const res = await fetch('/api/me');
    const data = await res.json();
    if (data.status === 'success' && data.user) {
      const u = data.user;
      document.getElementById('prof-fullname').value = u.full_name || '';
      document.getElementById('prof-college').value = u.college || '';
      document.getElementById('prof-branch').value = u.branch || '';
      document.getElementById('prof-cgpa').value = u.cgpa || 8.5;
      document.getElementById('prof-gradyear').value = u.graduation_year || 2026;
      document.getElementById('prof-targetcompany').value = u.target_company || '';
      document.getElementById('prof-targetpackage').value = u.target_package || '';
      document.getElementById('prof-bio').value = u.bio || '';
    }
  } catch (err) {
    console.error('Error loading profile', err);
  }
}

async function handleProfileUpdate(e) {
  e.preventDefault();
  const payload = {
    full_name: document.getElementById('prof-fullname').value,
    college: document.getElementById('prof-college').value,
    branch: document.getElementById('prof-branch').value,
    cgpa: parseFloat(document.getElementById('prof-cgpa').value),
    graduation_year: parseInt(document.getElementById('prof-gradyear').value),
    target_company: document.getElementById('prof-targetcompany').value,
    target_package: document.getElementById('prof-targetpackage').value,
    bio: document.getElementById('prof-bio').value
  };

  try {
    const res = await fetch('/api/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(data.message, 'success');
      checkCurrentUser();
      loadDashboard();
    } else {
      showToast(data.message || 'Failed to update profile', 'error');
    }
  } catch (err) {
    showToast('Failed to update profile', 'error');
  }
}

async function saveGeminiApiKey() {
  const key = document.getElementById('settings-gemini-key').value.trim();
  const statusEl = document.getElementById('gemini-connection-status');
  if (!key) {
    showToast('Please enter an API key', 'error');
    return;
  }

  if (statusEl) {
    statusEl.style.display = 'block';
    statusEl.style.background = 'var(--bg-tertiary, #1f293d)';
    statusEl.style.color = 'var(--text-muted, #94a3b8)';
    statusEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving and verifying Gemini API key connection...';
  }

  try {
    const res = await fetch('/api/settings/apikey', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: key, save_to_env: true })
    });
    const data = await res.json();
    if (data.status === 'success') {
      const conn = data.connection || {};
      if (conn.connected) {
        showToast('Gemini API connected successfully!', 'success');
        if (statusEl) {
          statusEl.style.background = 'rgba(16, 185, 129, 0.15)';
          statusEl.style.color = '#10b981';
          statusEl.style.border = '1px solid rgba(16, 185, 129, 0.3)';
          statusEl.innerHTML = `<i class="fa-solid fa-circle-check"></i> <strong>Live Gemini AI Connected!</strong> Model confirmed active.`;
        }
      } else {
        showToast(conn.message || 'Key saved, but verification failed.', 'warning');
        if (statusEl) {
          statusEl.style.background = 'rgba(245, 158, 11, 0.15)';
          statusEl.style.color = '#f59e0b';
          statusEl.style.border = '1px solid rgba(245, 158, 11, 0.3)';
          statusEl.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> <strong>Saved with warning:</strong> ${conn.message || 'Verification could not connect to Gemini.'}`;
        }
      }
      document.getElementById('settings-gemini-key').value = '';
    }
  } catch (err) {
    showToast('Failed to save API key', 'error');
    if (statusEl) {
      statusEl.style.display = 'block';
      statusEl.style.background = 'rgba(239, 68, 68, 0.15)';
      statusEl.style.color = '#ef4444';
      statusEl.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Connection error. Make sure the backend server is running.`;
    }
  }
}

async function testGeminiConnection() {
  const key = document.getElementById('settings-gemini-key').value.trim();
  const statusEl = document.getElementById('gemini-connection-status');
  if (statusEl) {
    statusEl.style.display = 'block';
    statusEl.style.background = 'var(--bg-tertiary, #1f293d)';
    statusEl.style.color = 'var(--text-muted, #94a3b8)';
    statusEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Testing connection to Google Gemini API...';
  }

  try {
    const res = await fetch('/api/settings/test-ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: key })
    });
    const data = await res.json();
    const conn = data.connection || {};
    if (conn.connected) {
      showToast('Gemini connection test successful!', 'success');
      if (statusEl) {
        statusEl.style.background = 'rgba(16, 185, 129, 0.15)';
        statusEl.style.color = '#10b981';
        statusEl.style.border = '1px solid rgba(16, 185, 129, 0.3)';
        statusEl.innerHTML = `<i class="fa-solid fa-circle-check"></i> <strong>Live Gemini AI Connected!</strong> (${conn.sample || 'Active'})`;
      }
    } else {
      showToast(conn.message || 'Gemini connection failed', 'error');
      if (statusEl) {
        statusEl.style.background = 'rgba(239, 68, 68, 0.15)';
        statusEl.style.color = '#ef4444';
        statusEl.style.border = '1px solid rgba(239, 68, 68, 0.3)';
        statusEl.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> <strong>Not Connected:</strong> ${conn.message}`;
      }
    }
  } catch (err) {
    showToast('Failed to reach backend test endpoint', 'error');
    if (statusEl) {
      statusEl.style.background = 'rgba(239, 68, 68, 0.15)';
      statusEl.style.color = '#ef4444';
      statusEl.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Backend server error or unreachable.`;
    }
  }
}

async function handlePasswordChange(e) {
  e.preventDefault();
  const old_password = document.getElementById('settings-old-pass').value;
  const new_password = document.getElementById('settings-new-pass').value;

  try {
    const res = await fetch('/api/settings/password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ old_password, new_password })
    });
    const data = await res.json();
    if (data.status === 'success') {
      showToast(data.message, 'success');
      document.getElementById('settings-old-pass').value = '';
      document.getElementById('settings-new-pass').value = '';
    } else {
      showToast(data.message || 'Password change failed', 'error');
    }
  } catch (err) {
    showToast('Error changing password', 'error');
  }
}
