# AI PLACEMENT PRO 🎓🚀
### *Your Personal AI Placement Preparation Partner*

**AI PLACEMENT PRO** is a full-stack, autonomous, placement training platform engineered to prepare college engineering and graduate students for campus placements and technical recruitment drives.

The application integrates **four dedicated AI Placement Agents** with an interactive **Track Me** performance analytics engine, timed mock examinations, company-oriented preparation guides, an ATS resume builder, and an adaptive AI study planner.

---

## 🌟 Key Features & Systems

### 1. Student Performance Dashboard
- **Overall Placement Preparation Percentage:** Dynamically computed from test scores, coding submissions, and study logs.
- **Total Learning Hours:** Stored and aggregated in SQLite from live timer tracking.
- **Coding Problems Solved:** Real-time counter of verified algorithmic submissions.
- **Sectional Scores:** Quantitative Aptitude, Technical Interview, and HR / Behavioral readiness.
- **Daily Learning Streak:** Flame-animated consecutive day counter based on study activities.
- **Weekly Progress Chart:** Interactive **Chart.js** bar visualization of hours studied over the past 7 days.
- **Active Study Goals & Recent Activities Feed:** Real-time record of completed milestones.

### 2. Four Specialized AI Placement Agents
- 🧮 **Agent 1: Aptitude Agent**
  - Quantitative Aptitude (Time & Work, Speed-Distance, Probability, Permutations, Profit & Loss).
  - Logical Reasoning (Syllogisms, Blood Relations, Coding-Decoding).
  - Verbal Ability & Grammar.
  - Step-by-step mathematical breakdowns, shortcuts, and timed verification.
- 💻 **Agent 2: Coding Agent**
  - Languages: Python, Java, C++, and C.
  - Core DSA: Trees, Graphs, Dynamic Programming, Heaps, Two Pointers.
  - Built-in interactive code editor with syntax formatting and one-click testcase runner.
  - Big-O Time & Space Complexity analysis and code debugging.
- 🎙 **Agent 3: Technical Interview Agent**
  - Core CS Fundamentals: DBMS, Operating Systems, Computer Networks, OOP, System Design.
  - Interactive mock technical rounds with real-time scoring (out of 10), technical depth critique, and model answer formulation.
- 👔 **Agent 4: HR Interview Agent**
  - "Tell Me About Yourself" 3-part elevator pitch coaching (Present ➔ Past ➔ Future).
  - Behavioral questions evaluated using the **STAR Method** (Situation, Task, Action, Result).
  - Conflict resolution, career goals, weakness reframing, and group discussion etiquette.

### 3. Track Me System (Personal Performance Tracker)
- **Live Study Timer Widget:**
  - Select subject (DSA, Aptitude, DBMS, OS, Networks, HR, etc.).
  - **START TRACKING** countup timer with glowing animated indicators.
  - **STOP & SAVE SESSION** automatically commits duration to SQLite and increments total learning hours.
- **ADD PROGRESS Modal:** Manually record completed topics, difficulty levels, solved counts, and study takeaways.
- **Achievement Badges:** Automatically unlocks badges (*First Track, Consistency Champion, Code Warrior, Aptitude Ace, Week Titan*).
- **Persistent SQLite Tables:** Full historical logs of all sessions and progress entries survive application restarts.

### 4. AI Personalized Study Planner
- Analyzes individual student weaknesses across tests and practice logs.
- Isolates lowest-scoring subjects and generates daily study schedules (Morning, Afternoon, Evening blocks).
- Constructs weekly milestone roadmaps and suggests next immediate learning activities.

### 5. Mock Test System
- Timed assessments for Quantitative Aptitude, Core CS MCQs, and DSA Complexity Quizzes.
- Live countdown timer, question palette navigation, and early submit option.
- Automatic evaluation engine with instant score percentage, correct/incorrect status, and in-depth explanations for every option.

