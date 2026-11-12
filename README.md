# AI PLACEMENT PRO 🎓🚀
### Your Personal AI Placement Preparation Partner

AI PLACEMENT PRO is a full-stack AI-powered placement training platform designed to help college students prepare for campus placements and technical recruitment drives.

The application integrates four dedicated AI Placement Agents, an interactive Track Me performance analytics engine, timed mock examinations, company-oriented preparation guides, an ATS resume builder, and an adaptive AI study planner.

---

## 🌟 Key Features

### 1. Student Performance Dashboard
- Overall placement preparation percentage.
- Total learning hours tracked using SQLite.
- Coding problems solved counter.
- Sectional scores for Aptitude, Technical, and HR.
- Daily learning streak.
- Weekly progress charts using Chart.js.
- Active study goals and recent activities.

### 2. Four Specialized AI Placement Agents

**🧮 Agent 1: Aptitude Agent**
- Quantitative Aptitude.
- Logical Reasoning.
- Verbal Ability and Grammar.
- Step-by-step solutions and shortcuts.

**💻 Agent 2: Coding Agent**
- Python, Java, C++, and C.
- Data Structures and Algorithms.
- Trees, Graphs, Dynamic Programming, and Heaps.
- Code debugging and complexity analysis.

**🎙 Agent 3: Technical Interview Agent**
- DBMS, Operating Systems, Computer Networks, and OOP.
- System Design fundamentals.
- Interactive technical mock interviews.
- Interview feedback and model answers.

**👔 Agent 4: HR Interview Agent**
- Tell Me About Yourself coaching.
- STAR method behavioral questions.
- Career goals and weakness analysis.
- Conflict resolution and group discussion preparation.

### 3. Track Me – Personal Performance Tracker
- Live study timer.
- Subject selection.
- Start and stop study sessions.
- Automatic SQLite session storage.
- Manual progress tracking.
- Achievement badges.
- Historical study records.

### 4. AI Personalized Study Planner
- Identifies weak subjects.
- Generates personalized daily schedules.
- Morning, afternoon, and evening study plans.
- Weekly milestone roadmaps.
- Personalized learning recommendations.

### 5. Mock Test System
- Quantitative Aptitude tests.
- Core Computer Science MCQs.
- DSA complexity quizzes.
- Countdown timer.
- Question navigation.
- Automatic evaluation and explanations.

### 6. ATS-Friendly Resume Builder
- Profile and education sections.
- Experience and project details.
- Skills management.
- AI bullet point optimization.
- Live resume preview.
- Print and PDF download.

### 7. Company Preparation

Preparation resources for nine leading companies:

1. TCS
2. Infosys
3. Wipro
4. Accenture
5. Cognizant
6. Capgemini
7. Zoho
8. Amazon
9. Microsoft

---

## 🛠 Technology Stack

| Component | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| UI Charts | Chart.js 4 |
| Backend | Python Flask 3.1 |
| Database | SQLite 3 |
| Security | Werkzeug Security |
| AI Integration | Google Gemini API |
| SDK | google-genai |
| Design | Dark Navy and Royal Purple SaaS Theme |

---

## 🚀 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/kanagavijayan/AI-placement-pro.git
```

### Step 2: Navigate to the Project Folder

```bash
cd AI-placement-pro
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Gemini API configuration is optional if the local knowledge engine supports the requested functionality.

### Step 5: Initialize the Database

```bash
python database.py
```

### Step 6: Run the Application

```bash
python app.py
```

### Step 7: Open in Browser

Visit:

http://127.0.0.1:5000

---

## 🔑 Demo Login Credentials

| Role | Username | Password |
|---|---|---|
| Student | demo | demo123 |
| Administrator | admin | admin123 |

*Demo credentials are available only if the application initializes these accounts.*

---

## 📋 Database Architecture

The SQLite database (`placement_pro.db`) contains the following tables:

1. `users` – User accounts and roles.
2. `student_profiles` – Student academic details.
3. `study_sessions` – Study timer records.
4. `study_goals` – Learning targets.
5. `progress_records` – Student progress.
6. `test_results` – Examination results.
7. `coding_submissions` – Coding practice records.
8. `ai_conversations` – AI chat history.
9. `achievements` – Achievement records.
10. `resumes` – Resume information.

---

## 🎯 Project Objective

To provide students with an intelligent, personalized, and comprehensive placement preparation platform that improves technical knowledge, coding ability, interview confidence, and overall placement readiness.

---

**AI PLACEMENT PRO – Your Personal AI Placement Preparation Partner.** 🚀