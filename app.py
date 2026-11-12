import os
import json
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from database import get_db, init_db
from ai_service import generate_agent_response, call_gemini_api, test_gemini_connection, get_gemini_api_key
from questions_data import get_test_questions, evaluate_test_submission, MOCK_TEST_BANKS
from company_data import get_company_list, get_company_details
from planner_service import analyze_student_performance, generate_personalized_study_plan

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "ai_placement_pro_super_secure_key_2026")
CORS(app)

# Ensure DB is initialized
init_db()

# --- Helper Decorators & Functions ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({"status": "error", "message": "Authentication required"}), 401
            return redirect(url_for('auth_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({"status": "error", "message": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def calculate_streak(user_id):
    """Calculate current consecutive study days."""
    conn = get_db()
    cursor = conn.cursor()
    # Get all distinct active dates from study sessions and progress records
    cursor.execute("""
        SELECT DISTINCT DATE(started_at) as log_date FROM study_sessions WHERE user_id = ?
        UNION
        SELECT DISTINCT logged_date as log_date FROM progress_records WHERE user_id = ?
        ORDER BY log_date DESC
    """, (user_id, user_id))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 0

    dates = [datetime.strptime(r["log_date"], "%Y-%m-%d").date() for r in rows if r["log_date"]]
    if not dates:
        return 0

    today = date.today()
    streak = 0
    current_check = today

    # If the user hasn't studied today yet, check if they studied yesterday
    if dates[0] == today:
        streak = 1
        current_check = today - timedelta(days=1)
        check_idx = 1
    elif dates[0] == today - timedelta(days=1):
        streak = 1
        current_check = today - timedelta(days=2)
        check_idx = 1
    else:
        return 0

    while check_idx < len(dates):
        if dates[check_idx] == current_check:
            streak += 1
            current_check -= timedelta(days=1)
            check_idx += 1
        else:
            break

    return streak

def check_and_award_badges(user_id):
    """Check conditions and award achievement badges dynamically."""
    conn = get_db()
    cursor = conn.cursor()

    # 1. First session
    cursor.execute("SELECT COUNT(*) as cnt FROM study_sessions WHERE user_id = ?", (user_id,))
    sessions_cnt = cursor.fetchone()["cnt"]
    if sessions_cnt >= 1:
        cursor.execute("INSERT OR IGNORE INTO achievements (user_id, badge_key, badge_name, badge_desc, badge_icon) VALUES (?, 'first_session', 'First Track', 'Completed your first live tracking study session', 'fa-stopwatch')", (user_id,))

    # 2. Streak badges
    streak = calculate_streak(user_id)
    if streak >= 3:
        cursor.execute("INSERT OR IGNORE INTO achievements (user_id, badge_key, badge_name, badge_desc, badge_icon) VALUES (?, 'streak_3', 'Consistency Champion', 'Maintained a 3-day active placement study streak', 'fa-fire')", (user_id,))
    if streak >= 7:
        cursor.execute("INSERT OR IGNORE INTO achievements (user_id, badge_key, badge_name, badge_desc, badge_icon) VALUES (?, 'streak_7', 'Week Titan', 'Maintained a 7-day non-stop study streak', 'fa-medal')", (user_id,))

    # 3. Coding warrior
    cursor.execute("SELECT COUNT(*) as cnt FROM coding_submissions WHERE user_id = ? AND status = 'Accepted'", (user_id,))
    solved_cnt = cursor.fetchone()["cnt"]
    if solved_cnt >= 5:
        cursor.execute("INSERT OR IGNORE INTO achievements (user_id, badge_key, badge_name, badge_desc, badge_icon) VALUES (?, 'code_warrior', 'Code Warrior', 'Solved 5+ algorithmic challenges', 'fa-code')", (user_id,))

    # 4. Mock test achiever
    cursor.execute("SELECT COUNT(*) as cnt FROM test_results WHERE user_id = ? AND score >= 80", (user_id,))
    high_score_cnt = cursor.fetchone()["cnt"]
    if high_score_cnt >= 2:
        cursor.execute("INSERT OR IGNORE INTO achievements (user_id, badge_key, badge_name, badge_desc, badge_icon) VALUES (?, 'aptitude_ace', 'Aptitude Ace', 'Scored > 80% on 2 Mock Examinations', 'fa-brain')", (user_id,))

    conn.commit()
    conn.close()

# --- Page Routes ---
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))
    return render_template('index.html')

