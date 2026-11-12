import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def get_gemini_api_key(custom_key: str = None) -> str:
    """Retrieve Gemini API key from parameter, environment, or fresh .env file."""
    if custom_key and custom_key.strip():
        return custom_key.strip().strip("'\"")
    key = os.getenv("GEMINI_API_KEY", "").strip().strip("'\"")
    if not key:
        load_dotenv(override=True)
        key = os.getenv("GEMINI_API_KEY", "").strip().strip("'\"")
    return key

# System prompts for the 4 AI Placement Agents
SYSTEM_PROMPTS = {
    "aptitude": """You are the 'Aptitude Agent' in AI PLACEMENT PRO.
Your purpose: Train engineering and graduate students for campus placement aptitude tests.
Domain covers:
1. Quantitative Aptitude (Time & Work, Speed-Distance, Profit & Loss, Percentages, Permutations, Probability, Ratio & Proportion, Averages, Number Systems)
2. Logical Reasoning (Syllogisms, Blood Relations, Coding-Decoding, Seating Arrangements, Data Sufficiency, Series)
3. Verbal Ability (Sentence correction, Reading comprehension, Vocabulary, Para jumbles)

Guidelines:
- When a user asks for practice, generate realistic placement-level problems with multiple choices (A, B, C, D).
- When a user submits an answer or asks for an explanation, give a rigorous, crystal-clear STEP-BY-STEP breakdown, highlighting short-cuts, formulas, and common traps.
- Keep tone supportive, sharp, and encouraging.
- Format with markdown, bullet points, and highlighted formulas.""",

    "coding": """You are the 'Coding Agent' in AI PLACEMENT PRO.
Your purpose: Train students in programming (C, Python, Java, C++) and core Data Structures & Algorithms (DSA).
Domain covers:
1. DSA: Arrays, Linked Lists, Stacks, Queues, Trees, Binary Search Trees, Heaps, Graphs, Hashing, Dynamic Programming, Greedy, Recursion.
2. Coding challenges with difficulty levels (Easy, Medium, Hard).
3. Code debugging: Diagnose syntax/logical bugs, off-by-one errors, memory management, and time/space complexity bottlenecks.
4. Explanations: Explain code line-by-line, provide Big-O time and space complexity analysis, and suggest optimal alternatives.

Guidelines:
- Provide clean, readable, well-commented code blocks.
- Always state the Time Complexity and Space Complexity.
- If asked to debug, clearly point out the exact lines causing the bug, explain WHY it fails, and provide the corrected code.""",

    "technical": """You are the 'Technical Interview Agent' in AI PLACEMENT PRO.
Your purpose: Conduct realistic technical interview rounds for software engineering campus placements.
Domain covers:
1. DBMS (SQL queries, Normalization 1NF-BCNF, ACID properties, Transactions, B+ Trees, Indexing, NoSQL).
2. Operating Systems (Processes vs Threads, CPU Scheduling, Deadlocks, Virtual Memory, Paging, Semaphores).
3. Computer Networks (OSI 7 Layers, TCP/IP, TCP 3-way handshake, HTTP/HTTPS, DNS, Subnetting, Sockets).
4. Object-Oriented Programming (Polymorphism, Inheritance, Encapsulation, Abstraction, SOLID principles).
5. System Design & AI/ML basics (Client-Server, Caching, Load Balancing, Machine Learning basics).

Guidelines:
- Act like a senior technical interviewer at a top tech company.
- You can ask challenging conceptual and scenario-based questions.
- When the student provides an answer, give an objective evaluation:
  * Rating: (e.g. 8/10)
  * Strengths in answer
  * Missing technical depth or misconceptions
  * What the ideal interviewer-ready answer would look like.""",

    "hr": """You are the 'HR Interview Agent' in AI PLACEMENT PRO.
Your purpose: Prepare candidates for Behavioral, HR, and Leadership rounds in campus placements.
Domain covers:
1. "Tell me about yourself" (Elevator pitch structure: Present, Past, Future).
2. Behavioral questions using the STAR framework (Situation, Task, Action, Result).
3. Strengths and Weaknesses, Handling failure, Conflict resolution with teammates.
4. "Why should we hire you?", "Why this company?", Long-term career goals.
5. Group discussion tips and communication etiquette.

Guidelines:
- Be professional, warm, yet discerning.
- When evaluating user responses, analyze clarity, confidence, relevance, and alignment with corporate culture.
- Use the STAR framework analysis to point out missing metrics or vague statements.
- Provide a refined, punchy rewrite of their answer."""
}

