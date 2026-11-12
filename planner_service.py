from database import get_db
import json
from ai_service import call_gemini_api

def analyze_student_performance(user_id):
    """
    Analyse student performance across tests, study sessions, and coding submissions.
    Returns: proficiency scores, weak subjects, total learning hours, solved problems count.
    """
    conn = get_db()
    cursor = conn.cursor()

    # 1. Total learning time (in hours)
    cursor.execute("SELECT SUM(duration_seconds) as total_sec FROM study_sessions WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    total_seconds = row["total_sec"] if row and row["total_sec"] else 0
    total_hours = round(total_seconds / 3600.0, 1)

    # 2. Coding problems solved
    cursor.execute("SELECT COUNT(*) as cnt FROM coding_submissions WHERE user_id = ? AND status = 'Accepted'", (user_id,))
    coding_count = cursor.fetchone()["cnt"]

    # 3. Test scores by category
    cursor.execute("""
    SELECT test_type, AVG(score) as avg_score, COUNT(*) as attempts
    FROM test_results
    WHERE user_id = ?
    GROUP BY test_type
    """, (user_id,))
    test_stats = {r["test_type"]: {"avg": round(r["avg_score"], 1), "attempts": r["attempts"]} for r in cursor.fetchall()}

    # 4. Progress records count
    cursor.execute("SELECT COUNT(*) as cnt FROM progress_records WHERE user_id = ?", (user_id,))
    progress_count = cursor.fetchone()["cnt"]

    # Calculate subject readiness percentages (0-100)
    aptitude_score = test_stats.get("aptitude", {}).get("avg", 65.0)
    technical_score = test_stats.get("technical", {}).get("avg", 70.0)
    coding_score = min(100.0, max(50.0, coding_count * 10 + (test_stats.get("coding", {}).get("avg", 75.0) * 0.5)))
    hr_score = 75.0 # baseline behavioral readiness

    # Identify weak subject
    scores = [
        ("Quantitative Aptitude", aptitude_score, "Permutations, Probability & Speed-Distance"),
        ("Technical Core CS", technical_score, "Operating Systems Paging & DBMS Indexing"),
        ("Data Structures & Algorithms", coding_score, "Dynamic Programming & Graph Algorithms"),
        ("HR & Communication", hr_score, "STAR Framework & Resume Behavioral Questions")
    ]
    scores.sort(key=lambda x: x[1])
    weakest = scores[0]

    # Calculate overall placement preparation percentage
    overall_readiness = round((aptitude_score * 0.25) + (technical_score * 0.3) + (coding_score * 0.3) + (hr_score * 0.15), 1)

    conn.close()

    return {
        "total_hours": total_hours,
        "coding_solved": coding_count,
        "progress_count": progress_count,
        "aptitude_score": aptitude_score,
        "technical_score": technical_score,
        "coding_score": round(coding_score, 1),
        "hr_score": hr_score,
        "overall_readiness": min(100.0, overall_readiness),
        "weak_subject": weakest[0],
        "weak_score": weakest[1],
        "weak_topics": weakest[2],
        "all_scores": scores
    }

def generate_personalized_study_plan(user_id, custom_api_key=None):
    """
    Generate an AI-driven personalized Daily & Weekly study plan based on analysis.
    """
    perf = analyze_student_performance(user_id)

    # Check if Gemini API is available
    if custom_api_key:
        prompt = f"""
Student Profile Summary:
- Overall Placement Readiness: {perf['overall_readiness']}%
- Weakest Area: {perf['weak_subject']} (Score: {perf['weak_score']}%)
- Recommended Focus Topics: {perf['weak_topics']}
- Total Hours Logged: {perf['total_hours']} hrs
- Algorithmic Problems Solved: {perf['coding_solved']}

Generate a concise, highly actionable Daily and Weekly Study Plan formatted in clean Markdown with:
1. Diagnostic Analysis (identifying specific weak spots)
2. Daily Schedule (Morning, Afternoon, Evening blocks with time allocation)
3. Weekly Milestone Goals (Monday to Sunday progression)
4. Recommended Next Placement Activity
"""
        reply = call_gemini_api(custom_api_key, "You are the AI Chief Placement Director.", [], prompt)
        if reply:
            return {
                "performance": perf,
                "plan_markdown": reply,
                "mode": "gemini_personalized"
            }

    # Autonomous pedagogical generator
    plan_md = f"""
### 📊 AI Placement Diagnostic Analysis
- **Overall Placement Readiness:** **{perf['overall_readiness']}%**
- **Identified Weakest Area:** **{perf['weak_subject']}** ({perf['weak_score']}% average score)
- **Primary Focus Need:** Re-enforce {perf['weak_topics']} to avoid sectional cutoffs in upcoming corporate assessments.

---

### 📅 AI Personalized Daily Study Plan (Target: 3.5 Hours)

| Time Window | Focus Subject | Actionable Task | Target Outcome |
| :--- | :--- | :--- | :--- |
| **Morning (45 mins)** | **{perf['weak_subject']}** | Solve 10 timed practice questions on {perf['weak_topics']} | Attain > 80% accuracy in under 1.5 mins/problem |
| **Afternoon (90 mins)** | **Data Structures & Algorithms** | Implement 2 Medium-level problems (Two Pointers / Sliding Window) | Write bug-free code with $O(N)$ time complexity |
| **Evening (45 mins)** | **Technical Interview (Core CS)** | Revise Operating Systems (Deadlocks & Virtual Memory) or DBMS ACID properties | Practice explaining concepts out loud to the Technical Agent |
| **Night (30 mins)** | **Behavioral & HR Practice** | Prepare 1 STAR scenario for teamwork and conflict resolution | Deliver concise 90-second elevator pitch to HR Agent |

---

### 🗓 Weekly Roadmap & Placement Milestones

- **Monday - Tuesday (Aptitude Surge):** Deep-dive into Time-Work, Speed-Distance, and Probability. Attempt 1 timed diagnostic test in the Mock Test module.
- **Wednesday - Thursday (Coding & Optimization):** Tree traversals (Inorder, Level-order) and Graph BFS/DFS. Focus on edge cases (null inputs, cycles).
- **Friday (Core CS & SQL):** Write complex SQL joins, subqueries, and review transaction isolation levels (Read Committed vs Serializable).
- **Saturday (Full Mock Assessment):** Attempt a 90-minute comprehensive mock placement exam under strict examination conditions.
- **Sunday (Revision & Resume Polish):** Review missed questions, update resume project metrics, and log weekly progress in Track Me.

---

### 🎯 Next Recommended Immediate Action
👉 **Start a 45-minute timed study session on '{perf['weak_subject']}' using the Track Me timer!**
"""

    return {
        "performance": perf,
        "plan_markdown": plan_md.strip(),
        "mode": "heuristic_ai"
    }