@app.route('/auth')
def auth_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('auth.html')

# --- Authentication APIs ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip() or username
    college = data.get('college', '').strip() or "National Institute of Technology"

    if not username or not email or not password:
        return jsonify({"status": "error", "message": "Username, email, and password are required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        return jsonify({"status": "error", "message": "Username or Email already registered"}), 409

    hashed_pw = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, 'student')",
                   (username, email, hashed_pw))
    user_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO student_profiles (user_id, full_name, college, branch, cgpa, graduation_year, target_company, target_package)
        VALUES (?, ?, ?, 'Computer Science & Engineering', 8.5, 2026, 'Top Tech Enterprise', '18-24 LPA')
    """, (user_id, full_name, college))

    # Seed welcome goals
    cursor.execute("""
        INSERT INTO study_goals (user_id, title, goal_type, target_value, current_value, unit, is_completed)
        VALUES
        (?, 'Solve 3 DSA Questions', 'daily', 3, 0, 'problems', 0),
        (?, 'Complete 1 Hour Aptitude Session', 'daily', 1, 0, 'hours', 0),
        (?, 'Take 2 Full Mock Tests', 'weekly', 2, 0, 'tests', 0),
        (?, 'Log 10 Total Study Hours', 'weekly', 10, 0, 'hours', 0)
    """, (user_id, user_id, user_id, user_id))

    conn.commit()
    conn.close()

    session['user_id'] = user_id
    session['username'] = username
    session['role'] = 'student'

    return jsonify({"status": "success", "message": "Account created successfully", "user": {"id": user_id, "username": username, "role": "student"}})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username_or_email = data.get('username', '').strip()
    password = data.get('password', '')

    if not username_or_email or not password:
        return jsonify({"status": "error", "message": "Please enter credentials"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username_or_email, username_or_email))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401

    session['user_id'] = user['id']
    session['username'] = user['username']
    session['role'] = user['role']

    return jsonify({"status": "success", "message": "Login successful", "user": {"id": user['id'], "username": user['username'], "role": user['role']}})

@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully"})

@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.username, u.email, u.role, u.created_at,
               p.full_name, p.college, p.branch, p.cgpa, p.graduation_year,
               p.target_company, p.target_package, p.phone, p.linkedin, p.github, p.bio, p.avatar_seed
        FROM users u
        LEFT JOIN student_profiles p ON u.id = p.user_id
        WHERE u.id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"status": "error", "message": "User not found"}), 404

    return jsonify({"status": "success", "user": dict(row)})

# --- Dashboard APIs ---
@app.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()

    # 1. Profile
    cursor.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_id,))
    prof_row = cursor.fetchone()
    profile = dict(prof_row) if prof_row else {}

    # 2. Performance metrics
    perf = analyze_student_performance(user_id)
    streak = calculate_streak(user_id)
    check_and_award_badges(user_id)

    # 3. Weekly progress chart data (last 7 days study hours)
    weekly_hours = []
    weekly_labels = []
    today = date.today()
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_str = d.strftime("%Y-%m-%d")
        weekly_labels.append(d.strftime("%a"))
        cursor.execute("""
            SELECT SUM(duration_minutes) as mins FROM study_sessions
            WHERE user_id = ? AND DATE(started_at) = ?
        """, (user_id, day_str))
        r = cursor.fetchone()
        mins = r["mins"] if r and r["mins"] else 0
        weekly_hours.append(round(mins / 60.0, 1))

    # 4. Upcoming / Active Goals
    cursor.execute("SELECT * FROM study_goals WHERE user_id = ? ORDER BY is_completed ASC, id DESC LIMIT 5", (user_id,))
    goals = [dict(r) for r in cursor.fetchall()]

    # 5. Recent Activities
    activities = []
    # Test results
    cursor.execute("SELECT test_title, score, created_at, 'test' as act_type FROM test_results WHERE user_id = ? ORDER BY id DESC LIMIT 3", (user_id,))
    for r in cursor.fetchall():
        activities.append({
            "title": f"Completed {r['test_title']}",
            "desc": f"Score: {r['score']}%",
            "time": r['created_at'],
            "type": "test",
            "icon": "fa-clipboard-check"
        })
    # Study sessions
    cursor.execute("SELECT subject, duration_minutes, started_at, 'session' as act_type FROM study_sessions WHERE user_id = ? ORDER BY id DESC LIMIT 3", (user_id,))
    for r in cursor.fetchall():
        activities.append({
            "title": f"Tracked Study: {r['subject']}",
            "desc": f"{int(r['duration_minutes'])} mins focused study",
            "time": r['started_at'],
            "type": "session",
            "icon": "fa-clock"
        })
    # Coding submissions
    cursor.execute("SELECT problem_title, status, created_at, 'code' as act_type FROM coding_submissions WHERE user_id = ? ORDER BY id DESC LIMIT 3", (user_id,))
    for r in cursor.fetchall():
        activities.append({
            "title": f"Coding Challenge: {r['problem_title']}",
            "desc": f"Status: {r['status']}",
            "time": r['created_at'],
            "type": "code",
            "icon": "fa-code"
        })

    # Sort activities by timestamp
    activities.sort(key=lambda x: str(x['time']), reverse=True)
    recent_activities = activities[:6]

    conn.close()

    return jsonify({
        "status": "success",
        "profile": profile,
        "metrics": {
            "overall_readiness": perf["overall_readiness"],
            "total_learning_hours": perf["total_hours"],
            "coding_solved": perf["coding_solved"],
            "aptitude_score": perf["aptitude_score"],
            "technical_score": perf["technical_score"],
            "hr_score": perf["hr_score"],
            "streak_days": streak,
            "weak_subject": perf["weak_subject"]
        },
        "weekly_chart": {
            "labels": weekly_labels,
            "data": weekly_hours
        },
        "goals": goals,
        "recent_activities": recent_activities
    })

# --- AI Placement Agents APIs ---
@app.route('/api/agent/chat', methods=['POST'])
@login_required
def agent_chat():
    user_id = session['user_id']
    data = request.get_json() or {}
    agent_type = data.get('agent_type', 'aptitude').lower()
    message = data.get('message', '').strip()
    custom_key = session.get('user_gemini_key') or os.getenv("GEMINI_API_KEY", "")

    if not message:
        return jsonify({"status": "error", "message": "Message cannot be empty"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Save user message
    cursor.execute("""
        INSERT INTO ai_conversations (user_id, agent_type, sender, message)
        VALUES (?, ?, 'user', ?)
    """, (user_id, agent_type, message))

    # Retrieve last 6 messages for context
    cursor.execute("""
        SELECT sender, message FROM ai_conversations
        WHERE user_id = ? AND agent_type = ?
        ORDER BY id DESC LIMIT 6
    """, (user_id, agent_type))
    history = [dict(r) for r in reversed(cursor.fetchall())]

    # Generate response
    response_data = generate_agent_response(agent_type, message, history, custom_key)
    bot_reply = response_data.get("reply", "I am here to assist with your placement training!")

    # Save agent response
    cursor.execute("""
        INSERT INTO ai_conversations (user_id, agent_type, sender, message, metadata_json)
        VALUES (?, ?, 'agent', ?, ?)
    """, (user_id, agent_type, bot_reply, json.dumps({"mode": response_data.get("mode")})))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "reply": bot_reply,
        "mode": response_data.get("mode"),
        "note": response_data.get("note", ""),
        "agent_type": agent_type
    })

@app.route('/api/agent/history/<agent_type>', methods=['GET'])
@login_required
def agent_history(agent_type):
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, sender, message, created_at, metadata_json
        FROM ai_conversations
        WHERE user_id = ? AND agent_type = ?
        ORDER BY id ASC LIMIT 50
    """, (user_id, agent_type))
    messages = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"status": "success", "messages": messages})

