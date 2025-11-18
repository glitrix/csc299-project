# StudyPal Demo Script - Sample Commands for Video Demonstration

**Duration:** 6-8 minutes  
This script demonstrates all major features of StudyPal in a logical flow.

---

## PART 1: INTRODUCTION & SETUP (0:30)

```bash
# Start StudyPal
py -m src.studypal

# Show help to introduce commands
help
```

---

## PART 2: NOTE MANAGEMENT (1:30)

```bash
# Create first note with tags and content
add note "Python Basics" --tags python,programming --content "Variables: store data (x = 10). Functions: reusable code blocks. Loops: for and while for iteration."

# Create second note
add note "Object-Oriented Programming" --tags python,oop --content "Classes define objects. Objects have attributes and methods. Key concepts: encapsulation, inheritance, polymorphism."

# Create third note
add note "Data Structures" --tags python,algorithms --content "Lists: ordered, mutable. Tuples: ordered, immutable. Dictionaries: key-value pairs. Sets: unique elements."

# Create fourth note for later demos
add note "Algorithm Analysis" --tags algorithms,complexity --content "Time complexity: how execution time grows. Space complexity: memory usage. Big O notation: O(1), O(n), O(log n), O(n²)."

# List all notes
list notes

# Show detailed view of a note
show note 1

# List notes by tag
list notes --tag python

# Search for a note by keyword
search notes "loops"
```

---

## PART 3: LINKING NOTES (1:00)

```bash
# Use AI to suggest links between notes
suggest links 1

# Create a link between related notes
link note 1 to 2

# View the linked note
show note 1

# Suggest links for another note
suggest links 3

# Link data structures to algorithms
link note 3 to 4
```

---

## PART 4: TASK MANAGEMENT (1:30)

```bash
# Create tasks with different priorities and due dates
add task "Study Python loops" --due 2025-11-25 --priority 5 --desc "Focus on for loops and while loops with examples"

add task "Review OOP concepts" --due 2025-11-27 --priority 4 --desc "Review classes, objects, inheritance"

add task "Practice data structures" --due 2025-11-30 --priority 3 --desc "Implement list and dictionary exercises"

add task "Complete algorithm homework" --due 2025-11-22 --priority 5 --desc "Time complexity analysis problems"

add task "Read Chapter 5" --due 2025-12-01 --priority 2

# List all tasks
list tasks

# Show specific task details
show task 1

# Filter tasks by status
list tasks --status todo

# Filter by priority
list tasks --priority 5

# Update a task status
update task 1 --status in_progress

# Check task statistics
stats
```

---

## PART 5: AI-POWERED TAG SUGGESTIONS (0:30)

```bash
# Get AI tag suggestions for a note
suggest tags 1

# Get suggestions for another note
suggest tags 4

# Update note with suggested tags
update note 4 --tags algorithms,complexity,big-o
```

---

## PART 6: AI STUDY PLANNING (1:00)

```bash
# Generate AI-powered weekly study plan
plan week

# Get daily recommendations
plan today
```

---

## PART 7: AI SUMMARIES & EXPANSION (1:00)

```bash
# Generate AI summary of a note
summary 2

# Expand a note with AI (add more detail)
expand 1 --mode expand

# Show the expanded note
show note 1

# Clarify a complex note
expand 4 --mode clarify

# Add examples to a note
expand 3 --mode examples
```

---

## PART 8: AI QUIZ GENERATION (0:45)

```bash
# Generate quiz questions from a note
quiz 1 --num 5

# Generate quiz for algorithm note
quiz 4 --num 3
```

---

## PART 9: AI KNOWLEDGE ASSISTANT (0:45)

```bash
# Ask general questions about your study materials
ask "What topics should I focus on this week?"

# Ask specific questions
ask "How are lists and tuples different?"

# Ask about your progress
ask "What tasks are most urgent?"

# Clear conversation history
clear conversation
```

---

## PART 10: STUDY BUDDY CHAT MODE (1:30)