### 6. ATS-Friendly Resume Builder
- Structured editor for Profile, Education, Experience, Projects, and Skills.
- **AI Bullet Optimizer:** Enhances project statements with action verbs and quantifiable metrics.
- Synchronized live preview on a standard ATS-compliant template.
- Direct **Print / PDF Download** with dedicated `@media print` stylesheet.

### 7. Company Preparation (9 Top Employers)
- Dedicated syllabi, recruitment rounds, and preparation strategies for:
  - **TCS** (Ninja, Digital, Prime)
  - **Infosys** (Systems Engineer, Specialist Programmer)
  - **Wipro** (Elite, Turbo)
  - **Accenture** (Associate Software Engineer, Advanced ASE)
  - **Cognizant** (GenC, GenC Elevate, GenC Next)
  - **Capgemini** (Analyst, Game-based assessment)
  - **Zoho** (Application design & core logic)
  - **Amazon** (SDE-1, 16 Leadership Principles)
  - **Microsoft** (DSA, System design, Growth mindset)

---

## 🛠 Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6+), Chart.js 4, FontAwesome 6, Google Plus Jakarta Sans & Fira Code.
- **Backend:** Python Flask 3.1, SQLite 3, Werkzeug Security (PBKDF2 SHA-256 password hashing).
- **AI Engine:** Google Gemini API (`google-genai` SDK and REST endpoint) + Autonomous Domain-Expert Local Knowledge Engine for seamless offline / keyless operation.
- **Design:** Modern Dark Navy (`#0b0f19`) & Royal Purple (`#7c3aed`) SaaS theme with instant toggleable Light Mode.

---

## 🚀 Quick Start Guide (Windows PowerShell)

### Step 1: Open PowerShell and navigate to the project folder
```powershell
cd c:\Users\SHANTHOSH\OneDrive\Desktop\projectNN
```

### Step 2: Initialize or verify the SQLite database
```powershell
python database.py
```

### Step 3: Run the automated test suite
```powershell
python test_suite.py
```

### Step 4: Start the AI PLACEMENT PRO server
```powershell
python app.py
```

### Step 5: Open your web browser
Visit: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Demo Login Credentials

For quick testing, pre-seeded accounts are immediately available:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Student** | `demo` | `demo123` | Pre-populated with study history, goals, and test records |
| **Administrator** | `admin` | `admin123` | Administrative overview privileges |

You can also click **"Register Student"** on the auth page to create a brand new student account!

---

## ⚙️ Google Gemini API Configuration (Optional)

The application includes an **Autonomous Expert Knowledge Engine** that handles aptitude, coding, technical rounds, and HR feedback right out of the box with zero setup required.

To connect live Gemini Generative AI models:
1. Obtain a free API key at [Google AI Studio](https://aistudio.google.com/).
2. Either:
   - Add `GEMINI_API_KEY=your_key_here` to the `.env` file in the project root.
   - Or enter it directly in the in-app **Settings** screen (`13. Settings` in the sidebar).

---

## 📋 Database Architecture (SQLite)

The SQLite database file is stored at `placement_pro.db` and contains 10 relational tables:
1. `users`: Credentials, roles (student/admin), timestamps.
2. `student_profiles`: Academic branch, CGPA, target dream companies, target package.
3. `study_sessions`: Timer records, subjects, duration in seconds/minutes, notes.
4. `study_goals`: Daily and weekly targets, progress counters, completion status.
5. `progress_records`: Manual topic entries, difficulty ratings, questions solved.
6. `test_results`: Examination scores, correct answer counts, full JSON solution details.
7. `coding_submissions`: Code drafts, runtimes, status (Accepted / Wrong Answer).
8. `ai_conversations`: Persistent chat history with all 4 AI agents.
9. `achievements`: Dynamic badge unlock records.
10. `resumes`: Structured candidate resume data with ATS scoring.

---

*AI PLACEMENT PRO — Your Personal AI Placement Preparation Partner.*
"# AI-placement-pro" 