@app.route('/api/agent/clear/<agent_type>', methods=['POST'])
@login_required
def agent_clear_history(agent_type):
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ai_conversations WHERE user_id = ? AND agent_type = ?", (user_id, agent_type))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"{agent_type.capitalize()} Agent conversation history cleared"})

# Coding Challenge runner / evaluator
@app.route('/api/coding/run', methods=['POST'])
@login_required
def run_code():
    user_id = session['user_id']
    data = request.get_json() or {}
    problem_id = data.get('problem_id', 'CUSTOM_1')
    problem_title = data.get('problem_title', 'Algorithmic Challenge')
    language = data.get('language', 'Python')
    code = data.get('code', '')

    if not code.strip():
        return jsonify({"status": "error", "message": "Please write your code before running."}), 400

    # Basic static check & simulation
    status = "Accepted"
    passed = 10
    total = 10
    runtime = 42

    # Check for syntax or common errors in basic code
    if "error" in code.lower() or "syntax" in code.lower() or len(code.strip()) < 15:
        status = "Wrong Answer"
        passed = 3
        runtime = 85

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO coding_submissions (user_id, problem_id, problem_title, language, code, status, passed_testcases, total_testcases, runtime_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, problem_id, problem_title, language, code, status, passed, total, runtime))
    conn.commit()
    conn.close()

    check_and_award_badges(user_id)

    return jsonify({
        "status": "success",
        "submission": {
            "status": status,
            "passed_testcases": passed,
            "total_testcases": total,
            "runtime_ms": runtime,
            "memory_mb": 14.2
        }
    })

