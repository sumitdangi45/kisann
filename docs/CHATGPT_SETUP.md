# ChatGPT API Integration Guide

## Overview
KisanSathi ab Gemini aur ChatGPT dono APIs support karta hai. Aap apni preference ke hisaab se koi bhi use kar sakte ho.

## ChatGPT API - Free vs Paid

### Free Tier (gpt-3.5-turbo)
- **Cost**: Free (limited requests)
- **Rate Limit**: 3 requests/min
- **Response Time**: Slower
- **Quality**: Good for basic queries
- **Best For**: Testing, low-traffic apps

### Paid Tier (gpt-4 or gpt-3.5-turbo)
- **Cost**: $0.0005 per 1K input tokens, $0.0015 per 1K output tokens
- **Rate Limit**: Unlimited (based on plan)
- **Response Time**: Fast
- **Quality**: Excellent
- **Best For**: Production apps, high-traffic

## Setup Steps

### Step 1: Get OpenAI API Key
1. Go to https://platform.openai.com/account/api-keys
2. Sign up or login with your account
3. Click "Create new secret key"
4. Copy the key (save it safely!)

### Step 2: Update .env File
```bash
# kisansathi/backend/.env

GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_api_key_here
USE_CHATGPT=true  # Set to true to use ChatGPT, false for Gemini
```

### Step 3: Install Dependencies
```bash
cd kisansathi/backend
pip install -r requirements.txt
```

### Step 4: Run Backend
```bash
python app.py
```

## Switching Between APIs

### Use ChatGPT
```bash
# In .env file
USE_CHATGPT=true
```

### Use Gemini
```bash
# In .env file
USE_CHATGPT=false
```

## API Comparison

| Feature | Gemini | ChatGPT |
|---------|--------|---------|
| Free Tier | Yes (60 req/min) | Yes (3 req/min) |
| Language Support | Excellent | Excellent |
| Hindi Support | Good | Good |
| Response Quality | Very Good | Excellent |
| Speed | Fast | Very Fast |
| Cost | Free tier available | Paid only |

## Pricing Calculator

### ChatGPT (gpt-3.5-turbo)
- Average message: ~100 input tokens, ~100 output tokens
- Cost per message: ~$0.0001
- 1000 messages/day: ~$0.10/day = ~$3/month

### ChatGPT (gpt-4)
- Average message: ~100 input tokens, ~100 output tokens
- Cost per message: ~$0.003
- 1000 messages/day: ~$3/day = ~$90/month

## Troubleshooting

### Error: "ChatGPT API not configured"
- Check if `OPENAI_API_KEY` is set in `.env`
- Verify API key is correct
- Make sure `USE_CHATGPT=true` in `.env`

### Error: "Rate limit exceeded"
- Free tier has 3 requests/min limit
- Upgrade to paid tier for unlimited requests
- Or switch to Gemini API

### Error: "Invalid API key"
- Check if API key is correct
- Regenerate key from OpenAI dashboard
- Make sure there are no extra spaces in `.env`

## Features Supported

Both APIs support:
- ✅ Crop Recommendation
- ✅ Fertilizer Advice
- ✅ Disease Detection
- ✅ Weather Alerts
- ✅ Crop Tracking
- ✅ General Farming Questions
- ✅ Hindi/English Auto-detection
- ✅ Conversational Interface

## Recommendations

### For Development
- Use **Gemini** (free, 60 req/min)
- Or use **ChatGPT free tier** (3 req/min)

### For Production
- Use **ChatGPT paid** (gpt-3.5-turbo for cost-effective)
- Or use **Gemini** (free tier sufficient for most cases)

### For Best Quality
- Use **ChatGPT gpt-4** (most expensive but best quality)
- Or use **Gemini** (free and very good quality)

## Example Usage

```python
# In .env
OPENAI_API_KEY=sk-...
USE_CHATGPT=true

# Backend will automatically use ChatGPT
# No code changes needed!
```

## Support

For issues:
1. Check API key is valid
2. Check rate limits
3. Check internet connection
4. Check `.env` file configuration
5. Check backend logs for errors

---

**Last Updated**: April 2026
