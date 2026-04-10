"""
modules/knowledge_base.py
Central knowledge store for EduBridge.

Syllabus concepts used:
  - Dictionaries        : topic_bank is a dict of dicts
  - Lists               : keywords, steps, and examples stored as lists
  - Strings             : all content is string data
  - Tuples              : flashcard data stored as list of tuples
"""

# ─────────────────────────────────────────────────────────────
# TOPIC BANK
# Structure: { topic_key: { keywords, title, steps, example, tip } }
# ─────────────────────────────────────────────────────────────

TOPIC_BANK = {
    "variables": {
        "keywords": ["variable", "assign", "store", "value", "int", "float", "data type", "declare"],
        "title": "Variables & Data Types",
        "steps": [
            "A variable is a named container that stores a value in memory.",
            "Python has 4 basic data types: int (whole numbers), float (decimals), str (text), bool (True/False).",
            "You do NOT need to declare the type — Python detects it automatically.",
            "Use = to assign a value to a variable name.",
        ],
        "example": 'age = 18          # int\nheight = 5.9      # float\nname = "Arjun"    # str\nis_student = True  # bool\n\nprint(type(age))   # <class \'int\'>',
        "tip": "Variable names are case-sensitive! 'age' and 'Age' are two different variables."
    },

    "if_else": {
        "keywords": ["if", "else", "elif", "condition", "branching", "conditional", "decision"],
        "title": "Branching — If / Elif / Else",
        "steps": [
            "Branching lets your program make decisions based on conditions.",
            "Use 'if' for the first condition.",
            "Use 'elif' (else-if) for additional conditions.",
            "Use 'else' as the default when no conditions match.",
            "Conditions must evaluate to True or False.",
        ],
        "example": 'marks = 85\n\nif marks >= 90:\n    print("Grade: A+")\nelif marks >= 75:\n    print("Grade: A")\nelif marks >= 60:\n    print("Grade: B")\nelse:\n    print("Grade: C")',
        "tip": "Python uses indentation (4 spaces) instead of {} braces. Always indent your if/else blocks!"
    },

    "for_loop": {
        "keywords": ["for loop", "for", "loop", "iterate", "iteration", "range", "repeat"],
        "title": "For Loop",
        "steps": [
            "A for loop repeats a block of code for each item in a sequence.",
            "Use 'for item in sequence:' syntax.",
            "range(n) generates numbers from 0 to n-1.",
            "range(start, stop, step) gives more control.",
            "You can loop over lists, strings, dictionaries, and more.",
        ],
        "example": '# Loop over a list\nfruits = ["apple", "mango", "banana"]\nfor fruit in fruits:\n    print(fruit)\n\n# Loop with range\nfor i in range(1, 6):\n    print(f"Count: {i}")\n\n# Loop over a string\nfor char in "Python":\n    print(char)',
        "tip": "Use 'enumerate(list)' to get both the index and value: for i, val in enumerate(my_list)"
    },

    "while_loop": {
        "keywords": ["while", "while loop", "infinite", "break", "continue", "pass", "exit"],
        "title": "While Loop + Break/Continue/Pass",
        "steps": [
            "A while loop runs as long as its condition is True.",
            "Always update the loop variable inside the loop, or you'll get an infinite loop.",
            "'break' immediately exits the loop.",
            "'continue' skips the current iteration and moves to the next.",
            "'pass' is a placeholder that does nothing — useful for empty blocks.",
        ],
        "example": 'count = 0\nwhile count < 5:\n    if count == 3:\n        count += 1\n        continue   # skip 3\n    print(count)\n    count += 1\n\n# break example\nfor i in range(10):\n    if i == 5:\n        break     # stop at 5\n    print(i)',
        "tip": "If your program freezes, you probably have an infinite while loop! Press Ctrl+C to stop it."
    },

    "functions": {
        "keywords": ["function", "def", "return", "parameter", "argument", "lambda", "anonymous", "positional", "keyword", "default"],
        "title": "Functions",
        "steps": [
            "A function is a reusable block of code — define once, use many times.",
            "Use 'def function_name(parameters):' to define.",
            "Parameters are inputs; return sends a result back.",
            "Default arguments have a fallback value if none is given.",
            "Lambda creates a small one-line anonymous function.",
        ],
        "example": 'def greet(name, msg="Hello"):   # default argument\n    return f"{msg}, {name}!"\n\nprint(greet("Arjun"))          # Hello, Arjun!\nprint(greet("Priya", "Hi"))    # Hi, Priya!\n\n# Global and local variables\nx = 10  # global\ndef show():\n    y = 5  # local — only exists here\n    print(x, y)\n\n# Lambda (anonymous function)\nsquare = lambda n: n ** 2\nprint(square(7))  # 49',
        "tip": "Functions should do ONE thing well. If a function is more than 20 lines, split it up!"
    },

    "recursion": {
        "keywords": ["recursion", "recursive", "base case", "factorial", "fibonacci", "divide conquer", "call itself"],
        "title": "Recursion",
        "steps": [
            "Recursion is when a function calls ITSELF to solve a smaller version of the problem.",
            "Every recursive function MUST have a base case — the condition that stops the recursion.",
            "Without a base case, you'll get RecursionError (Python stops after ~1000 calls).",
            "Think of recursion like Russian dolls — each doll opens to reveal a smaller one.",
        ],
        "example": 'def factorial(n):\n    # Base case: stop here\n    if n == 0:\n        return 1\n    # Recursive case: call itself with smaller n\n    return n * factorial(n - 1)\n\nprint(factorial(5))\n# 5 * factorial(4)\n# 5 * 4 * factorial(3)\n# 5 * 4 * 3 * 2 * 1 = 120',
        "tip": "Always write the base case FIRST before the recursive case. It's the most important part!"
    },

    "strings": {
        "keywords": ["string", "str", "upper", "lower", "split", "join", "strip", "slice", "find", "replace", "format", "f-string"],
        "title": "Strings & String Methods",
        "steps": [
            "Strings are sequences of characters enclosed in ' ' or \" \".",
            "Strings are IMMUTABLE — you can't change them in place, only create new ones.",
            "String indexing starts at 0. Negative indexes count from the end (-1 = last).",
            "Slicing: string[start:end:step] extracts a portion.",
            "Common methods: upper(), lower(), strip(), split(), join(), find(), replace().",
        ],
        "example": 'name = "  EduBridge  "\nprint(name.strip())          # "EduBridge"\nprint(name.strip().upper())  # "EDUBRIDGE"\nprint(name.strip().lower())  # "edubridge"\n\nsentence = "Python is great"\nwords = sentence.split(" ")  # [\'Python\', \'is\', \'great\']\nprint("-".join(words))       # Python-is-great\nprint(sentence[0:6])         # Python\nprint(sentence[::-1])        # taerg si nohtyP',
        "tip": "Use f-strings for formatting: f'Hello {name}, you scored {score}%' — much cleaner than + concatenation!"
    },

    "lists": {
        "keywords": ["list", "append", "insert", "remove", "pop", "index", "sort", "reverse", "len"],
        "title": "Lists",
        "steps": [
            "A list is an ordered, mutable (changeable) collection of items.",
            "Lists use square brackets [] and can hold any data type.",
            "Indexing starts at 0. Negative indexing: list[-1] is the last item.",
            "Common methods: append(), insert(), remove(), pop(), sort(), reverse(), len().",
            "List slicing works the same as string slicing: list[start:end:step].",
        ],
        "example": 'marks = [85, 92, 78, 95, 88]\n\nmarks.append(91)       # add to end → [..., 91]\nmarks.insert(0, 100)   # add at index 0\nmarks.remove(78)       # remove first occurrence of 78\nmarks.sort()           # sort in place\n\nprint(marks[0])        # first item\nprint(marks[-1])       # last item\nprint(marks[1:4])      # slicing\nprint(len(marks))      # number of items\nprint(max(marks))      # highest value',
        "tip": "Remember: list.sort() changes the list IN PLACE. sorted(list) returns a NEW sorted list."
    },

    "tuples": {
        "keywords": ["tuple", "immutable", "packing", "unpacking", "parentheses"],
        "title": "Tuples",
        "steps": [
            "A tuple is like a list but IMMUTABLE — you cannot change it after creation.",
            "Tuples use parentheses () instead of square brackets [].",
            "Use tuples for data that should NOT change (e.g. coordinates, RGB colors).",
            "Tuple packing: grouping values. Tuple unpacking: extracting them.",
            "Tuples are faster than lists and signal 'this data is fixed'.",
        ],
        "example": 'coordinates = (10, 20)   # tuple\ncolors = ("red", "green", "blue")\n\n# Unpacking\nx, y = coordinates\nprint(x)   # 10\nprint(y)   # 20\n\n# Tuples in a list (common pattern)\nstudents = [(\"Arjun\", 95), (\"Priya\", 89), (\"Rohit\", 72)]\nfor name, score in students:\n    print(f"{name}: {score}")',
        "tip": "If your data is constant (like days of week), use a tuple. If it will change, use a list."
    },

    "sets": {
        "keywords": ["set", "unique", "union", "intersection", "difference", "add", "discard", "in"],
        "title": "Sets",
        "steps": [
            "A set is an unordered collection of UNIQUE elements — no duplicates allowed.",
            "Sets use curly braces {} (but empty set must be set(), not {}).",
            "Union (|): all elements from both sets.",
            "Intersection (&): only elements present in BOTH sets.",
            "Difference (-): elements in one set but not the other.",
        ],
        "example": 'nums = {1, 2, 2, 3, 3, 3}\nprint(nums)     # {1, 2, 3} — duplicates removed!\n\na = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\n\nprint(a | b)    # Union → {1,2,3,4,5,6}\nprint(a & b)    # Intersection → {3,4}\nprint(a - b)    # Difference → {1,2}\n\n# Membership check (very fast for sets)\nprint(3 in a)   # True',
        "tip": "Sets are PERFECT for removing duplicates from a list: unique = list(set(my_list))"
    },

    "dictionaries": {
        "keywords": ["dictionary", "dict", "key", "value", "key-value", "keys", "values", "items", "get", "update"],
        "title": "Dictionaries",
        "steps": [
            "A dictionary stores data as key-value pairs — like a real dictionary.",
            "Keys must be UNIQUE and IMMUTABLE (strings, numbers, or tuples).",
            "Access values using dict[key] or dict.get(key) (safer — no error if missing).",
            "Useful methods: keys(), values(), items(), get(), update(), pop().",
            "Dictionaries preserve insertion order (Python 3.7+).",
        ],
        "example": 'student = {\n    "name": "Arjun",\n    "age": 18,\n    "marks": 95\n}\n\nprint(student["name"])          # Arjun\nprint(student.get("grade", "N/A"))  # N/A (safe)\n\nstudent["grade"] = "A"          # add new key\nstudent.update({"age": 19})     # update existing\n\nfor key, value in student.items():\n    print(f"{key}: {value}")',
        "tip": "Always use .get(key, default) instead of [key] when the key might not exist — it won't crash!"
    },

    "exceptions": {
        "keywords": ["exception", "try", "except", "finally", "raise", "error", "value error", "custom", "user defined"],
        "title": "Exception Handling",
        "steps": [
            "Exceptions are errors that occur during program execution.",
            "'try' block contains code that might fail.",
            "'except' block catches the error and handles it gracefully.",
            "'finally' block ALWAYS runs, even if an error occurred — use it for cleanup.",
            "'raise' lets you throw your own exceptions. Create custom ones by subclassing Exception.",
        ],
        "example": 'class AgeError(Exception):      # Custom exception\n    pass\n\ndef check_age(age):\n    try:\n        if not isinstance(age, int):\n            raise ValueError("Age must be a number!")\n        if age < 0:\n            raise AgeError("Age cannot be negative!")\n        print(f"Valid age: {age}")\n    except ValueError as e:\n        print(f"ValueError: {e}")\n    except AgeError as e:\n        print(f"AgeError: {e}")\n    finally:\n        print("Check complete.")  # always runs\n\ncheck_age(-5)',
        "tip": "Catch specific exceptions (ValueError, TypeError) — never use bare 'except:' as it hides bugs!"
    },

    "file_io": {
        "keywords": ["file", "open", "read", "write", "close", "with", "append", "readline", "readlines"],
        "title": "File Handling (I/O)",
        "steps": [
            "File I/O lets your program permanently save and load data.",
            "Always use 'with open(...)' — it automatically closes the file even if an error occurs.",
            "Modes: 'r' = read, 'w' = write (overwrites!), 'a' = append, 'x' = create new.",
            "read() reads the whole file. readlines() reads all lines as a list.",
            "write() writes a string. writelines() writes a list of strings.",
        ],
        "example": '# Write to file\nwith open("scores.txt", "w") as f:\n    f.write("Arjun: 95\\n")\n    f.write("Priya: 89\\n")\n\n# Read from file\nwith open("scores.txt", "r") as f:\n    for line in f:\n        print(line.strip())\n\n# Append without overwriting\nwith open("scores.txt", "a") as f:\n    f.write("Rohit: 78\\n")',
        "tip": "Use 'a' mode to ADD to a file. Using 'w' will ERASE everything in the file first!"
    },

    "modules": {
        "keywords": ["module", "import", "from import", "package", "numpy", "pygame", "pip", "install"],
        "title": "Modules & Packages",
        "steps": [
            "A module is a Python file you can import to reuse code.",
            "Python has built-in modules: math, os, random, json, datetime.",
            "External packages (numpy, pygame) are installed via pip.",
            "'import module' imports the whole module.",
            "'from module import function' imports only what you need.",
        ],
        "example": 'import math\nprint(math.sqrt(25))   # 5.0\nprint(math.pi)         # 3.14159...\n\nfrom random import randint, choice\nprint(randint(1, 10))  # random 1-10\nprint(choice(["a","b","c"]))  # random pick\n\nimport os\nprint(os.getcwd())     # current directory\n\n# Your own module: save as mymodule.py\n# def greet(name): return f"Hi {name}"\n# Then in another file: import mymodule',
        "tip": "Use 'import as' to give modules a shorter name: import numpy as np, import pandas as pd"
    },

    "photosynthesis": {
        "keywords": ["photosynthesis", "plant", "chlorophyll", "sunlight", "glucose", "carbon dioxide", "oxygen", "chloroplast"],
        "title": "Photosynthesis",
        "steps": [
            "Photosynthesis is how plants make their own food using sunlight.",
            "It occurs inside chloroplasts, which contain the green pigment chlorophyll.",
            "Inputs: Carbon dioxide (CO₂) from air + Water (H₂O) from soil + Sunlight (energy).",
            "Outputs: Glucose (C₆H₁₂O₆) as food + Oxygen (O₂) released into air.",
            "This is why plants are called 'producers' — they produce food from scratch.",
        ],
        "example": "Equation:\n6CO₂ + 6H₂O + Sunlight → C₆H₁₂O₆ + 6O₂\n\nWhere it happens: Chloroplasts (in leaf cells)\n\nLight Reaction: Occurs in thylakoid membrane\n                Uses light to split water\n\nDark Reaction:  Occurs in stroma\n                Uses CO₂ to make glucose",
        "tip": "Memory trick: CO₂ IN, O₂ OUT. Plants breathe in what we breathe out — a perfect partnership!"
    },

    "newton_laws": {
        "keywords": ["newton", "law", "motion", "force", "inertia", "acceleration", "action", "reaction", "f=ma", "mass"],
        "title": "Newton's Laws of Motion",
        "steps": [
            "Newton's 3 laws describe how objects move and respond to forces.",
            "1st Law (Inertia): Objects stay at rest or in motion unless a force acts on them.",
            "2nd Law (F=ma): Force = Mass × Acceleration. More mass = more force needed.",
            "3rd Law (Action-Reaction): Every action has an equal and opposite reaction.",
        ],
        "example": "1st Law: A book on a table stays still until you push it.\n          A rolling ball keeps rolling until friction stops it.\n\n2nd Law: F = m × a\n          If mass = 10 kg, acceleration = 2 m/s²\n          Then Force = 20 Newtons\n\n3rd Law: When you jump, you push Earth down.\n          Earth pushes you up with equal force.\n          Rockets: gas pushed DOWN → rocket goes UP.",
        "tip": "F=ma is the most important formula in mechanics. Double the mass → need double the force for same acceleration."
    },
}


