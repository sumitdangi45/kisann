# Quick API Switch Guide

## 30 Seconds Setup

### Option 1: Use Gemini (Free, Recommended for Dev)
```bash
# kisansathi/backend/.env

GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_key_here
USE_CHATGPT=false
```

### Option 2: Use ChatGPT (Paid, Recommended for Prod)
```bash
# kisansathi/backend/.env

GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=sk-your_openai_key_here
USE_CHATGPT=true
```

## Get API Keys

### Gemini API Key (Free)
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create new API key
4. Copy and paste in `.env`

### ChatGPT API Key (Paid)
1. Go to https://platform.openai.com/account/api-keys
2. Sign up or login
3. Click "Create new secret key"
4. Copy and paste in `.env`

## That's It!

No code changes needed. Just:
1. Update `.env` file
2. Restart backend
3. Done! ✅

## Verify It's Working

### Check Backend Logs
```bash
cd kisansathi/backend
python app.py

# You should see:
# - If USE_CHATGPT=true: "Using ChatGPT API"
# - If USE_CHATGPT=false: "Using Gemini API"
```

### Test in Frontend
1. Open http://localhost:8080
2. Go to Chatbot
3. Ask a question
4. Should get response in 1-3 seconds

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API not configured" | Check `.env` file has correct key |
| "Rate limit exceeded" | Upgrade to paid tier or use Gemini |
| "Invalid API key" | Regenerate key from provider dashboard |
| "No response" | Check internet connection |

## Cost Comparison

| API | Free Tier | Cost |
|-----|-----------|------|
| Gemini | ✅ Yes (60 req/min) | $0 |
| ChatGPT | ❌ No (3 req/min) | $0.0005/1K tokens |

## Recommendation

- **Development**: Use Gemini (free)
- **Production**: Use ChatGPT (better quality)
- **Budget**: Use Gemini (no cost)
- **Quality**: Use ChatGPT (best)

---

**That's all! Happy farming! 🌾**
