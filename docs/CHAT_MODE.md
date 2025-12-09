# Study Buddy Chat Mode 🎓

## Overview

The Study Buddy Chat Mode provides an interactive, conversational AI tutor that helps you learn more effectively. Unlike the one-off `ask` command, chat mode creates a persistent conversation where the AI remembers your previous questions and maintains context throughout your study session.

## Features

### 🤖 Conversational Learning
- **Continuous Dialogue**: The AI remembers your conversation history
- **Context-Aware**: References your specific notes and tasks
- **Adaptive Responses**: Adjusts explanations based on your questions

### 📚 Study Support
- **Concept Explanations**: Get clear, simple explanations of difficult topics
- **Interactive Quizzing**: Request quizzes on any topic from your notes
- **Study Strategies**: Receive personalized study advice
- **Motivation**: Encouraging, supportive feedback to keep you going

### 🎯 Smart Context
The AI has access to:
- All your notes (titles, tags, and content)
- Your current tasks and their status
- Previous messages in the current chat session

## Usage

### Starting Chat Mode

```bash
studypal> chat
```

This launches the interactive chat interface.

### Example Conversation

```
💭 You: Can you explain what recursion is?

🤖 Study Buddy: Recursion is when a function calls itself to solve 
a problem by breaking it down into smaller, similar sub-problems. 
Think of it like Russian nesting dolls - each doll contains a smaller 
version of itself until you reach the smallest one.

The key components are:
1. Base case - the stopping condition
2. Recursive case - where the function calls itself

Would you like me to show you an example from your notes, or would 
you prefer a practice problem?

💭 You: Show me an example

🤖 Study Buddy: [Provides example with explanation...]
```

### Exit Commands

To leave chat mode, use any of these:
- `bye`
- `exit`
- `quit`
- `stop`
- `end`

Or press `Ctrl+C` (will prompt you to use an exit command)

## Example Use Cases

### 1. Topic Explanation
```
💭 You: What's the difference between lists and tuples in Python?
```

### 2. Interactive Quiz
```
💭 You: Quiz me on data structures
```

### 3. Study Planning
```
💭 You: I have an exam next week. How should I prepare?
```

### 4. Concept Clarification
```
💭 You: I don't understand how binary search works
```

### 5. Reference Your Notes
```
💭 You: Can you summarize my Python notes?
```

## Tips for Best Results

### ✅ DO:
- **Be specific**: "Explain binary search" is better than "explain algorithms"
- **Ask follow-ups**: The AI remembers context, so build on previous questions
- **Request examples**: "Show me an example" or "Give me a practice problem"
- **Use your notes**: "Quiz me on my Python notes"

### ❌ DON'T:
- Ask questions completely unrelated to studying (it's focused on helping you learn)
- Expect it to remember conversations from previous sessions (each session is fresh)
- Use it for homework answers without understanding (it's a tutor, not a cheater!)

## Chat vs Ask Command

| Feature | Chat Mode | Ask Command |
|---------|-----------|-------------|
| Remembers context | ✅ Yes (in session) | ❌ No |
| Conversation flow | ✅ Multi-turn | ❌ Single Q&A |
| Interactive quizzing | ✅ Yes | ⚠️ Limited |
| Study guidance | ✅ Personalized | ⚠️ Basic |
| Best for | Deep learning, tutoring | Quick questions |

## Technical Details

- **Model**: GPT-4o-mini (fast and cost-effective)
- **Memory**: Stores last 15 exchanges (30 messages)
- **Temperature**: 0.7 (balanced creativity/accuracy)
- **Max Tokens**: 600 per response (keeps responses concise)

## Session Summary

When you exit chat mode, you'll see:
```
======================================================================
👋 Thanks for studying with me!
Session summary: 8 message exchanges
Keep up the great work! 🌟
======================================================================
```

This shows how many back-and-forth exchanges you had in the session.

## Requirements

- OpenAI API key configured (see `OPENAI_SETUP.md`)
- Active internet connection
- At least Python 3.7+

## Troubleshooting

### "OPENAI_API_KEY not found"
Set your API key:
```bash
$env:OPENAI_API_KEY="your-key-here"
```

### Chat Mode Not Responding
- Check your internet connection
- Verify API key is valid
- Check OpenAI API status

### Conversation Seems Off
- Try ending the session and starting fresh with `bye`
- Each session starts with a clean slate
- Use `clear conversation` in regular mode if needed

## Privacy Note

- Conversations are sent to OpenAI's API
- No data is permanently stored beyond your session
- Each chat session is independent
- See OpenAI's privacy policy for API usage details