def call_gemini_api(api_key: str, system_prompt: str, conversation_history: list, user_message: str) -> str:
    """Call Google Gemini API using google-genai or requests."""
    key = get_gemini_api_key(api_key)
    if not key:
        return None

    # Try using google-genai SDK first
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=key)

        # Build clean alternating contents
        contents = []
        history = list(conversation_history or [])
        # Exclude the very last entry if it matches user_message to prevent duplicate user turns
        if history and history[-1].get("message", "").strip() == user_message.strip():
            history = history[:-1]

        for msg in history[-8:]:
            role = "user" if msg.get("role") == "user" or msg.get("sender") == "user" else "model"
            text = (msg.get("message") or "").strip()
            if not text:
                continue
            if contents and contents[-1]["role"] == role:
                contents[-1]["parts"][0]["text"] += f"\n\n{text}"
            else:
                contents.append({"role": role, "parts": [{"text": text}]})

        # Ensure multiturn conversation starts with 'user'
        while contents and contents[0]["role"] != "user":
            contents.pop(0)

        # Add current user prompt
        contents.append({"role": "user", "parts": [{"text": user_message}]})

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        )

        for model_id in ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-2.5-flash-lite", "gemini-flash-latest"]:
            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    return response.text
            except Exception as model_err:
                continue
    except Exception as sdk_err:
        print(f"[AI Service] google-genai SDK call error: {sdk_err}")

    # Fallback to direct HTTP requests to Gemini REST endpoint
    for model_id in ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-2.5-flash-lite", "gemini-flash-latest"]:
        try:
            import requests
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={key}"
            payload = {
                "systemInstruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": user_message}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1024
                }
            }
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and parts[0].get("text"):
                        return parts[0].get("text", "")
            else:
                print(f"[AI Service] REST call to {model_id} returned {res.status_code}: {res.text[:180]}")
        except Exception as rest_err:
            print(f"[AI Service] REST call error: {rest_err}")

    return None

def test_gemini_connection(api_key: str = None) -> dict:
    """Test connection with the provided or configured Gemini API key."""
    key = get_gemini_api_key(api_key)
    if not key:
        return {
            "connected": False,
            "message": "No API key configured. Provide an API key in Settings or add GEMINI_API_KEY to .env."
        }
    try:
        reply = call_gemini_api(key, "You are a friendly system status verifier.", [], "Reply with 'CONNECTED' if you receive this.")
        if reply:
            return {
                "connected": True,
                "message": "Successfully connected to Google Gemini AI!",
                "response": reply.strip()
            }
        return {
            "connected": False,
            "message": "API key provided, but Gemini did not return a response. Please check that the key has Gemini API access enabled and quota available."
        }
    except Exception as e:
        return {
            "connected": False,
            "message": f"Connection failed with error: {str(e)}"
        }

def generate_agent_response(agent_type: str, user_message: str, conversation_history: list = None, custom_api_key: str = None) -> dict:
    """Generate intelligent response for the specified agent."""
    if conversation_history is None:
        conversation_history = []

    system_prompt = SYSTEM_PROMPTS.get(agent_type, SYSTEM_PROMPTS["aptitude"])

    # 1. Try Live Gemini API call if key is provided
    api_key_to_use = get_gemini_api_key(custom_api_key)
    if api_key_to_use:
        live_reply = call_gemini_api(api_key_to_use, system_prompt, conversation_history, user_message)
        if live_reply:
            return {
                "status": "success",
                "mode": "live_gemini",
                "reply": live_reply,
                "agent_type": agent_type
            }

    # 2. Expert Offline/Demo AI Engine
    # Provides domain-accurate answers, step-by-step math, code solutions, interview feedback
    fallback_reply = generate_expert_fallback(agent_type, user_message)
    return {
        "status": "success",
        "mode": "local_expert_engine",
        "reply": fallback_reply,
        "agent_type": agent_type,
        "note": "Running on Autonomous Expert Knowledge Engine. To switch to live Gemini API, configure your key in Settings or .env."
    }

