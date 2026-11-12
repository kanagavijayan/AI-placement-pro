// AI PLACEMENT PRO - Mock Test Examination Controller

let currentExamQuestions = [];
let currentExamType = 'aptitude';
let currentExamTitle = '';
let currentQuestionIndex = 0;
let userExamAnswers = {}; // { 'apt_1': 1, ... }
let examTimerSeconds = 600; // 10 minutes default
let examTimerInterval = null;

async function startMockExam(testType, testTitle) {
  try {
    const res = await fetch(`/api/mocktests/questions?type=${testType}&count=6`);
    const data = await res.json();
    if (data.status !== 'success' || !data.questions || data.questions.length === 0) {
      showToast('No questions available for this assessment', 'error');
      return;
    }

    currentExamQuestions = data.questions;
    currentExamType = testType;
    currentExamTitle = testTitle;
    currentQuestionIndex = 0;
    userExamAnswers = {};
    examTimerSeconds = currentExamQuestions.length * 90; // 90 seconds per question

    // Hide selector grid, show active exam screen
    document.getElementById('mock-selector-grid').style.display = 'none';
    document.getElementById('active-exam-container').style.display = 'block';

    document.getElementById('exam-title-text').innerText = testTitle;

    // Start timer
    startExamTimer();
    renderExamQuestion(0);

    showToast(`Started: ${testTitle}. Good luck!`, 'info');
  } catch (err) {
    showToast('Failed to start mock examination', 'error');
  }
}

function startExamTimer() {
  clearInterval(examTimerInterval);
  updateExamTimerDisplay();
  examTimerInterval = setInterval(() => {
    examTimerSeconds--;
    updateExamTimerDisplay();
    if (examTimerSeconds <= 0) {
      clearInterval(examTimerInterval);
      showToast('Time is up! Submitting exam automatically.', 'warning');
      submitExam();
    }
  }, 1000);
}