# ─────────────────────────────────────────────────────────────
# FLASHCARD DATA
# Stored as a list of tuples: (tag, question, answer, example)
# Syllabus concept: List of tuples, tuple unpacking
# ─────────────────────────────────────────────────────────────

FLASHCARDS = [
    ("Python", "What is a variable?",
     "A named container that stores data in memory.",
     "age = 18\nname = 'Arjun'\npi = 3.14"),

    ("Python", "Difference between list and tuple?",
     "Lists are mutable (can change). Tuples are immutable (fixed).",
     "my_list = [1,2,3]  # can modify\nmy_tuple = (1,2,3) # cannot modify"),

    ("Python", "What does a recursive function always need?",
     "A BASE CASE — the stopping condition that ends the recursion.",
     "def fact(n):\n  if n==0: return 1  # base case\n  return n * fact(n-1)"),

    ("Python", "What does set() do with duplicates?",
     "Removes all duplicates automatically — only unique values remain.",
     "nums = {1,2,2,3,3,3}\nprint(nums)  # {1,2,3}"),

    ("Python", "What is a lambda function?",
     "An anonymous (nameless) one-line function using the lambda keyword.",
     "double = lambda x: x * 2\nprint(double(5))  # 10"),

    ("Python", "What does 'with open()' do automatically?",
     "Automatically closes the file after the block, even if an error occurs.",
     "with open('data.txt','r') as f:\n    content = f.read()\n# file is closed here"),

    ("Python", "Difference between break, continue, pass?",
     "break exits the loop. continue skips current iteration. pass is a placeholder.",
     "for i in range(5):\n  if i==2: continue  # skip 2\n  if i==4: break     # stop at 4\n  print(i)  # 0, 1, 3"),

    ("Python", "What is 'finally' in exception handling?",
     "A block that ALWAYS runs after try/except — used for cleanup code.",
     "try:\n  x = int(input())\nexcept ValueError:\n  print('Not a number')\nfinally:\n  print('Always runs!')"),

    ("Python", "What does list slicing [1:4] do?",
     "Returns items at index 1, 2, 3 (end index is EXCLUSIVE).",
     "nums = [10,20,30,40,50]\nprint(nums[1:4])  # [20,30,40]"),

    ("Python", "What is the difference between = and ==?",
     "= is assignment (store a value). == is comparison (check if equal).",
     "x = 5        # assigns 5 to x\nif x == 5:   # checks if x equals 5\n    print('yes')"),

    ("Science", "What are the inputs of photosynthesis?",
     "CO₂ (carbon dioxide), H₂O (water), and Sunlight.",
     "6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂"),

    ("Science", "Newton's 2nd Law formula?",
     "F = m × a (Force = Mass × Acceleration)",
     "mass = 10 kg, acceleration = 3 m/s²\nForce = 10 × 3 = 30 Newtons"),

    ("Maths", "What is 5! (5 factorial)?",
     "120 — product of all integers from 1 to 5.",
     "5! = 5×4×3×2×1 = 120\n0! = 1 (by definition)"),

    ("Maths", "What is set intersection (A ∩ B)?",
     "Elements that exist in BOTH sets at the same time.",
     "A = {1,2,3,4}\nB = {3,4,5,6}\nA∩B = {3,4}"),
]


