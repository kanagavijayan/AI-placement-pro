# Company-Oriented Placement Preparation Guides & Practice Blueprints
# Note: Syllabi and patterns represent educational recruitment frameworks. Practice questions are original skill-building drills.

COMPANIES_DATA = {
    "tcs": {
        "id": "tcs",
        "name": "Tata Consultancy Services (TCS)",
        "logo_icon": "fa-building",
        "category": "Service & Digital Solutions",
        "roles": "Ninja (3.6 LPA) / Digital (7.0 LPA) / Prime (9.0 LPA)",
        "rounds": [
            {
                "round_num": 1,
                "title": "National Qualifier Test (NQT)",
                "duration": "120-140 mins",
                "components": [
                    "Numerical Ability (Arithmetic, Algebra, Statistics, Data Interpretation)",
                    "Verbal Ability (Vocabulary, Sentence Completion, Reading Comprehension)",
                    "Reasoning Ability (Puzzles, Syllogisms, Critical Thinking)",
                    "Hands-on Coding (1 Easy array/string problem + 1 Medium logic/math problem)"
                ]
            },
            {
                "round_num": 2,
                "title": "Technical Interview",
                "duration": "30-45 mins",
                "components": [
                    "Object-Oriented Programming (Polymorphism, Inheritance)",
                    "SQL Queries (Joins, Aggregates, Group By)",
                    "Candidate Final Year Project walkthrough",
                    "Basic Data Structures (Arrays, Linked Lists, Stacks)"
                ]
            },
            {
                "round_num": 3,
                "title": "Managerial & HR Interview",
                "duration": "20 mins",
                "components": [
                    "Willingness to relocate & shift timings",
                    "Teamwork, conflict management, and learning adaptability"
                ]
            }
        ],
        "key_tips": [
            "TCS NQT has negative marking in some sections; avoid blind guesses.",
            "In the coding round, ensure your code compiles with zero syntax errors; partial test cases yield partial scores.",
            "Be prepared to explain every line of code in your resume projects."
        ],
        "drill_topics": ["Arrays & Math", "SQL Joins", "Time & Work", "Syllogisms", "Object Oriented Design"]
    },

    "infosys": {
        "id": "infosys",
        "name": "Infosys",
        "logo_icon": "fa-network-wired",
        "category": "IT Consulting & Digital",
        "roles": "Systems Engineer (3.6 LPA) / Specialist Programmer (9.5 LPA) / DSE (6.5 LPA)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Online Aptitude & Reasoning Assessment",
                "duration": "100 mins",
                "components": [
                    "Mathematical Critical Thinking (Probability, Speed-Time, Permutations)",
                    "Logical Reasoning (Cryptarithmetic, Data Sufficiency, Deductive logic)",
                    "Verbal Ability & English Grammar"
                ]
            },
            {
                "round_num": 2,
                "title": "Pseudocode & Coding Assessment (HackWithInfy / SP)",
                "duration": "180 mins (for SP/DSE)",
                "components": [
                    "Data Structures: Dynamic Programming, Graph Traversals, Greedy, Trees"
                ]
            },
            {
                "round_num": 3,
                "title": "Combined Technical + HR Interview",
                "duration": "30 mins",
                "components": [
                    "Data Structures, DBMS basics, and behavioral scenario questions"
                ]
            }
        ],
        "key_tips": [
            "Infosys sectional cutoffs are strict; allocate equal preparation to Cryptarithmetic and Verbal sections.",
            "For Specialist Programmer roles, focus heavily on Graph BFS/DFS and DP table formulations."
        ],
        "drill_topics": ["Cryptarithmetic Logic", "Graph Traversal", "Permutations", "Dynamic Programming"]
    },

    "wipro": {
        "id": "wipro",
        "name": "Wipro",
        "logo_icon": "fa-laptop-code",
        "category": "IT & Consulting",
        "roles": "Project Engineer (Elite: 3.5 LPA / Turbo: 6.5 LPA)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Elite Assessment (Online Test)",
                "duration": "128 mins",
                "components": [
                    "Quants, Logical & Verbal Aptitude",
                    "Written Communication (Essay writing 20 mins)",
                    "Coding Section (2 Problems: 1 Simple loop logic + 1 Array manipulation)"
                ]
            },
            {
                "round_num": 2,
                "title": "Technical Round",
                "duration": "30 mins",
                "components": [
                    "Basics of C/Java/Python, Pointers, Arrays, SQL basics, and Academic Projects"
                ]
            },
            {
                "round_num": 3,
                "title": "HR Round",
                "duration": "15-20 mins",
                "components": [
                    "Communication check, relocation willingness, career expectations"
                ]
            }
        ],
        "key_tips": [
            "Essay writing is evaluated automatically; focus on correct punctuation, grammar, and 150-200 words.",
            "In coding, test edge cases such as empty input arrays and negative integers."
        ],
        "drill_topics": ["Essay Grammar", "Array Rotation", "Pointers & References", "Logical Deduction"]
    },

    "accenture": {
        "id": "accenture",
        "name": "Accenture",
        "logo_icon": "fa-chart-pie",
        "category": "Strategy & Technology Consulting",
        "roles": "Associate Software Engineer (4.5 LPA) / Advanced ASE (6.5 LPA)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Cognitive & Technical Assessment",
                "duration": "90 mins",
                "components": [
                    "Cognitive: Critical Thinking, Abstract Reasoning, English Ability",
                    "Technical: Pseudocode, Common Applications & MS Office, Cloud & Network Security"
                ]
            },
            {
                "round_num": 2,
                "title": "Coding Assessment (Unlocks if Round 1 cleared)",
                "duration": "45 mins",
                "components": [
                    "2 Coding problems (String manipulation, number systems, binary bitwise operators)"
                ]
            },
            {
                "round_num": 3,
                "title": "Communication Assessment & Virtual Interview",
                "duration": "30 mins",
                "components": [
                    "Automated speech fluency, reading comprehension, and panel discussion"
                ]
            }
        ],
        "key_tips": [
            "Pseudocode section is unique to Accenture: practice tracing recursion and nested loops.",
            "Communication round tests pronunciation, reading aloud, and active listening."
        ],
        "drill_topics": ["Pseudocode Tracing", "Bitwise Operations", "String Parsing", "Cloud & Security Concepts"]
    },

    "cognizant": {
        "id": "cognizant",
        "name": "Cognizant (CTS)",
        "logo_icon": "fa-microchip",
        "category": "IT & Business Services",
        "roles": "GenC (4.0 LPA) / GenC Next (6.75 LPA) / GenC Elevate (5.4 LPA)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Cognizant Communication & Skill Assessment",
                "duration": "100 mins",
                "components": [
                    "Quantitative & Analytical Ability",
                    "English comprehension & grammar",
                    "GenC Next: Advanced Coding (Dynamic Programming, Trees, Hashing)"
                ]
            },
            {
                "round_num": 2,
                "title": "Technical & HR Discussion",
                "duration": "35 mins",
                "components": [
                    "Programming language fundamentals, database normalization, project architecture"
                ]
            }
        ],
        "key_tips": [
            "For GenC Elevate, demonstrate strong object-oriented and web fundamentals.",
            "Be crystal clear on normalization up to 3NF and ACID properties."
        ],
        "drill_topics": ["Database Normalization", "Tree Algorithms", "Quantitative Aptitude", "OOPS Concepts"]
    },

    "capgemini": {
        "id": "capgemini",
        "name": "Capgemini",
        "logo_icon": "fa-cube",
        "category": "Consulting & Digital Transformation",
        "roles": "Analyst (4.25 LPA) / Senior Analyst (5.75 - 7.5 LPA)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Online Aptitude & Game-Based Assessment",
                "duration": "80 mins",
                "components": [
                    "Pseudocode (Data types, control structures, algorithm tracing)",
                    "English & Communication test",
                    "Game-based cognitive challenges (Grid memory, inductive reasoning, motion planning)"
                ]
            },
            {
                "round_num": 2,
                "title": "Coding Round & Technical Interview",
                "duration": "45 mins",
                "components": [
                    "Hands-on coding followed by project review and CS fundamentals"
                ]
            }
        ],
        "key_tips": [
            "Game-based assessments evaluate spatial memory and speed under pressure; practice mental math and reaction drills.",
            "Pseudocode questions often test operator precedence and recursion depth."
        ],
        "drill_topics": ["Game-based Reasoning", "Pseudocode Tracing", "C++ / Java Basics", "Memory Paging"]
    },

    "zoho": {
        "id": "zoho",
        "name": "Zoho Corporation",
        "logo_icon": "fa-cogs",
        "category": "SaaS Product Development",
        "roles": "Software Developer (6.0 - 10.0 LPA)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Basic Programming & Aptitude",
                "duration": "90 mins",
                "components": [
                    "C Programming output questions, pointer arithmetic, recursion tracing",
                    "Quantitative math & logical problem solving"
                ]
            },
            {
                "round_num": 2,
                "title": "Basic Coding Round",
                "duration": "120 mins",
                "components": [
                    "Pattern printing, string manipulations, matrix transformations without built-in library functions"
                ]
            },
            {
                "round_num": 3,
                "title": "Advanced Coding Round (Application Design)",
                "duration": "180 mins",
                "components": [
                    "Designing complete small applications (e.g., Railway Reservation System, Invoice Generator, Ludo simulator)"
                ]
            },
            {
                "round_num": 4,
                "title": "Technical & General HR Round",
                "duration": "45 mins",
                "components": [
                    "In-depth design code review and problem-solving mindset evaluation"
                ]
            }
        ],
        "key_tips": [
            "Zoho strongly emphasizes core logic over library built-ins (e.g. implementing your own string split/reverse).",
            "In round 3, modular OOP design, edge-case validation, and clean console menus are crucial."
        ],
        "drill_topics": ["Matrix Traversal", "System Console Simulation", "Pointer Arithmetic", "Pattern Algorithms"]
    },

    "amazon": {
        "id": "amazon",
        "name": "Amazon",
        "logo_icon": "fa-cubes-stacked",
        "category": "Big Tech & Cloud (Product)",
        "roles": "SDE-1 (40 - 45 LPA CTC)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Online Assessment (OA)",
                "duration": "90 mins",
                "components": [
                    "2 Algorithmic Coding Problems (Arrays, Trees, Graphs, DP)",
                    "Work Simulation Assessment (Workplace scenarios & decisions)",
                    "Amazon 16 Leadership Principles questionnaire"
                ]
            },
            {
                "round_num": 2,
                "title": "Technical Interview 1 (DSA & Problem Solving)",
                "duration": "60 mins",
                "components": [
                    "Optimal algorithm formulation, Big-O proof, edge cases, clean production-grade code"
                ]
            },
            {
                "round_num": 3,
                "title": "Technical Interview 2 (System Architecture & CS Fundamentals)",
                "duration": "60 mins",
                "components": [
                    "Low-Level Design (LLD), OOP Principles, Concurrency, and OS/DB internals"
                ]
            },
            {
                "round_num": 4,
                "title": "Bar Raiser Interview",
                "duration": "60 mins",
                "components": [
                    "In-depth behavioral scrutiny using Amazon Leadership Principles (Customer Obsession, Ownership, Deliver Results) via STAR method"
                ]
            }
        ],
        "key_tips": [
            "Every interview round includes at least 15-20 minutes of behavioral questions tied to Leadership Principles.",
            "Write production-grade code with meaningful variable names, modular helper functions, and comprehensive constraint checks."
        ],
        "drill_topics": ["Binary Search & Two Pointers", "Trees & Graphs", "Dynamic Programming", "Amazon Leadership Principles"]
    },

    "microsoft": {
        "id": "microsoft",
        "name": "Microsoft",
        "logo_icon": "fa-windows",
        "category": "Big Tech & Enterprise Cloud",
        "roles": "Software Engineer (40 - 48 LPA CTC)",
        "rounds": [
            {
                "round_num": 1,
                "title": "Online Coding Assessment",
                "duration": "90 mins",
                "components": [
                    "2-3 Algorithmic challenges (Strings, Hash Maps, Priority Queues, DFS/BFS)"
                ]
            },
            {
                "round_num": 2,
                "title": "Technical Rounds (3 Rounds)",
                "duration": "45-60 mins each",
                "components": [
                    "Round 1: Data Structures & Algorithms",
                    "Round 2: Systems, Memory Architecture, Concurrency, and Low-Level Object Oriented Design",
                    "Round 3: Behavioral, Culture, and Growth Mindset"
                ]
            },
            {
                "round_num": 3,
                "title": "AA Round (As Appropriate / Partner Director)",
                "duration": "45 mins",
                "components": [
                    "Architectural vision, adaptability, passion for technology, and past projects"
                ]
            }
        ],
        "key_tips": [
            "Microsoft interviewers deeply care about your thought process: speak your assumptions out loud before writing code.",
            "Always test your code dry-run with null, single-element, and maximum constraint cases."
        ],
        "drill_topics": ["Tree Serialization", "Shortest Path & Graphs", "Memory & Threading", "Growth Mindset Scenarios"]
    }
}

def get_company_list():
    """Return summary list of all supported companies."""
    res = []
    for cid, data in COMPANIES_DATA.items():
        res.append({
            "id": data["id"],
            "name": data["name"],
            "logo_icon": data["logo_icon"],
            "category": data["category"],
            "roles": data["roles"]
        })
    return res

def get_company_details(company_id):
    """Retrieve full company guide."""
    return COMPANIES_DATA.get(company_id.lower())
