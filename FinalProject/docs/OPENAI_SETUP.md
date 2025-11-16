# OpenAI API Setup Guide for StudyPal

## Overview

StudyPal features extensive AI-powered capabilities using OpenAI's API. The following commands use AI when an API key is configured:

**Planning & Organization:**
- `plan week` - Generates an intelligent weekly study schedule
- `plan today` - Provides AI-powered daily task recommendations

**Note Enhancement:**  
- `suggest links <note_id>` - AI-powered semantic link suggestions between notes
- `suggest tags <note_id>` - AI-generated contextually relevant tags
- `summary <note_id>` - Generate AI-powered note summaries
- `expand <note_id>` - AI-assisted note improvement (expand, clarify, examples, simplify)

**Learning & Study:**
- `quiz <note_id>` - Generate quiz questions from note content
- `search notes "natural language query"` - Semantic search using meaning, not just keywords
- `ask "your question"` - Ask questions about your notes and tasks (conversation memory)
- `chat` - Interactive study buddy chat mode

**IMPORTANT:** An OpenAI API key is required for all AI features. StudyPal will not start without a valid API key configured.

## Getting Your OpenAI API Key

1. **Sign up for OpenAI:**
   - Visit https://platform.openai.com/signup
   - Create an account or sign in

2. **Generate an API Key:**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (it starts with `sk-`)
   - **Important:** Save this key immediately - you won't be able to see it again!

3. **Add Billing Information (Required):**
   - Go to https://platform.openai.com/account/billing
   - Add a payment method
   - OpenAI charges per API usage (very affordable for personal use)
   - Typical cost: ~$0.002 per planning request

## Setup Instructions

### Option 1: Using .env File (Recommended)

1. **Navigate to the FinalProject directory:**
   ```powershell
   cd FinalProject
   ```

2. **Create a .env file from the example:**
   ```powershell
   Copy-Item .env.example .env
   ```
   
   **Note:** The `.env.example` file is already provided in the FinalProject directory.

3. **Edit the .env file:**
   Open `.env` in a text editor and replace `your_openai_api_key_here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

4. **Install required packages:**
   ```powershell
   pip install -r requirements.txt
   ```

### Option 2: Using Environment Variables

Set the environment variable directly in your PowerShell session:

```powershell
$env:OPENAI_API_KEY = "sk-your-actual-key-here"
```

**Note:** This only lasts for the current PowerShell session. You'll need to set it again when you open a new terminal.

### Option 3: System Environment Variable (Windows)

For permanent setup:

1. Open System Properties → Environment Variables
2. Add a new User variable:
   - Name: `OPENAI_API_KEY`
   - Value: Your API key
3. Restart your terminal/VS Code

## Verifying Setup

1. **Start StudyPal:**
   ```powershell
   # Option 1: Run directly
   py studypal.py
   
   # Option 2: Run as module
   py -m src.studypal
   ```

2. **Try an AI command:**
   ```
   # Planning features
   plan week
   plan today
   
   # Note enhancement (requires existing notes)
   suggest links 1
   suggest tags 1
   summary 1
   
   # Interactive features
   ask "What should I study today?"
   chat
   ```

3. **What to expect:**
   - **With valid API key:** You'll get AI-generated responses for all AI commands
   - **Without API key:** StudyPal will exit with an error message on startup
   - **Invalid API key:** You'll see an error and the program will not start

## Troubleshooting

### "OpenAI API error" Message

**Possible causes:**
1. Invalid API key - double-check you copied it correctly
2. API key expired or revoked - generate a new one
3. No billing information - add payment method to your OpenAI account
4. Rate limit exceeded - wait a few minutes and try again
5. Network connectivity issues - check your internet connection

### "Import 'openai' could not be resolved"

**Solution:**
```powershell
# Make sure you're in the FinalProject directory
cd FinalProject
pip install -r requirements.txt
```

### Environment variable not loading

**Check if it's set:**
```powershell
echo $env:OPENAI_API_KEY
```

If empty, the variable isn't set. Use one of the setup options above.

## API Usage and Costs

### Estimated Costs

**Per-command estimates:**
- **Planning commands** (`plan week`, `plan today`): ~$0.002-0.003 per request
- **Note enhancement** (`suggest`, `summary`, `expand`): ~$0.001-0.002 per request  
- **Quiz generation** (`quiz`): ~$0.002-0.004 per request
- **Search & ask** (`search`, `ask`): ~$0.001-0.002 per request
- **Chat mode** (`chat`): ~$0.001-0.003 per message

For typical daily use (10-20 AI requests), expect monthly costs of **$1-3**.

### Usage Tips

1. **Set usage limits** in your OpenAI dashboard to control spending
2. **Monitor usage** at https://platform.openai.com/account/usage
3. StudyPal automatically falls back to basic planning if API calls fail
4. The API is only called when you run planning commands

## Project Structure

StudyPal is organized as a Python package:

```
FinalProject/
├── .env.example          # Template for environment variables
├── .env                  # Your actual API key (create from .env.example)
├── studypal.py          # Main entry point
├── requirements.txt     # Python dependencies
├── src/studypal/        # Main package
│   ├── __main__.py      # Module entry point
│   ├── cli.py           # Command-line interface
│   ├── agents.py        # AI planning agents
│   └── ...              # Other modules
└── data/                # Your notes and tasks
```

## Privacy & Security

- Your API key is stored locally in `.env` (not committed to git)
- The `.env.example` file provides a template without your actual key
- Task and note data is sent to OpenAI only during planning commands
- Data is not stored by OpenAI (per their API policy)
- You can revoke your API key anytime in the OpenAI dashboard

## AI-Powered Features

StudyPal uses OpenAI GPT-3.5 for comprehensive AI assistance:

| Feature | Description |
|---------|-------------|
| `plan week` | Intelligent weekly scheduling considering task context, optimal distribution, and study patterns |
| `plan today` | AI-powered daily task prioritization with reasoning |
| `suggest links <note_id>` | Semantic analysis to find meaningful connections between notes |
| `suggest tags <note_id>` | Context-aware tag generation based on note content |
| `summary <note_id>` | Intelligent note summarization highlighting key points |
| `expand <note_id>` | Note enhancement with multiple modes (expand, clarify, examples, simplify) |
| `quiz <note_id>` | Automatic quiz generation from note content with various question types |
| `search notes "query"` | Natural language semantic search that understands meaning and context |
| `ask "question"` | Conversational AI assistant with memory for questions about your study materials |
| `chat` | Interactive study buddy for ongoing conversations and study support |
| `clear conversation` | Reset AI conversation memory |

**Note:** ALL AI features require a valid OpenAI API key. Basic features (add/edit notes, tasks, manual linking) work without AI.

## Support

- **OpenAI API Issues:** https://help.openai.com/
- **StudyPal Issues:** Check the main README.md or create an issue