```bash
# Enter interactive chat mode
chat
```

**Example conversation** (type each message when prompted):

1. **Ask for explanation:**
   ```
   Can you explain what object-oriented programming is in simple terms?
   ```

2. **Follow-up question** (shows context memory):
   ```
   How does inheritance work?
   ```

3. **Request quiz:**
   ```
   Quiz me on Python basics
   ```

4. **Ask about study strategy:**
   ```
   I have an exam next week. How should I prepare based on my notes?
   ```

5. **Ask for summary:**
   ```
   Can you summarize what I've learned about data structures?
   ```

6. **Exit chat mode:**
   ```
   bye
   ```

---

## PART 11: UPDATING & ORGANIZING (0:30)

```bash
# Update note title and content
update note 1 --title "Python Fundamentals" --content "Variables store data. Functions are reusable blocks. Loops iterate: for (definite) and while (conditional). Control flow: if/elif/else."

# Update task with new due date
update task 3 --due 2025-11-28 --priority 4

# Mark task as complete
update task 4 --status done

# Check updated stats
stats

# List completed tasks
list tasks --status done
```

---

## PART 12: SEMANTIC SEARCH (0:30)

```bash
# Use AI semantic search (understands meaning, not just keywords)
search notes "what did I learn about iteration?"

search notes "explain object concepts"

search notes "how to analyze performance"
```

---

## PART 13: WRAP-UP (0:30)

```bash
# Show final task statistics
stats

# List all notes with their tags
list notes

# Show a note with all its links
show note 1

# Exit StudyPal
exit
```

---

## BONUS COMMANDS (if you have extra time)

```bash
# Create more specific tasks
add task "Write recursion function" --due 2025-11-26 --priority 4 --desc "Implement factorial and fibonacci recursively"

# Delete a task
delete task 5

# Delete a note
delete note 5

# Update note tags
update note 2 --tags python,oop,classes,objects

# Show task with full details
show task 2
```

---

## VIDEO STRUCTURE SUGGESTIONS

### Introduction (0:30)
- Show terminal, explain StudyPal
- Run `help` to show capabilities

### Core Features (3:00)
- Notes: create, list, search, link
- Tasks: create, prioritize, track
- Basic organization and management

### AI Features (3:00)
- Suggestions (links, tags)
- Study planning (week, daily)
- Summaries and expansion
- Quiz generation
- Knowledge assistant
- Study buddy chat mode
- Semantic search

### Conclusion (0:30)
- Show stats and progress
- Highlight key features
- Show test results (`py -m pytest`)

---

## PRESENTATION TIPS

1. ✅ Have your OpenAI API key set up BEFORE recording
2. ✅ Clear `data/notes.json` and `data/tasks.json` before starting for clean demo
3. ✅ Type commands smoothly - practice beforehand
4. ✅ Read the output briefly to show what's happening
5. ✅ Emphasize AI features - they're the most impressive
6. ✅ Show the chat mode - it's unique and engaging
7. ✅ Keep a steady pace - don't rush or drag
8. ✅ If something goes wrong, stay calm and continue

9. 💡 Consider showing code briefly:
   - Show one Python file (e.g., `agents.py`) to demonstrate development
   - Run `pytest` to show testing

10. 🎯 End with stats and a completed task list to show functionality

---

## ALTERNATIVE SHORTER DEMO (4-5 minutes)

If you need a shorter version, focus on:

1. **Quick intro + help** (0:30)
2. **Create 2 notes, 2 tasks** (0:45)
3. **AI link suggestions** (0:30)
4. **Study planning** (0:30)
5. **Quiz generation** (0:30)
6. **Chat mode demo** (1:00)
7. **Semantic search** (0:30)
8. **Stats and exit** (0:15)

---

## 🎬 Ready to Record!

Follow the commands in order, demonstrate the features naturally, and show how StudyPal makes studying more organized and efficient with AI-powered assistance. Good luck with your video!