function updateExamTimerDisplay() {
  const display = document.getElementById('exam-timer-display');
  if (!display) return;
  const mins = Math.floor(examTimerSeconds / 60);
  const secs = examTimerSeconds % 60;
  display.innerHTML = `<i class="fa-solid fa-clock"></i> ${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function renderExamQuestion(index) {
  if (index < 0 || index >= currentExamQuestions.length) return;
  currentQuestionIndex = index;

  const q = currentExamQuestions[index];
  document.getElementById('exam-question-progress').innerText = `Question ${index + 1} of ${currentExamQuestions.length} • Category: ${q.category}`;
  document.getElementById('exam-q-text').innerText = `${index + 1}. ${q.question}`;

  const optContainer = document.getElementById('exam-options-container');
  optContainer.innerHTML = '';

  const selectedChoice = userExamAnswers[q.id];

  q.options.forEach((optText, optIdx) => {
    const isSelected = selectedChoice === optIdx;
    const btn = document.createElement('div');
    btn.className = `option-card ${isSelected ? 'selected' : ''}`;
    btn.style.cssText = `
      padding: 12px 18px;
      border-radius: 10px;
      background: ${isSelected ? 'rgba(124, 58, 237, 0.25)' : 'var(--bg-primary)'};
      border: 1px solid ${isSelected ? 'var(--primary)' : 'var(--border-color)'};
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 0.88rem;
      transition: var(--transition);
    `;
    btn.innerHTML = `
      <div style="width: 26px; height: 26px; border-radius: 50%; border: 1px solid ${isSelected ? 'var(--primary)' : 'var(--text-dim)'}; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.78rem; background: ${isSelected ? 'var(--primary)' : 'transparent'}; color: #fff;">
        ${String.fromCharCode(65 + optIdx)}
      </div>
      <div>${escapeHtml(optText)}</div>
    `;
    btn.onclick = () => selectExamAnswer(q.id, optIdx);
    optContainer.appendChild(btn);
  });

  // Buttons state
  document.getElementById('btn-exam-prev').disabled = index === 0;
  const btnNext = document.getElementById('btn-exam-next');
  if (index === currentExamQuestions.length - 1) {
    btnNext.innerHTML = '<i class="fa-solid fa-flag-checkered"></i> Submit Exam';
    btnNext.onclick = finishExamEarly;
  } else {
    btnNext.innerHTML = 'Next <i class="fa-solid fa-chevron-right"></i>';
    btnNext.onclick = () => navigateExamQuestion(1);
  }
}

function selectExamAnswer(questionId, choiceIndex) {
  userExamAnswers[questionId] = choiceIndex;
  renderExamQuestion(currentQuestionIndex);
}

function navigateExamQuestion(delta) {
  renderExamQuestion(currentQuestionIndex + delta);
}

function finishExamEarly() {
  const answeredCount = Object.keys(userExamAnswers).length;
  const total = currentExamQuestions.length;
  if (answeredCount < total) {
    if (!confirm(`You have answered ${answeredCount} of ${total} questions. Are you sure you want to finish and submit now?`)) {
      return;
    }
  }
  submitExam();
}

async function submitExam() {
  clearInterval(examTimerInterval);

  try {
    const res = await fetch('/api/mocktests/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        test_type: currentExamType,
        test_title: currentExamTitle,
        answers: userExamAnswers,
        time_taken_seconds: (currentExamQuestions.length * 90) - examTimerSeconds
      })
    });
    const data = await res.json();
    if (data.status === 'success') {
      showExamResultsModal(data.result);
      loadMockHistory();
      loadDashboard();
    }
  } catch (err) {
    showToast('Failed to submit exam', 'error');
  }
}

function showExamResultsModal(result) {
  // Return UI to selector
  document.getElementById('mock-selector-grid').style.display = 'grid';
  document.getElementById('active-exam-container').style.display = 'none';

  const isPassed = result.score_pct >= 60;

  let modalHtml = `
    <div class="modal-overlay active" id="modal-exam-result">
      <div class="modal-box" style="max-width: 680px;">
        <div class="modal-header">
          <h3 class="modal-title"><i class="fa-solid fa-square-poll-vertical" style="color: var(--primary);"></i> Assessment Performance Report</h3>
          <button class="modal-close" onclick="document.getElementById('modal-exam-result').remove()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="modal-body">
          <div style="text-align: center; padding: 18px 0; border-bottom: 1px solid var(--border-color); margin-bottom: 18px;">
            <div style="font-size: 2.8rem; font-weight: 800; color: ${isPassed ? '#34d399' : '#f87171'};">
              ${result.score_pct}%
            </div>
            <p style="font-size: 0.95rem; font-weight: 600; color: var(--text-main); margin-top: 4px;">
              ${result.correct} Correct out of ${result.total} Questions
            </p>
            <span class="difficulty-pill ${isPassed ? 'Easy' : 'Hard'}" style="font-size: 0.8rem; margin-top: 6px; display: inline-block;">
              ${isPassed ? '✓ Passed Placement Benchmark' : 'Needs Practice on Weak Topics'}
            </span>
          </div>

          <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 12px;">Detailed Question Solutions:</h4>
          <div style="display: flex; flex-direction: column; gap: 14px; max-height: 340px; overflow-y: auto;">
            ${result.details.map((d, i) => `
              <div style="padding: 12px 14px; border-radius: 10px; background: var(--bg-primary); border: 1px solid ${d.is_correct ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'};">
                <div style="font-size: 0.84rem; font-weight: 600; margin-bottom: 6px;">
                  ${i + 1}. ${escapeHtml(d.question)}
                </div>
                <div style="font-size: 0.78rem; color: ${d.is_correct ? '#34d399' : '#f87171'}; margin-bottom: 4px;">
                  Your Choice: ${d.user_choice !== undefined ? d.options[d.user_choice] : 'Not answered'} (${d.is_correct ? 'Correct' : 'Incorrect'})
                </div>
                <div style="font-size: 0.76rem; color: var(--text-muted); background: var(--bg-secondary); padding: 8px 10px; border-radius: 6px;">
                  <strong>Explanation:</strong> ${escapeHtml(d.explanation)}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" onclick="document.getElementById('modal-exam-result').remove()">Close Report</button>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

async function loadMockHistory() {
  const tbody = document.getElementById('mock-history-tbody');
  if (!tbody) return;

  try {
    const res = await fetch('/api/mocktests/history');
    const data = await res.json();
    if (data.status === 'success' && data.history) {
      if (data.history.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:var(--text-dim); padding: 18px;">No test attempts yet. Select a test above to begin!</td></tr>`;
        return;
      }
      tbody.innerHTML = data.history.map(h => `
        <tr>
          <td style="font-weight: 600; color: var(--text-main);">${escapeHtml(h.test_title)}</td>
          <td><span class="topic-chip">${escapeHtml(h.category || h.test_type)}</span></td>
          <td><strong style="color: ${h.score >= 70 ? '#34d399' : '#fbbf24'};">${h.score}%</strong></td>
          <td>${h.correct_answers} / ${h.total_questions}</td>
          <td style="color: var(--text-dim); font-size: 0.75rem;">${h.created_at}</td>
        </tr>
      `).join('');
    }
  } catch (err) {
    console.error('Error loading test history', err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadMockHistory();
});