# --- Track Me System APIs ---
@app.route('/api/track/save', methods=['POST'])
@login_required
def save_study_session():
    user_id = session['user_id']
    data = request.get_json() or {}
    subject = data.get('subject', 'General Placement Prep')
    duration_seconds = int(data.get('duration_seconds', 0))
    notes = data.get('notes', 'Focus study session via Track Me timer')

    if duration_seconds < 1:
        return jsonify({"status": "error", "message": "Session duration must be at least 1 second"}), 400

    duration_minutes = round(duration_seconds / 60.0, 2)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO study_sessions (user_id, subject, duration_seconds, duration_minutes, notes, started_at, ended_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, subject, duration_seconds, duration_minutes, notes,
          (datetime.now() - timedelta(seconds=duration_seconds)).strftime('%Y-%m-%d %H:%M:%S'),
          datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    # Update goal progress if applicable
    cursor.execute("""
        UPDATE study_goals
        SET current_value = current_value + ?
        WHERE user_id = ? AND unit = 'hours' AND is_completed = 0
    """, (round(duration_minutes / 60.0, 1), user_id))

    conn.commit()
    conn.close()

    check_and_award_badges(user_id)
    streak = calculate_streak(user_id)

    return jsonify({
        "status": "success",
        "message": f"Successfully logged {duration_minutes} minutes for {subject}!",
        "streak": streak
    })

@app.route('/api/track/progress', methods=['GET', 'POST'])
@login_required
def track_progress():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        subject = data.get('subject', 'General')
        topic = data.get('topic', '').strip()
        difficulty = data.get('difficulty', 'Medium')
        questions_solved = int(data.get('questions_solved', 0))
        notes = data.get('notes', '')
        logged_date = data.get('logged_date') or date.today().strftime('%Y-%m-%d')

        if not topic:
            conn.close()
            return jsonify({"status": "error", "message": "Topic name is required"}), 400

        cursor.execute("""
            INSERT INTO progress_records (user_id, subject, topic, difficulty, questions_solved, notes, logged_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, subject, topic, difficulty, questions_solved, notes, logged_date))

        # Check goals
        cursor.execute("""
            UPDATE study_goals
            SET current_value = current_value + ?
            WHERE user_id = ? AND unit = 'problems' AND is_completed = 0
        """, (questions_solved, user_id))

        conn.commit()
        conn.close()
        check_and_award_badges(user_id)
        return jsonify({"status": "success", "message": f"Progress for '{topic}' logged successfully!"})

    # GET: return list
    cursor.execute("SELECT * FROM progress_records WHERE user_id = ? ORDER BY logged_date DESC, id DESC LIMIT 50", (user_id,))
    records = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"status": "success", "records": records})

@app.route('/api/track/stats', methods=['GET'])
@login_required
def track_stats():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()

    streak = calculate_streak(user_id)

    # Subject breakdown of study time
    cursor.execute("""
        SELECT subject, SUM(duration_minutes) as total_mins, COUNT(*) as sessions_count
        FROM study_sessions
        WHERE user_id = ?
        GROUP BY subject
        ORDER BY total_mins DESC
    """, (user_id,))
    subject_time = [dict(r) for r in cursor.fetchall()]

    # Total study time
    cursor.execute("SELECT SUM(duration_minutes) as mins FROM study_sessions WHERE user_id = ?", (user_id,))
    r_mins = cursor.fetchone()
    total_study_mins = r_mins["mins"] if r_mins and r_mins["mins"] else 0

    # Total questions solved
    cursor.execute("SELECT SUM(questions_solved) as qs FROM progress_records WHERE user_id = ?", (user_id,))
    r_qs = cursor.fetchone()
    total_questions = r_qs["qs"] if r_qs and r_qs["qs"] else 0

    # Badges
    cursor.execute("SELECT * FROM achievements WHERE user_id = ? ORDER BY unlocked_at DESC", (user_id,))
    badges = [dict(r) for r in cursor.fetchall()]

    # Sessions history (last 20)
    cursor.execute("SELECT * FROM study_sessions WHERE user_id = ? ORDER BY started_at DESC LIMIT 20", (user_id,))
    sessions = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return jsonify({
        "status": "success",
        "streak": streak,
        "total_study_hours": round(total_study_mins / 60.0, 1),
        "total_study_minutes": int(total_study_mins),
        "total_questions_solved": total_questions,
        "subject_breakdown": subject_time,
        "badges": badges,
        "recent_sessions": sessions
    })

@app.route('/api/track/goals', methods=['GET', 'POST'])
@login_required
def track_goals():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        goal_type = data.get('goal_type', 'daily')
        target_value = int(data.get('target_value', 1))
        unit = data.get('unit', 'hours')

        if not title:
            conn.close()
            return jsonify({"status": "error", "message": "Goal title is required"}), 400

        cursor.execute("""
            INSERT INTO study_goals (user_id, title, goal_type, target_value, current_value, unit, is_completed)
            VALUES (?, ?, ?, ?, 0, ?, 0)
        """, (user_id, title, goal_type, target_value, unit))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Goal created!"})

    cursor.execute("SELECT * FROM study_goals WHERE user_id = ? ORDER BY is_completed ASC, id DESC", (user_id,))
    goals = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"status": "success", "goals": goals})

@app.route('/api/track/goals/<int:goal_id>/toggle', methods=['POST'])
@login_required
def toggle_goal(goal_id):
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT is_completed FROM study_goals WHERE id = ? AND user_id = ?", (goal_id, user_id))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"status": "error", "message": "Goal not found"}), 404

    new_state = 0 if row["is_completed"] else 1
    cursor.execute("UPDATE study_goals SET is_completed = ? WHERE id = ? AND user_id = ?", (new_state, goal_id, user_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "is_completed": new_state})

# --- AI Personalized Study Planner API ---
@app.route('/api/planner/generate', methods=['GET'])
@login_required
def get_study_plan():
    user_id = session['user_id']
    custom_key = session.get('user_gemini_key') or os.getenv("GEMINI_API_KEY", "")
    plan = generate_personalized_study_plan(user_id, custom_key)
    return jsonify({"status": "success", "plan": plan})

# --- Mock Test APIs ---
@app.route('/api/mocktests/questions', methods=['GET'])
@login_required
def get_mock_questions():
    test_type = request.args.get('type', 'aptitude')
    count = int(request.args.get('count', 6))
    questions = get_test_questions(test_type, count)
    # Strip correct_index and explanation for candidate test view
    safe_questions = []
    for q in questions:
        safe_questions.append({
            "id": q["id"],
            "category": q["category"],
            "topic": q["topic"],
            "question": q["question"],
            "options": q["options"]
        })
    return jsonify({"status": "success", "test_type": test_type, "questions": safe_questions})

@app.route('/api/mocktests/submit', methods=['POST'])
@login_required
def submit_mock_test():
    user_id = session['user_id']
    data = request.get_json() or {}
    test_type = data.get('test_type', 'aptitude')
    test_title = data.get('test_title', 'Placement Mock Assessment')
    answers = data.get('answers', {})
    time_taken = int(data.get('time_taken_seconds', 300))

    eval_result = evaluate_test_submission(test_type, answers)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO test_results (user_id, test_type, test_title, score, total_questions, correct_answers, time_taken_seconds, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, test_type, test_title, eval_result["score_pct"], eval_result["total"], eval_result["correct"], time_taken, json.dumps(eval_result["details"])))
    conn.commit()
    conn.close()

    check_and_award_badges(user_id)

    return jsonify({"status": "success", "result": eval_result})

@app.route('/api/mocktests/history', methods=['GET'])
@login_required
def mock_history():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_results WHERE user_id = ? ORDER BY id DESC LIMIT 20", (user_id,))
    history = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"status": "success", "history": history})

# --- Resume Builder APIs ---
@app.route('/api/resume', methods=['GET'])
@login_required
def get_resume():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        resume = dict(row)
        for key in ['education_json', 'experience_json', 'projects_json', 'skills_json', 'certifications_json']:
            if resume.get(key) and isinstance(resume[key], str):
                try:
                    resume[key] = json.loads(resume[key])
                except Exception:
                    pass
        return jsonify({"status": "success", "resume": resume})

    # Return default draft based on profile
    return jsonify({
        "status": "success",
        "resume": {
            "full_name": session.get('username', 'Placement Candidate'),
            "email": "candidate@example.com",
            "phone": "+91 98765 43210",
            "linkedin": "https://linkedin.com/in/candidate",
            "github": "https://github.com/candidate",
            "portfolio": "https://candidate.dev",
            "summary": "Proactive software engineering student with strong command over Data Structures, Algorithmic thinking, and Modern Web Development. Eager to solve challenging problems in enterprise environments.",
            "education_json": [{"degree": "B.Tech in Computer Science", "institution": "Institute of Engineering", "year": "2022 - 2026", "grade": "8.5 CGPA"}],
            "experience_json": [{"title": "Software Intern", "company": "Tech Innovations", "period": "Summer 2025", "description": "Developed backend APIs and optimized database queries, reducing response latency by 25%."}],
            "projects_json": [{"title": "AI Placement Pro Platform", "tech": "Flask, SQLite, Chart.js, AI", "description": "Constructed multi-agent placement training platform with performance tracking and mock examinations."}],
            "skills_json": {"languages": ["Python", "Java", "C++", "SQL"], "frameworks": ["Flask", "React", "Docker", "Git"], "core": ["Data Structures", "DBMS", "Operating Systems", "Computer Networks"]},
            "certifications_json": [{"name": "Cloud Certified Practitioner", "issuer": "Global Cloud Provider", "year": "2025"}],
            "ats_score": 85
        }
    })

@app.route('/api/resume/save', methods=['POST'])
@login_required
def save_resume():
    user_id = session['user_id']
    data = request.get_json() or {}

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resumes (user_id, full_name, email, phone, linkedin, github, portfolio, summary, education_json, experience_json, projects_json, skills_json, certifications_json, ats_score, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            full_name = excluded.full_name,
            email = excluded.email,
            phone = excluded.phone,
            linkedin = excluded.linkedin,
            github = excluded.github,
            portfolio = excluded.portfolio,
            summary = excluded.summary,
            education_json = excluded.education_json,
            experience_json = excluded.experience_json,
            projects_json = excluded.projects_json,
            skills_json = excluded.skills_json,
            certifications_json = excluded.certifications_json,
            ats_score = excluded.ats_score,
            updated_at = CURRENT_TIMESTAMP
    """, (
        user_id,
        data.get('full_name'),
        data.get('email'),
        data.get('phone'),
        data.get('linkedin'),
        data.get('github'),
        data.get('portfolio'),
        data.get('summary'),
        json.dumps(data.get('education_json', [])),
        json.dumps(data.get('experience_json', [])),
        json.dumps(data.get('projects_json', [])),
        json.dumps(data.get('skills_json', {})),
        json.dumps(data.get('certifications_json', [])),
        data.get('ats_score', 85)
    ))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Resume saved successfully!"})

@app.route('/api/resume/optimize', methods=['POST'])
@login_required
def optimize_resume_bullet():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    custom_key = session.get('user_gemini_key') or os.getenv("GEMINI_API_KEY", "")

    if not text:
        return jsonify({"status": "error", "message": "Text is required"}), 400

    if custom_key:
        prompt = f"Rewrite this resume bullet point into an ATS-friendly, high-impact statement using active power verbs and quantifiable impact (Action + Context + Result):\n\n'{text}'\n\nProvide 2 polished bullet point alternatives."
        reply = call_gemini_api(custom_key, "You are a Fortune 500 ATS Resume Specialist.", [], prompt)
        if reply:
            return jsonify({"status": "success", "optimized": reply})

    # Heuristic enhancement
    optimized = (
        f"• Engineered scalable solutions for '{text}', improving system execution speed by 35% and enhancing reliability across high-traffic operations.\n"
        f"• Architected and implemented key features for '{text}', collaborating in an Agile lifecycle with unit test coverage exceeding 90%."
    )
    return jsonify({"status": "success", "optimized": optimized})

# --- Company Preparation APIs ---
@app.route('/api/companies', methods=['GET'])
@login_required
def get_companies():
    return jsonify({"status": "success", "companies": get_company_list()})

@app.route('/api/companies/<company_id>', methods=['GET'])
@login_required
def get_company(company_id):
    details = get_company_details(company_id)
    if not details:
        return jsonify({"status": "error", "message": "Company blueprint not found"}), 404
    return jsonify({"status": "success", "company": details})

# --- Profile & Settings APIs ---
@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    user_id = session['user_id']
    data = request.get_json() or {}

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE student_profiles
        SET full_name = ?, college = ?, branch = ?, cgpa = ?, graduation_year = ?,
            target_company = ?, target_package = ?, phone = ?, linkedin = ?, github = ?, bio = ?
        WHERE user_id = ?
    """, (
        data.get('full_name', 'Student'),
        data.get('college', 'Engineering College'),
        data.get('branch', 'CSE'),
        float(data.get('cgpa', 8.5)),
        int(data.get('graduation_year', 2026)),
        data.get('target_company', 'Top Tech Enterprise'),
        data.get('target_package', '18-24 LPA'),
        data.get('phone', ''),
        data.get('linkedin', ''),
        data.get('github', ''),
        data.get('bio', ''),
        user_id
    ))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Profile updated successfully!"})

@app.route('/api/settings/apikey', methods=['POST'])
@login_required
def set_api_key():
    data = request.get_json() or {}
    api_key = data.get('api_key', '').strip()
    session['user_gemini_key'] = api_key
    
    # Save to .env if requested or by default if valid
    save_env = data.get('save_to_env', True)
    if save_env and api_key:
        try:
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            lines = []
            key_set = False
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            new_lines = []
            for line in lines:
                if line.startswith('GEMINI_API_KEY='):
                    new_lines.append(f"GEMINI_API_KEY={api_key}\n")
                    key_set = True
                else:
                    new_lines.append(line)
            if not key_set:
                new_lines.append(f"GEMINI_API_KEY={api_key}\n")
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            os.environ['GEMINI_API_KEY'] = api_key
        except Exception as e:
            print(f"Error persisting API key to .env: {e}")

    # Test the connection immediately if key provided
    test_res = test_gemini_connection(api_key) if api_key else {"connected": False, "message": "Key cleared"}
    return jsonify({
        "status": "success",
        "message": "Gemini API Key configured!",
        "connection": test_res
    })

@app.route('/api/settings/test-ai', methods=['POST', 'GET'])
@login_required
def test_ai_status():
    custom_key = session.get('user_gemini_key') or os.getenv("GEMINI_API_KEY", "")
    data = request.get_json(silent=True) or {}
    key_to_test = data.get('api_key') or custom_key
    result = test_gemini_connection(key_to_test)
    return jsonify({
        "status": "success",
        "has_key": bool(get_gemini_api_key(key_to_test)),
        "connection": result
    })

@app.route('/api/settings/password', methods=['POST'])
@login_required
def change_password():
    user_id = session['user_id']
    data = request.get_json() or {}
    old_pw = data.get('old_password', '')
    new_pw = data.get('new_password', '')

    if not old_pw or not new_pw:
        return jsonify({"status": "error", "message": "All fields required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row or not check_password_hash(row["password_hash"], old_pw):
        conn.close()
        return jsonify({"status": "error", "message": "Current password incorrect"}), 400

    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (generate_password_hash(new_pw), user_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Password changed successfully!"})

# --- Admin API ---
@app.route('/api/admin/overview', methods=['GET'])
@admin_required
def admin_overview():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total_users FROM users WHERE role = 'student'")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT SUM(duration_minutes) as total_mins FROM study_sessions")
    r_mins = cursor.fetchone()
    total_study_hours = round((r_mins["mins"] or 0) / 60.0, 1)

    cursor.execute("SELECT COUNT(*) as total_tests FROM test_results")
    total_tests = cursor.fetchone()["total_tests"]

    cursor.execute("""
        SELECT u.username, p.full_name, p.target_company, p.college,
               (SELECT COUNT(*) FROM coding_submissions WHERE user_id = u.id AND status = 'Accepted') as solved_count,
               (SELECT ROUND(AVG(score), 1) FROM test_results WHERE user_id = u.id) as avg_score
        FROM users u
        JOIN student_profiles p ON u.id = p.user_id
        WHERE u.role = 'student'
        LIMIT 10
    """)
    students = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return jsonify({
        "status": "success",
        "stats": {
            "total_students": total_users,
            "total_study_hours": total_study_hours,
            "total_tests_conducted": total_tests
        },
        "students": students
    })

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"=================================================")
    print(f"  AI PLACEMENT PRO - Server Starting on port {port}")
    print(f"  Tagline: Your Personal AI Placement Partner")
    print(f"  URL: http://127.0.0.1:{port}")
    print(f"=================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
