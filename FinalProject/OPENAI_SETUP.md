# OpenAI API Setup Guide for StudyPal

## Overview

StudyPal now supports AI-powered planning features using OpenAI's API. The following commands will use AI when an API key is configured:

- `plan week` - Generates an intelligent weekly study schedule
- `plan today` - Provides AI-powered daily task recommendations

**Note:** StudyPal works without an API key, but will use simpler rule-based planning instead.

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
   py -m src.studypal
   ```

2. **Try an AI command:**
   ```
   plan week
   ```

3. **What to expect:**
   - **With API key configured:** You'll get an AI-generated, personalized study plan
   - **Without API key:** You'll get a basic rule-based plan (still functional!)
   - **API error:** You'll see an error message and fall back to basic planning

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

- **plan week command:** ~$0.002-0.003 per request
- **plan today command:** ~$0.001-0.002 per request

For typical use (5-10 planning requests per day), expect monthly costs of **less than $1**.

### Usage Tips

1. **Set usage limits** in your OpenAI dashboard to control spending
2. **Monitor usage** at https://platform.openai.com/account/usage
3. StudyPal automatically falls back to basic planning if API calls fail
4. The API is only called when you run planning commands

## Privacy & Security

- Your API key is stored locally in `.env` (not committed to git)
- Task and note data is sent to OpenAI only during planning commands
- Data is not stored by OpenAI (per their API policy)
- You can revoke your API key anytime in the OpenAI dashboard

## Features with AI vs. Without AI

| Feature | With OpenAI API | Without API |
|---------|----------------|-------------|
| `plan week` | Intelligent scheduling considering task context, optimal distribution, and study patterns | Rule-based distribution by priority and due date |
| `plan today` | AI-powered task prioritization with reasoning | Simple sorting by priority and due date |
| Other features | No difference | No difference |

## Disabling AI Features

To disable AI features and use only basic planning:

1. Remove the API key from `.env`
2. Or unset the environment variable:
   ```powershell
   Remove-Item Env:\OPENAI_API_KEY
   ```

StudyPal will automatically use basic planning without any errors.

## Support

- **OpenAI API Issues:** https://help.openai.com/
- **StudyPal Issues:** Check the main README.md or create an issue
