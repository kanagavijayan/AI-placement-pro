# Original educational question banks for AI PLACEMENT PRO Mock Tests

MOCK_TEST_BANKS = {
    "aptitude": [
        {
            "id": "apt_1",
            "category": "Quantitative Aptitude",
            "topic": "Time and Work",
            "question": "Worker P can finish a task in 15 days, while Worker Q can finish the same task in 20 days. If they work together for 4 days, what fraction of the task remains unfinished?",
            "options": [
                "7 / 15",
                "8 / 15",
                "11 / 15",
                "1 / 3"
            ],
            "correct_index": 1,
            "explanation": "P's 1-day work = 1/15, Q's 1-day work = 1/20. Combined 1-day work = 1/15 + 1/20 = 7/60. In 4 days, work completed = 4 * (7/60) = 7/15. Fraction remaining = 1 - 7/15 = 8/15."
        },
        {
            "id": "apt_2",
            "category": "Quantitative Aptitude",
            "topic": "Speed and Distance",
            "question": "A vehicle covers a distance of 360 km in 6 hours. If its speed is increased by 15 km/h, how much time will it take to cover a distance of 450 km?",
            "options": [
                "5 hours",
                "6 hours",
                "6.5 hours",
                "5.5 hours"
            ],
            "correct_index": 1,
            "explanation": "Initial speed = 360 / 6 = 60 km/h. New speed = 60 + 15 = 75 km/h. Time taken for 450 km = 450 / 75 = 6 hours."
        },
        {
            "id": "apt_3",
            "category": "Quantitative Aptitude",
            "topic": "Percentages & Profit",
            "question": "A merchant marks an item 25% above the cost price and then offers a discount of 10% on the marked price. What is the merchant's net profit percentage?",
            "options": [
                "12.5%",
                "15.0%",
                "11.5%",
                "13.5%"
            ],
            "correct_index": 0,
            "explanation": "Let Cost Price = 100. Marked Price = 125. Selling Price after 10% discount = 125 - 12.5 = 112.5. Profit = 112.5 - 100 = 12.5%."
        },
        {
            "id": "apt_4",
            "category": "Logical Reasoning",
            "topic": "Blood Relations",
            "question": "Pointing to a photograph, Rohit says, 'She is the daughter of the only son of my grandfather.' How is the girl in the photograph related to Rohit?",
            "options": [
                "Niece",
                "Sister",
                "Cousin",
                "Aunt"
            ],
            "correct_index": 1,
            "explanation": "Rohit's grandfather's only son is Rohit's father. The daughter of Rohit's father is Rohit's sister."
        },
        {
            "id": "apt_5",
            "category": "Logical Reasoning",
            "topic": "Number Series",
            "question": "Find the missing number in the sequence: 4, 9, 19, 39, 79, ?",
            "options": [
                "149",
                "159",
                "169",
                "139"
            ],
            "correct_index": 1,
            "explanation": "Pattern: multiply by 2 and add 1. (4*2)+1=9; (9*2)+1=19; (19*2)+1=39; (39*2)+1=79; (79*2)+1=159."
        },
        {
            "id": "apt_6",
            "category": "Verbal Ability",
            "topic": "Sentence Correction",
            "question": "Identify the grammatically correct sentence:",
            "options": [
                "Neither the manager nor the employees was aware of the policy update.",
                "Neither the manager nor the employees were aware of the policy update.",
                "Neither the manager nor the employees has been aware of the policy update.",
                "Neither the manager or the employees was aware of the policy update."
            ],
            "correct_index": 1,
            "explanation": "In 'neither... nor' constructions, the verb agrees with the closer subject ('the employees', plural), requiring the plural verb 'were'."
        },
        {
            "id": "apt_7",
            "category": "Quantitative Aptitude",
            "topic": "Probability",
            "question": "Two fair dice are thrown simultaneously. What is the probability that the sum of the numbers appearing on top is 8?",
            "options": [
                "5 / 36",
                "1 / 6",
                "7 / 36",
                "1 / 9"
            ],
            "correct_index": 0,
            "explanation": "Total possible outcomes = 6 * 6 = 36. Favorable outcomes resulting in sum 8: (2,6), (3,5), (4,4), (5,3), (6,2) -> 5 outcomes. Probability = 5/36."
        },
        {
            "id": "apt_8",
            "category": "Logical Reasoning",
            "topic": "Coding Decoding",
            "question": "If in a certain code language, 'GLOBAL' is written as 'HMPCBN', how is 'SERVER' written in that code?",
            "options": [
                "TFSWFS",
                "TFUXFS",
                "TFRWFS",
                "SFVXFS"
            ],
            "correct_index": 0,
            "explanation": "Each letter is shifted forward by 1 (+1): G->H, L->M, O->P, B->C, A->B, L->N. For SERVER: S->T, E->F, R->S, V->W, E->F, R->S = TFSWFS."
        }
    ],

    "technical": [
        {
            "id": "tech_1",
            "category": "Operating Systems",
            "topic": "Deadlocks",
            "question": "Which of the following is NOT one of the four necessary conditions for a deadlock to occur in an operating system?",
            "options": [
                "Mutual Exclusion",
                "Hold and Wait",
                "Preemptive Scheduling",
                "Circular Wait"
            ],
            "correct_index": 2,
            "explanation": "The four Coffman conditions are Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. Preemptive scheduling actually helps prevent deadlocks."
        },
        {
            "id": "tech_2",
            "category": "DBMS",
            "topic": "Transactions & ACID",
            "question": "Which component of the ACID properties guarantees that concurrent transactions execute as if they were executed sequentially without interference?",
            "options": [
                "Atomicity",
                "Consistency",
                "Isolation",
                "Durability"
            ],
            "correct_index": 2,
            "explanation": "Isolation ensures that concurrent transactions do not see uncommitted intermediate states of other transactions."
        },
        {
            "id": "tech_3",
            "category": "Computer Networks",
            "topic": "OSI & Protocols",
            "question": "At which layer of the OSI model does the Transport Layer Security (TLS/SSL) protocol primarily operate to establish encrypted transport sessions?",
            "options": [
                "Network Layer",
                "Data Link Layer",
                "Transport / Session Interface Layer",
                "Physical Layer"
            ],
            "correct_index": 2,
            "explanation": "TLS operates between the Transport layer (TCP) and the Application layer (HTTP), managing session establishment, handshakes, and encryption."
        },
        {
            "id": "tech_4",
            "category": "Data Structures",
            "topic": "Tree & Heap",
            "question": "What is the worst-case time complexity of searching for an element in an unbalanced Binary Search Tree (BST) with N nodes?",
            "options": [
                "O(1)",
                "O(log N)",
                "O(N)",
                "O(N log N)"
            ],
            "correct_index": 2,
            "explanation": "In an unbalanced BST that degenerates into a skewed line (like a linked list), searching requires visiting all N nodes, resulting in O(N) worst-case time."
        },
        {
            "id": "tech_5",
            "category": "Object-Oriented Programming",
            "topic": "Polymorphism",
            "question": "In Java/C++, which mechanism enables runtime (dynamic) method polymorphism?",
            "options": [
                "Method Overloading",
                "Virtual Function / Method Overriding",
                "Inline Functions",
                "Static Binding"
            ],
            "correct_index": 1,
            "explanation": "Runtime polymorphism is achieved via method overriding (using virtual tables / dynamic dispatch), allowing a subclass to provide a specific implementation of a method defined in its superclass."
        },
        {
            "id": "tech_6",
            "category": "Operating Systems",
            "topic": "Memory Management",
            "question": "What is 'Thrashing' in virtual memory systems?",
            "options": [
                "A state where the CPU executes instructions at peak frequency.",
                "A phenomenon where the system spends significantly more time swapping pages than executing instructions.",
                "Corrupting memory blocks due to power surges.",
                "Fast caching of repeatedly accessed memory pages."
            ],
            "correct_index": 1,
            "explanation": "Thrashing occurs when the active working sets of processes exceed physical RAM, causing constant page faults and disk swapping, collapsing CPU utilization."
        },
        {
            "id": "tech_7",
            "category": "DBMS",
            "topic": "Normalization",
            "question": "A relational table is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency X -> Y:",
            "options": [
                "Y is a prime attribute.",
                "X is a super key.",
                "X contains no null values.",
                "Y is functionally dependent on the entire primary key."
            ],
            "correct_index": 1,
            "explanation": "BCNF requires that for every functional dependency X -> Y, the determinant X must be a super key of the table."
        },
        {
            "id": "tech_8",
            "category": "Computer Networks",
            "topic": "TCP / IP",
            "question": "What flags are exchanged between a client and a server during the standard TCP 3-way connection handshake?",
            "options": [
                "SYN -> SYN-ACK -> ACK",
                "ACK -> SYN -> FIN",
                "RST -> ACK -> SYN",
                "SYN -> ACK -> FIN"
            ],
            "correct_index": 0,
            "explanation": "TCP 3-way handshake sequence: Client sends SYN, Server responds with SYN-ACK, and Client completes connection with ACK."
        }
    ],

    "coding_quiz": [
        {
            "id": "cq_1",
            "category": "Algorithms",
            "topic": "Sorting & Searching",
            "question": "What is the optimal average-case time complexity of QuickSort on an array of size N?",
            "options": [
                "O(N)",
                "O(N log N)",
                "O(N^2)",
                "O(log N)"
            ],
            "correct_index": 1,
            "explanation": "QuickSort divides the array around a pivot and recurses on both halves, giving an average time complexity of O(N log N)."
        },
        {
            "id": "cq_2",
            "category": "Data Structures",
            "topic": "Hash Maps",
            "question": "What is the amortized average time complexity of inserting and retrieving a key in a well-distributed Hash Table?",
            "options": [
                "O(1)",
                "O(log N)",
                "O(N)",
                "O(N^2)"
            ],
            "correct_index": 0,
            "explanation": "With a good hash function and low load factor, hash table insertions and lookups operate in O(1) average time."
        },
        {
            "id": "cq_3",
            "category": "Algorithms",
            "topic": "Graph Algorithms",
            "question": "Dijkstra's Single Source Shortest Path algorithm works correctly on graphs containing:",
            "options": [
                "Negative weight cycles only",
                "Arbitrary negative edge weights without cycles",
                "Non-negative edge weights only",
                "Undirected graphs with negative cycles"
            ],
            "correct_index": 2,
            "explanation": "Dijkstra's greedy approach assumes edge weights are non-negative. For graphs with negative weights, the Bellman-Ford algorithm should be used."
        },
        {
            "id": "cq_4",
            "category": "Complexity Theory",
            "topic": "Space-Time Tradeoffs",
            "question": "Which traversal algorithm on a tree visits all nodes level by level using a Queue data structure?",
            "options": [
                "Depth First Search (Preorder)",
                "Breadth First Search (Level Order)",
                "Inorder Traversal",
                "Postorder Traversal"
            ],
            "correct_index": 1,
            "explanation": "Breadth First Search (BFS) uses a FIFO Queue to process nodes level by level in order of distance from the root."
        }
    ],

    "tcs": [
        {
            "id": "tcs_1",
            "category": "TCS NQT Numerical",
            "topic": "Work and Rates",
            "question": "A team of 12 engineers can finish an IT deployment in 16 days working 8 hours a day. How many days will 16 engineers take to finish twice the deployment working 6 hours a day?",
            "options": [
                "24 days",
                "32 days",
                "28 days",
                "36 days"
            ],
            "correct_index": 1,
            "explanation": "Using M1*D1*H1 / W1 = M2*D2*H2 / W2: (12 * 16 * 8) / 1 = (16 * D2 * 6) / 2. 1536 = 48 * D2 -> D2 = 1536 / 48 = 32 days."
        },
        {
            "id": "tcs_2",
            "category": "TCS Reasoning",
            "topic": "Logical Statements",
            "question": "Statements: (1) All microservices are containers. (2) Some containers are scalable. Conclusions: (I) Some microservices are scalable. (II) Some scalable entities are containers.",
            "options": [
                "Only Conclusion I follows",
                "Only Conclusion II follows",
                "Both I and II follow",
                "Neither follows"
            ],
            "correct_index": 1,
            "explanation": "From 'Some containers are scalable', by conversion, 'Some scalable entities are containers' necessarily follows (Conclusion II). Conclusion I cannot be asserted with certainty."
        },
        {
            "id": "tcs_3",
            "category": "TCS Technical Coding",
            "topic": "Bit Manipulation",
            "question": "What is the result of evaluating the bitwise expression: (18 ^ 18) | (25 & 1) in C/Python?",
            "options": [
                "0",
                "1",
                "25",
                "19"
            ],
            "correct_index": 1,
            "explanation": "18 ^ 18 = 0 (XOR of identical numbers is 0). 25 & 1 = 1 (checks if odd, 25 is odd). 0 | 1 = 1."
        }
    ],

    "infosys": [
        {
            "id": "inf_1",
            "category": "Infosys Pseudocode",
            "topic": "Recursion Tracing",
            "question": "Consider the pseudocode function: Integer solve(Integer n) { if(n <= 1) return 1; return n * solve(n - 2); }. What is the return value for solve(7)?",
            "options": [
                "105",
                "48",
                "5040",
                "120"
            ],
            "correct_index": 0,
            "explanation": "solve(7) = 7 * solve(5) = 7 * (5 * solve(3)) = 7 * 5 * (3 * solve(1)) = 7 * 5 * 3 * 1 = 105."
        },
        {
            "id": "inf_2",
            "category": "Infosys Critical Thinking",
            "topic": "Cryptarithmetic / Modular",
            "question": "What is the remainder when 3^45 is divided by 8?",
            "options": [
                "1",
                "3",
                "5",
                "7"
            ],
            "correct_index": 1,
            "explanation": "3^2 = 9 = 1 mod 8. Hence 3^45 = (3^2)^22 * 3^1 = (1)^22 * 3 = 3 mod 8. Remainder is 3."
        }
    ],

    "amazon": [
        {
            "id": "amz_1",
            "category": "Amazon SDE Technical",
            "topic": "System & Algorithmic Design",
            "question": "In a distributed streaming architecture, which data structure is most effective for finding the median of a continuous stream of incoming real-time integers in O(log N) per insertion?",
            "options": [
                "Single Red-Black Tree",
                "Two Heaps (Max-Heap for lower half, Min-Heap for upper half)",
                "Segment Tree",
                "Circular Queue"
            ],
            "correct_index": 1,
            "explanation": "The two-heap technique (Max-Heap for lower half and Min-Heap for upper half) maintains median access in O(1) time and accepts new insertions in O(log N) time."
        },
        {
            "id": "amz_2",
            "category": "Amazon SDE DSA",
            "topic": "Monotonic Stack",
            "question": "Which data structure pattern yields an optimal O(N) solution for the 'Next Greater Element' problem across an array of length N?",
            "options": [
                "Monotonic Stack",
                "Breadth First Search Queue",
                "Trie Data Structure",
                "Min Priority Queue"
            ],
            "correct_index": 0,
            "explanation": "A monotonic decreasing stack processes each element at most twice (one push, one pop), solving Next Greater Element in linear O(N) time."
        }
    ]
}