def generate_expert_fallback(agent_type: str, message: str) -> str:
    """High-quality contextual placement tutor for offline/demo operation."""
    msg = message.lower().strip()

    if agent_type == "aptitude":
        if any(w in msg for w in ["work", "time and work", "pipes"]):
            return (
                "### 🎯 Time & Work: Master Concept & Practice Problem\n\n"
                "**Core Formula:**\n"
                "- If Person A completes a task in $x$ days, their 1-day work rate is $\\frac{1}{x}$.\n"
                "- If Person B completes the task in $y$ days, their 1-day work rate is $\\frac{1}{y}$.\n"
                "- Combined work rate: $\\frac{1}{x} + \\frac{1}{y} = \\frac{x + y}{xy}$.\n"
                "- Days needed together: $\\frac{xy}{x + y}$.\n\n"
                "**Placement Practice Question:**\n"
                "> *Worker A can finish an engineering project in 12 days. Worker B can finish it in 18 days. Both work together for 4 days, after which Worker A leaves. How many more days will Worker B take to complete the remaining project alone?*\n\n"
                "**Options:**\n"
                "- A) 6 days\n- B) 8 days\n- C) 9 days\n- D) 10 days\n\n"
                "**Step-by-step Solution:**\n"
                "1. Total Units of Work = LCM(12, 18) = **36 units**.\n"
                "2. Efficiency of A = $36 / 12 = 3$ units/day.\n"
                "3. Efficiency of B = $36 / 18 = 2$ units/day.\n"
                "4. Combined Efficiency = $3 + 2 = 5$ units/day.\n"
                "5. In 4 days together, they complete: $4 \\times 5 = 20$ units.\n"
                "6. Remaining Work = $36 - 20 = 16$ units.\n"
                "7. Time taken by B alone = $16 / 2 =$ **8 days**.\n\n"
                "✅ **Correct Answer: Option B (8 days)**\n\n"
                "💡 *Pro-Tip:* Always use the LCM (Unit Work) method rather than fractions to calculate in under 45 seconds during timed tests!"
            )
        elif any(w in msg for w in ["speed", "distance", "train", "relative"]):
            return (
                "### ⚡ Speed, Time & Distance: Relative Speed Analysis\n\n"
                "**Key Conversions & Rules:**\n"
                "- $1 \\text{ km/h} = \\frac{5}{18} \\text{ m/s}$\n"
                "- When two objects move in opposite directions: $S_{rel} = S_1 + S_2$\n"
                "- When two objects move in the same direction: $S_{rel} = |S_1 - S_2|$\n\n"
                "**Placement Challenge:**\n"
                "> *A train 180 meters long passes an express train 120 meters long travelling in the opposite direction at 54 km/h in 10 seconds. What is the speed of the first train in km/h?*\n\n"
                "**Step-by-Step Breakdown:**\n"
                "1. Total Distance = Length of Train 1 + Length of Train 2 = $180 + 120 = 300\\text{ meters}$.\n"
                "2. Time = $10\\text{ seconds}$.\n"
                "3. Relative Speed = $\\frac{\\text{Distance}}{\\text{Time}} = \\frac{300}{10} = 30\\text{ m/s}$.\n"
                "4. Convert relative speed to km/h: $30 \\times \\frac{18}{5} = 108\\text{ km/h}$.\n"
                "5. Since they travel in opposite directions: $S_1 + S_2 = 108\\text{ km/h}$.\n"
                "6. Given $S_2 = 54\\text{ km/h}$, hence $S_1 = 108 - 54 =$ **54 km/h**.\n\n"
                "✅ **Result: 54 km/h**"
            )
        elif any(w in msg for w in ["probability", "permutation", "combination"]):
            return (
                "### 🎲 Permutations & Probability Framework\n\n"
                "**Placement Rules:**\n"
                "- Permutations (Order matters): $P(n, r) = \\frac{n!}{(n-r)!}$\n"
                "- Combinations (Order does not matter): $C(n, r) = \\frac{n!}{r!(n-r)!}$\n"
                "- Probability: $P(E) = \\frac{n(E)}{n(S)}$\n\n"
                "**Frequent Campus Question:**\n"
                "> *A box contains 5 red balls, 4 green balls, and 3 blue balls. If 2 balls are drawn at random without replacement, what is the probability that both are of the same color?*\n\n"
                "**Calculation:**\n"
                "1. Total balls = $5 + 4 + 3 = 12$.\n"
                "2. Total outcomes $n(S) = C(12, 2) = \\frac{12 \\times 11}{2} = 66$.\n"
                "3. Favorable outcomes (Both Red OR Both Green OR Both Blue):\n"
                "   - Both Red: $C(5, 2) = 10$\n"
                "   - Both Green: $C(4, 2) = 6$\n"
                "   - Both Blue: $C(3, 2) = 3$\n"
                "4. $n(E) = 10 + 6 + 3 = 19$.\n"
                "5. Probability = **19 / 66** (approx **28.78%**).\n\n"
                "Would you like another numerical practice problem or a timed set?"
            )
        else:
            return (
                "### 🧠 Quantitative & Logical Aptitude Coach\n\n"
                "Welcome to your dedicated Aptitude Session! In major campus placement assessments (like TCS NQT, Infosys, Accenture, Cognizant, and product evaluations), aptitude determines whether your technical profile gets reviewed.\n\n"
                "**Choose an area to practice right now:**\n"
                "1. ⏱ **Quantitative Aptitude:** Time & Work, Speed & Distance, Profit/Loss, Probability, Permutations, Simple & Compound Interest\n"
                "2. 🧩 **Logical Reasoning:** Syllogisms, Blood Relations, Seating Arrangements, Coding-Decoding\n"
                "3. 📖 **Verbal Ability:** Reading Comprehension, Sentence Correction, Para Jumbles\n\n"
                "*Type any topic or ask: 'Give me 3 quantitative questions on Time & Work' to begin immediate practice!*"
            )

    elif agent_type == "coding":
        if any(w in msg for w in ["reverse", "linked list"]):
            return (
                "### 💻 Reverse a Singly Linked List (Optimal Solution)\n\n"
                "**Problem Statement:** Given the head of a singly linked list, reverse the list in-place and return the new head.\n\n"
                "```python\n"
                "class ListNode:\n"
                "    def __init__(self, val=0, next=None):\n"
                "        self.val = val\n"
                "        self.next = next\n\n"
                "def reverseList(head: ListNode) -> ListNode:\n"
                "    prev = None\n"
                "    curr = head\n"
                "    while curr is not None:\n"
                "        nxt = curr.next     # 1. Save next node\n"
                "        curr.next = prev    # 2. Reverse current pointer\n"
                "        prev = curr         # 3. Advance prev pointer\n"
                "        curr = nxt          # 4. Advance curr pointer\n"
                "    return prev             # prev is the new head\n"
                "```\n\n"
                "**Complexity Analysis:**\n"
                "- **Time Complexity:** $O(N)$ - single pass through the linked list of length $N$.\n"
                "- **Space Complexity:** $O(1)$ - in-place pointer reversal without extra heap memory.\n\n"
                "**Common Interview Follow-Up:** *Can you solve this recursively?* Yes, with $O(N)$ call stack space."
            )
        elif any(w in msg for w in ["tree", "traversal", "dfs", "bfs", "binary"]):
            return (
                "### 🌳 Binary Tree Traversals: Recursive & Iterative\n\n"
                "**Key Traversal Orders:**\n"
                "1. **Inorder (Left, Root, Right):** Produces sorted order for a Binary Search Tree (BST).\n"
                "2. **Preorder (Root, Left, Right):** Useful for cloning or serializing trees.\n"
                "3. **Postorder (Left, Right, Root):** Useful for bottom-up computation (e.g., tree height, deletion).\n"
                "4. **Level Order (BFS):** Uses a FIFO Queue to traverse level-by-level.\n\n"
                "```python\n"
                "from collections import deque\n\n"
                "def levelOrder(root):\n"
                "    if not root: return []\n"
                "    result, queue = [], deque([root])\n"
                "    while queue:\n"
                "        level_size = len(queue)\n"
                "        level = []\n"
                "        for _ in range(level_size):\n"
                "            node = queue.popleft()\n"
                "            level.append(node.val)\n"
                "            if node.left: queue.append(node.left)\n"
                "            if node.right: queue.append(node.right)\n"
                "        result.append(level)\n"
                "    return result\n"
                "```\n\n"
                "- **Time:** $O(N)$ | **Space:** $O(W)$ where $W$ is maximum tree width."
            )
        elif any(w in msg for w in ["debug", "error", "bug"]):
            return (
                "### 🛠 Code Debugging & Optimization Assistant\n\n"
                "I am ready to review your code! Please paste your snippet along with:\n"
                "1. The programming language (Python, C++, Java, C)\n"
                "2. The expected output vs actual output/error message\n"
                "3. Any constraints or failing edge cases (e.g. empty inputs, large arrays, negative values)\n\n"
                "*Tip:* I inspect pointer bounds, off-by-one indices, recursion termination, memory leaks, and Big-O efficiency."
            )
        else:
            return (
                "### 🚀 Algorithmic Problem Solving & Code Engine\n\n"
                "I can help you build coding fluency in **C, Python, Java, and C++** for placement interviews.\n\n"
                "**Available Activities:**\n"
                "- 📝 **Coding Challenge:** Ask me for an *Easy*, *Medium*, or *Hard* challenge on Arrays, Hash Tables, Trees, or Dynamic Programming.\n"
                "- 🔍 **Code Review & Debug:** Paste your code and I will find bugs and optimize time complexity.\n"
                "- ⏱ **Big-O Analysis:** Ask how to optimize an $O(N^2)$ algorithm down to $O(N \\log N)$ or $O(N)$.\n\n"
                "*Try asking:* 'Give me a medium dynamic programming challenge with sample test cases.'"
            )

    elif agent_type == "technical":
        if any(w in msg for w in ["dbms", "sql", "acid", "index", "normalization"]):
            return (
                "### 🗄 Technical Round: DBMS Core Fundamentals\n\n"
                "**Top Placement Topic: ACID Properties & Indexing**\n\n"
                "1. **Atomicity:** All operations in a transaction succeed, or the entire transaction is rolled back (All-or-Nothing). Managed via Undo Logs.\n"
                "2. **Consistency:** Database transitions only between valid states conforming to integrity constraints.\n"
                "3. **Isolation:** Concurrent transactions execute without interfering with one another. Enforced using Locks and MVCC (Multi-Version Concurrency Control).\n"
                "4. **Durability:** Once committed, changes survive power outages or system crashes. Managed via Redo/Write-Ahead Logging (WAL).\n\n"
                "**Interviewer Follow-Up Question:**\n"
                "> *Why are B+ Trees preferred over Binary Search Trees or Hash Tables for relational database indexing on disk?*\n\n"
                "**Model Answer:**\n"
                "- **High Fan-Out & Low Height:** B+ Trees have large branching factors, requiring only 3-4 disk I/O reads even for millions of records.\n"
                "- **Range Queries:** In B+ Trees, all leaf nodes are linked sequentially via pointers, making queries like `WHERE age BETWEEN 20 AND 30` ultra-fast $O(\\log N + K)$ compared to Hash indexing which only supports equality lookups $O(1)$."
            )
        elif any(w in msg for w in ["os", "operating system", "deadlock", "process", "thread"]):
            return (
                "### 💻 Technical Round: Operating Systems & Concurrency\n\n"
                "**The 4 Coffman Conditions for Deadlock:**\n"
                "Deadlock can occur if and only if all 4 conditions hold simultaneously:\n"
                "1. **Mutual Exclusion:** At least one resource must be non-shareable.\n"
                "2. **Hold and Wait:** A process holding at least one resource is waiting to acquire additional resources held by other processes.\n"
                "3. **No Preemption:** Resources cannot be forcibly seized from a process holding them.\n"
                "4. **Circular Wait:** A closed chain of processes exists such that each process holds a resource that the next process in the chain needs.\n\n"
                "**Deadlock Prevention Strategies:**\n"
                "- Impose an order on resource acquisition to eliminate Circular Wait.\n"
                "- Banker's Algorithm for deadlock avoidance (safe state verification).\n\n"
                "**Practice Evaluation:** How would you answer: *'What is the difference between a Process and a Thread, and what resources are shared between threads?'*"
            )
        elif any(w in msg for w in ["network", "tcp", "udp", "osi", "http"]):
            return (
                "### 🌐 Technical Round: Computer Networks\n\n"
                "**TCP 3-Way Handshake (Connection Establishment):**\n"
                "1. **SYN (Synchronize):** Client sends a SYN segment with Initial Sequence Number (ISN) $x$ to the server.\n"
                "2. **SYN-ACK (Synchronize-Acknowledge):** Server responds with SYN segment with its own ISN $y$ and ACK $x + 1$.\n"
                "3. **ACK (Acknowledge):** Client sends ACK $y + 1$. Connection state is now `ESTABLISHED`.\n\n"
                "**Key Placement Comparison: TCP vs UDP**\n"
                "- **TCP:** Connection-oriented, reliable (flow control, retransmission), higher overhead. Used in HTTP, SSH, FTP, SMTP.\n"
                "- **UDP:** Connectionless, unreliable/best-effort, low latency, header only 8 bytes. Used in DNS, VoIP, Video Streaming, Gaming."
            )
        else:
            return (
                "### 🎙 Technical Interview Simulator\n\n"
                "Hello! I am your Technical Interviewer. I evaluate your depth in **Data Structures, DBMS, Operating Systems, Computer Networks, and System Design**.\n\n"
                "**Let's simulate a technical question:**\n"
                "> *'Can you explain what happens under the hood from the moment you type https://www.google.com into your browser and press Enter until the web page renders on your screen?'*\n\n"
                "Please respond with your answer as you would speak in an actual technical interview round, and I will grade your answer out of 10 with detailed constructive feedback!"
            )

    elif agent_type == "hr":
        if any(w in msg for w in ["introduce", "yourself", "intro", "tell me about"]):
            return (
                "### 👔 Mastering 'Tell Me About Yourself'\n\n"
                "**The Winning 3-Part Placement Formula (Present ➔ Past ➔ Future):**\n\n"
                "1. **Present (30 seconds):**\n"
                "   - Your degree, institution, and core technical identity.\n"
                "   *Example:* 'I am an engineering senior at XYZ Institute specializing in Computer Science, passionate about building robust backend systems and intuitive web solutions.'\n\n"
                "2. **Past (45 seconds):**\n"
                "   - Highlight 1-2 major projects, internships, or competitive milestones.\n"
                "   *Example:* 'During my internship at Novatech, I developed scalable REST APIs that reduced transaction response times by 35%. I also led my college team to 1st place in a 36-hour hackathon.'\n\n"
                "3. **Future (20 seconds):**\n"
                "   - Why this specific company and how your ambition matches their goals.\n"
                "   *Example:* 'I have been following your team’s recent developments in distributed infrastructure, and I am excited to contribute my problem-solving skills to your engineering initiatives.'\n\n"
                "**Action:** Draft your 90-second self-introduction below, and I will critique its delivery and word choice!"
            )
        elif any(w in msg for w in ["weakness", "strength", "conflict", "failure"]):
            return (
                "### 🌟 Behavioral Rounds: The STAR Framework\n\n"
                "When answering questions like *'Tell me about a time you handled a difficult conflict with a teammate'*, always structure your answer using **STAR**:\n\n"
                "- **S (Situation):** Set the scene concisely (time, team context, goal).\n"
                "- **T (Task):** Describe your specific responsibility or the dilemma faced.\n"
                "- **A (Action):** The proactive steps YOU took (open communication, objective data, compromise).\n"
                "- **R (Result):** The positive outcome, quantified metrics, and what you learned.\n\n"
                "**How to frame a Weakness:**\n"
                "Never say *'I have no weaknesses'* or *'I am too much of a perfectionist'*. Instead, pick a genuine technical or soft skill (e.g., public speaking or initial delegation), and immediately describe the concrete steps you are actively taking to improve."
            )
        else:
            return (
                "### 🤝 HR & Behavioral Round Partner\n\n"
                "Welcome to your HR preparation session! HR and management rounds assess your **communication clarity, emotional intelligence, cultural fit, and resilience**.\n\n"
                "**Common High-Impact Questions we can practice:**\n"
                "1. *'Tell me about yourself and your career aspirations.'*\n"
                "2. *'Why do you want to join our organization over others?'*\n"
                "3. *'Tell me about a challenging project deadline and how you handled pressure.'*\n"
                "4. *'Where do you see yourself in 3 to 5 years?'*\n"
                "5. *'What are your salary expectations and relocation preferences?'*\n\n"
                "Type your response to any question, and I will evaluate it on **Clarity, Impact, and Professionalism**!"
            )

    return "Thank you for reaching out! Let me know what specific placement topic you'd like to work on."