# ─────────────────────────────────────────────────────────────
# QUIZ QUESTIONS
# Stored as: list of dicts, each with q, options, answer index, explanation
# ─────────────────────────────────────────────────────────────

QUIZ_BANK = {
    "Python": [
        {"q": "What does a recursive function always need to prevent infinite recursion?",
         "options": ["A loop", "A base case", "A return type", "A class"],
         "answer": 1,
         "explanation": "A base case is the stopping condition. Without it, the function calls itself forever and Python raises RecursionError."},
        {"q": "Which data structure stores key-value pairs?",
         "options": ["List", "Tuple", "Set", "Dictionary"],
         "answer": 3,
         "explanation": "Dictionaries store data as key:value pairs using {}. Keys must be unique and immutable."},
        {"q": "What will print(set([1,2,2,3,3,3])) output?",
         "options": ["{1,2,2,3,3,3}", "{1,2,3}", "[1,2,3]", "Error"],
         "answer": 1,
         "explanation": "Sets automatically remove duplicates. [1,2,2,3,3,3] becomes {1,2,3}."},
        {"q": "Which keyword catches errors in Python?",
         "options": ["catch", "except", "error", "handle"],
         "answer": 1,
         "explanation": "Python uses try/except (not try/catch like Java). The except block handles errors gracefully."},
        {"q": "What does [10,20,30,40,50][1:4] return?",
         "options": ["[10,20,30]", "[20,30,40]", "[10,20,30,40]", "[20,30,40,50]"],
         "answer": 1,
         "explanation": "Slicing [1:4] gives indices 1, 2, 3 — NOT 4! Start is inclusive, end is exclusive."},
        {"q": "What does the 'finally' block always do?",
         "options": ["Runs only if no error", "Runs only on error", "Always runs, error or not", "Stops the program"],
         "answer": 2,
         "explanation": "finally ALWAYS executes whether an exception occurred or not. Perfect for cleanup like closing files!"},
        {"q": "Which is correct lambda syntax?",
         "options": ["lambda x => x*2", "def lambda x: x*2", "lambda x: x*2", "function(x): x*2"],
         "answer": 2,
         "explanation": "Lambda syntax: lambda parameters: expression. Short, anonymous, one-line functions."},
        {"q": "Which file mode appends WITHOUT overwriting existing content?",
         "options": ["'r'", "'w'", "'a'", "'x'"],
         "answer": 2,
         "explanation": "'a' mode appends to the file. 'w' erases everything first. Always use 'a' to add to existing files."},
    ],
    "Science": [
        {"q": "Which pigment in plants captures sunlight for photosynthesis?",
         "options": ["Melanin", "Chlorophyll", "Carotene", "Hemoglobin"],
         "answer": 1,
         "explanation": "Chlorophyll is the green pigment in chloroplasts that absorbs sunlight for photosynthesis."},
        {"q": "Newton's 2nd Law: Force equals?",
         "options": ["Mass / Acceleration", "Mass + Velocity", "Mass × Acceleration", "Velocity × Time"],
         "answer": 2,
         "explanation": "F = ma. Force equals mass times acceleration. Double the mass → need double the force for same acceleration."},
        {"q": "What gas do plants release during photosynthesis?",
         "options": ["Carbon dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
         "answer": 2,
         "explanation": "Plants take in CO₂ and release O₂ during photosynthesis — why forests are called Earth's lungs!"},
        {"q": "'Every action has equal and opposite reaction' is which law?",
         "options": ["Newton's 1st", "Newton's 2nd", "Newton's 3rd", "Hooke's Law"],
         "answer": 2,
         "explanation": "Newton's 3rd Law! When you jump, you push Earth down and Earth pushes you up with equal force."},
        {"q": "Where exactly does photosynthesis take place in a plant?",
         "options": ["Mitochondria", "Nucleus", "Chloroplasts", "Vacuole"],
         "answer": 2,
         "explanation": "Chloroplasts contain chlorophyll and are the site of photosynthesis, mainly found in leaves."},
        {"q": "An object at rest stays at rest unless acted on by a force. This is?",
         "options": ["2nd Law", "Law of Conservation", "1st Law (Inertia)", "Hooke's Law"],
         "answer": 2,
         "explanation": "Newton's 1st Law — the Law of Inertia! Objects resist changes to their state of motion."},
    ],
    "Maths": [
        {"q": "What is the value of 5! (5 factorial)?",
         "options": ["25", "120", "60", "720"],
         "answer": 1,
         "explanation": "5! = 5×4×3×2×1 = 120. Factorial grows very fast — recursion computes this beautifully!"},
        {"q": "If A={1,2,3} and B={2,3,4}, what is A∩B (intersection)?",
         "options": ["{1,2,3,4}", "{2,3}", "{1,4}", "{}"],
         "answer": 1,
         "explanation": "Intersection = elements in BOTH sets. 2 and 3 appear in both A and B, so A∩B = {2,3}."},
        {"q": "What is the slope of the line y = 3x + 5?",
         "options": ["5", "3", "8", "15"],
         "answer": 1,
         "explanation": "In y = mx + c, m is the slope and c is the y-intercept. Here slope m = 3."},
        {"q": "Pythagorean theorem: a² + b² = ?",
         "options": ["a + b", "c", "c²", "2c"],
         "answer": 2,
         "explanation": "a² + b² = c² where c is the hypotenuse (longest side) of a right-angled triangle."},
        {"q": "Sum of interior angles of any triangle?",
         "options": ["90°", "180°", "270°", "360°"],
         "answer": 1,
         "explanation": "The sum of interior angles in any triangle is always exactly 180°. A fundamental theorem!"},
        {"q": "Probability of getting heads on a fair coin toss?",
         "options": ["1", "0", "0.5", "0.25"],
         "answer": 2,
         "explanation": "P = favourable / total = 1/2 = 0.5. One head outcome out of two equally likely possibilities."},
    ],
    "History": [
        {"q": "Who was India's first Prime Minister?",
         "options": ["Mahatma Gandhi", "Sardar Patel", "Jawaharlal Nehru", "B.R. Ambedkar"],
         "answer": 2,
         "explanation": "Jawaharlal Nehru became India's first Prime Minister on August 15, 1947, serving until 1964."},
        {"q": "In which year did India gain independence?",
         "options": ["1945", "1947", "1950", "1942"],
         "answer": 1,
         "explanation": "India became independent on August 15, 1947. We became a Republic on January 26, 1950."},
        {"q": "The Indian Constitution came into effect on?",
         "options": ["Aug 15 1947", "Jan 26 1950", "Nov 26 1949", "Jan 26 1949"],
         "answer": 1,
         "explanation": "The Constitution was adopted on November 26, 1949 and came into effect on January 26, 1950 — Republic Day!"},
        {"q": "Who wrote the Indian National Anthem 'Jana Gana Mana'?",
         "options": ["Bankim Chandra", "Rabindranath Tagore", "Mahatma Gandhi", "Sarojini Naidu"],
         "answer": 1,
         "explanation": "Rabindranath Tagore wrote it. First sung at the Calcutta INC session in 1911."},
        {"q": "The Quit India Movement was launched in which year?",
         "options": ["1930", "1935", "1942", "1945"],
         "answer": 2,
         "explanation": "Gandhi launched Quit India on August 8, 1942, demanding an end to British colonial rule."},
    ],
}