def get_test_questions(test_type="aptitude", count=5):
    """Retrieve curated test questions for a mock examination."""
    bank = MOCK_TEST_BANKS.get(test_type, MOCK_TEST_BANKS["aptitude"])
    import random
    questions = bank.copy()
    random.shuffle(questions)
    return questions[:min(count, len(questions))]

def evaluate_test_submission(test_type, answers_dict):
    """
    answers_dict: { 'apt_1': 1, 'apt_2': 0, ... }
    returns: score, total, correct, details
    """
    bank = MOCK_TEST_BANKS.get(test_type, MOCK_TEST_BANKS["aptitude"])
    bank_map = {q["id"]: q for q in bank}

    total = len(answers_dict)
    correct = 0
    details = []

    for qid, user_choice in answers_dict.items():
        q_item = bank_map.get(qid)
        if not q_item:
            continue
        is_correct = (user_choice == q_item["correct_index"])
        if is_correct:
            correct += 1
        details.append({
            "id": qid,
            "question": q_item["question"],
            "options": q_item["options"],
            "user_choice": user_choice,
            "correct_index": q_item["correct_index"],
            "is_correct": is_correct,
            "explanation": q_item["explanation"]
        })

    score_pct = round((correct / max(1, total)) * 100, 1)
    return {
        "score_pct": score_pct,
        "correct": correct,
        "total": total,
        "details": details
    }
