import sqlite3
import os
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'placement_pro.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Student Profiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        college TEXT DEFAULT 'Institute of Engineering & Technology',
        branch TEXT DEFAULT 'Computer Science & Engineering',
        cgpa REAL DEFAULT 8.6,
        graduation_year INTEGER DEFAULT 2026,
        target_company TEXT DEFAULT 'Top Tech Enterprise',
        target_package TEXT DEFAULT '18-24 LPA',
        phone TEXT DEFAULT '+91 9876543210',
        linkedin TEXT DEFAULT 'https://linkedin.com/in/student',
        github TEXT DEFAULT 'https://github.com/student',
        bio TEXT DEFAULT 'Passionate software engineer striving for top-tier tech placements.',
        avatar_seed TEXT DEFAULT 'Felix',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 3. Study Sessions (Track Me Timer logs)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        duration_seconds INTEGER NOT NULL,
        duration_minutes REAL NOT NULL,
        notes TEXT,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 4. Study Goals
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        goal_type TEXT NOT NULL, -- 'daily', 'weekly'
        target_value INTEGER NOT NULL,
        current_value INTEGER DEFAULT 0,
        unit TEXT NOT NULL, -- 'hours', 'problems', 'tests', 'topics'
        is_completed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 5. Progress Records (Add Progress manual logs)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Medium', -- 'Easy', 'Medium', 'Hard'
        questions_solved INTEGER DEFAULT 0,
        notes TEXT,
        logged_date DATE DEFAULT CURRENT_DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 6. Test Results (Mock Tests & Company Prep)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        test_type TEXT NOT NULL, -- 'aptitude', 'technical', 'coding', 'company'
        test_title TEXT NOT NULL,
        category TEXT DEFAULT 'General',
        score REAL NOT NULL,
        total_questions INTEGER NOT NULL,
        correct_answers INTEGER NOT NULL,
        time_taken_seconds INTEGER NOT NULL,
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 7. Coding Submissions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS coding_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        problem_id TEXT NOT NULL,
        problem_title TEXT NOT NULL,
        language TEXT NOT NULL,
        code TEXT NOT NULL,
        status TEXT NOT NULL, -- 'Accepted', 'Wrong Answer', 'Time Limit Exceeded', 'Runtime Error'
        passed_testcases INTEGER DEFAULT 0,
        total_testcases INTEGER DEFAULT 0,
        runtime_ms INTEGER DEFAULT 45,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 8. AI Conversations (Aptitude, Coding, Technical, HR chats)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        agent_type TEXT NOT NULL, -- 'aptitude', 'coding', 'technical', 'hr'
        sender TEXT NOT NULL, -- 'user', 'agent'
        message TEXT NOT NULL,
        metadata_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 9. Achievements & Badges
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        badge_key TEXT NOT NULL,
        badge_name TEXT NOT NULL,
        badge_desc TEXT NOT NULL,
        badge_icon TEXT NOT NULL,
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, badge_key),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    # 10. Resume Details
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        linkedin TEXT,
        github TEXT,
        portfolio TEXT,
        summary TEXT,
        education_json TEXT,
        experience_json TEXT,
        projects_json TEXT,
        skills_json TEXT,
        certifications_json TEXT,
        ats_score INTEGER DEFAULT 82,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    conn.commit()

    # Seed initial demo user if no user exists
    seed_demo_data(conn)
    conn.close()

def seed_demo_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = 'demo'")
    user = cursor.fetchone()

    if not user:
        # Create default demo student
        hashed_pw = generate_password_hash('demo123')
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, role)
        VALUES ('demo', 'demo@placementpro.ai', ?, 'student')
        ''', (hashed_pw,))
        user_id = cursor.lastrowid

        # Create admin user
        admin_pw = generate_password_hash('admin123')
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, role)
        VALUES ('admin', 'admin@placementpro.ai', ?, 'admin')
        ''', (admin_pw,))

        # Seed profile
        cursor.execute('''
        INSERT INTO student_profiles (user_id, full_name, college, branch, cgpa, graduation_year, target_company, target_package, bio)
        VALUES (?, 'Jordan Lee', 'Institute of Engineering & Technology', 'Computer Science & Engineering', 8.85, 2026, 'CloudScale Systems', '20-25 LPA',
        'Aspiring software engineer specialized in Full Stack Development, Data Structures, and Cloud Architecture.')
        ''', (user_id,))

        # Seed realistic study sessions (across last 7 days)
        now = datetime.now()
        sessions = [
            ('Data Structures & Algorithms', 5400, 90.0, 'Practiced tree traversal algorithms and recursive methods', now - timedelta(days=6)),
            ('Quantitative Aptitude', 3600, 60.0, 'Worked on work-rate and probability calculation problems', now - timedelta(days=5)),
            ('DBMS & SQL', 4500, 75.0, 'Reviewed index designs, normalization rules, and query optimization', now - timedelta(days=4)),
            ('Technical Interview Simulation', 3000, 50.0, 'Completed mock technical question drill on Operating Systems', now - timedelta(days=3)),
            ('Coding Practice (Python)', 6000, 100.0, 'Implemented graph search routines and tested corner test cases', now - timedelta(days=2)),
            ('HR Interview & Behavioral', 2400, 40.0, 'Practiced structured situation-action-result behavioral scenarios', now - timedelta(days=1)),
            ('Computer Networks', 4200, 70.0, 'Analyzed protocol models, socket programming, and connection phases', now - timedelta(hours=3))
        ]
        for subject, dur_sec, dur_min, notes, dt in sessions:
            cursor.execute('''
            INSERT INTO study_sessions (user_id, subject, duration_seconds, duration_minutes, notes, started_at, ended_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, subject, dur_sec, dur_min, notes, dt.strftime('%Y-%m-%d %H:%M:%S'), (dt + timedelta(seconds=dur_sec)).strftime('%Y-%m-%d %H:%M:%S')))

        # Seed goals
        cursor.execute('''
        INSERT INTO study_goals (user_id, title, goal_type, target_value, current_value, unit, is_completed)
        VALUES
        (?, 'Solve 5 Algorithm Challenges', 'daily', 5, 4, 'problems', 0),
        (?, 'Complete 2 Hours Quantitative Aptitude', 'daily', 2, 2, 'hours', 1),
        (?, 'Attempt 3 Mock Technical Interviews', 'weekly', 3, 2, 'tests', 0),
        (?, 'Log 15 Total Study Hours', 'weekly', 15, 12, 'hours', 0)
        ''', (user_id, user_id, user_id, user_id))

        # Seed progress records
        progress = [
            ('Data Structures', 'Balanced Tree Operations', 'Medium', 6, 'Grasped rotation mechanics and rebalancing logic', (now - timedelta(days=2)).strftime('%Y-%m-%d')),
            ('Quantitative Aptitude', 'Permutations & Probability', 'Hard', 15, 'Mastered combinatorial selection techniques', (now - timedelta(days=1)).strftime('%Y-%m-%d')),
            ('Operating Systems', 'Process Synchronization', 'Medium', 8, 'Analyzed mutual exclusion and semaphore primitives', now.strftime('%Y-%m-%d')),
            ('Coding', 'Dynamic Programming Fundamentals', 'Hard', 4, 'Explored memoization vs tabulation trade-offs', now.strftime('%Y-%m-%d'))
        ]
        for subj, top, diff, q_cnt, notes, l_date in progress:
            cursor.execute('''
            INSERT INTO progress_records (user_id, subject, topic, difficulty, questions_solved, notes, logged_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, subj, top, diff, q_cnt, notes, l_date))

        # Seed test results
        tests = [
            ('aptitude', 'Quantitative Aptitude Assessment', 'Aptitude', 85.0, 20, 17, 1200),
            ('technical', 'Computer Science Core Concepts', 'Core CS', 90.0, 20, 18, 950),
            ('company', 'Corporate Placement Comprehensive Mock', 'Enterprise Prep', 82.5, 40, 33, 2700),
            ('coding', 'Array & String Algorithmic Evaluation', 'Coding', 100.0, 5, 5, 1800),
            ('technical', 'Distributed Systems & Network Architecture', 'Core CS', 75.0, 20, 15, 1100)
        ]
        for t_type, t_title, cat, score, tot, cor, time_s in tests:
            cursor.execute('''
            INSERT INTO test_results (user_id, test_type, test_title, category, score, total_questions, correct_answers, time_taken_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, t_type, t_title, cat, score, tot, cor, time_s))

        # Seed coding submissions
        submissions = [
            ('PAIR_SUM', 'Find Pair with Target Sum', 'Python', 'def find_pair(nums, target):\n    lookup = set()\n    for n in nums:\n        if (target - n) in lookup:\n            return True\n        lookup.add(n)\n    return False', 'Accepted', 10, 10, 32),
            ('VALID_BRACKETS', 'Balanced Bracket Verification', 'Python', 'def is_balanced(text):\n    stack = []\n    pairs = {")": "(", "}": "{", "]": "["}\n    for ch in text:\n        if ch in pairs.values():\n            stack.append(ch)\n        elif ch in pairs:\n            if not stack or stack.pop() != pairs[ch]: return False\n    return len(stack) == 0', 'Accepted', 15, 15, 28),
            ('ARRAY_ROTATION', 'Cyclic Array Shift', 'Java', 'class Solution {\n    public void rotate(int[] nums, int k) {\n        // Efficient cyclic in-place reversal\n    }\n}', 'Accepted', 20, 20, 58),
            ('INTERVAL_MERGE', 'Merge Overlapping Ranges', 'Python', 'def merge_ranges(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = []\n    for cur in intervals:\n        if not merged or merged[-1][1] < cur[0]:\n            merged.append(cur)\n        else:\n            merged[-1][1] = max(merged[-1][1], cur[1])\n    return merged', 'Accepted', 12, 12, 44)
        ]
        for pid, ptitle, lang, code, status, ptc, ttc, rt in submissions:
            cursor.execute('''
            INSERT INTO coding_submissions (user_id, problem_id, problem_title, language, code, status, passed_testcases, total_testcases, runtime_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, pid, ptitle, lang, code, status, ptc, ttc, rt))

        # Seed badges / achievements
        badges = [
            ('first_session', 'First Track', 'Completed your first live tracking study session', 'fa-stopwatch'),
            ('streak_3', 'Consistency Champion', 'Maintained a 3-day active placement study streak', 'fa-fire'),
            ('code_warrior', 'Code Warrior', 'Solved 15+ algorithmic and data structure exercises', 'fa-code'),
            ('aptitude_ace', 'Aptitude Ace', 'Scored > 80% on 3 Aptitude Mock Examinations', 'fa-brain'),
            ('mock_master', 'Interview Ready', 'Completed technical and HR interview agent simulations', 'fa-user-tie')
        ]
        for bkey, bname, bdesc, bicon in badges:
            cursor.execute('''
            INSERT INTO achievements (user_id, badge_key, badge_name, badge_desc, badge_icon)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, bkey, bname, bdesc, bicon))

        # Seed Resume Data
        cursor.execute('''
        INSERT INTO resumes (user_id, full_name, email, phone, linkedin, github, portfolio, summary, education_json, experience_json, projects_json, skills_json, certifications_json, ats_score)
        VALUES (?, 'Jordan Lee', 'jordan.lee@example.com', '+91 98765 43210', 'https://linkedin.com/in/jordanlee', 'https://github.com/jordanlee', 'https://jordanlee.dev',
        'Results-oriented Computer Science undergraduate with proven expertise in algorithmic problem solving, full-stack architecture, and distributed systems. Recipient of national technical innovation award and active open-source contributor.',
        '[{"degree":"B.Tech in Computer Science & Engineering","institution":"Institute of Engineering & Technology","year":"2022 - 2026","grade":"8.85 CGPA"},{"degree":"Higher Secondary School Certificate (Science)","institution":"City Model Senior Secondary School","year":"2020 - 2022","grade":"95.4%"}]',
        '[{"title":"Software Engineering Intern","company":"Novatech Engineering Labs","period":"May 2025 - July 2025","description":"Engineered responsive web endpoints and relational schemas, reducing response latency by 35%. Implemented in-memory caching for high-volume transactions."}]',
        '[{"title":"Autonomous Placement Training Suite","tech":"Python Flask, SQLite, Chart.js, Intelligent Agents","description":"Architected an interactive multi-agent campus placement training platform with real-time timers, adaptive study plans, and evaluation dashboards."},{"title":"Distributed Event Streaming Gateway","tech":"Python, Redis, Docker, RESTful APIs","description":"Developed reliable publish-subscribe message pipeline sustaining high throughput with guaranteed at-least-once message delivery."}]',
        '{"languages":["Python","Java","C++","SQL","JavaScript"],"frameworks":["Flask","React","Node.js","Docker","Git"],"core":["Data Structures & Algorithms","Database Management Systems","Operating Systems","Computer Networks","Software Engineering"]}',
        '[{"name":"Cloud Foundations Certification","issuer":"Cloud Computing Consortium","year":"2025"},{"name":"Advanced Algorithmic Design Specialization","issuer":"Global Tech Academy","year":"2024"}]',
        88)
        ''', (user_id,))

        conn.commit()

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass
    init_db()
    print("Database refreshed and initialized successfully at:", DB_PATH)
