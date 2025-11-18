# ShelfSense Custom GPT Setup for Web

This guide shows how to create a Custom GPT so your entire team can use ShelfSense through ChatGPT web.

## Prerequisites

- ✅ Mock API deployed on Railway
- ✅ ChatGPT Plus or Team subscription (required for Custom GPTs)
- ✅ Railway API URL

## Step 1: Get Your Railway URL

From Railway dashboard:
1. Click on your Mock API service
2. Go to **Settings** → **Networking**
3. Copy your domain (e.g., `shelfsense-mock-api-production-xxxx.up.railway.app`)

## Step 2: Update OpenAPI Schema

1. Open `shelfsense-openapi.yaml`
2. Replace the URL in `servers` section:
   ```yaml
   servers:
     - url: https://YOUR-ACTUAL-RAILWAY-URL.up.railway.app
       description: Production server
   ```

## Step 3: Create Custom GPT

1. **Go to ChatGPT:** https://chat.openai.com
2. **Click your profile** (bottom left)
3. **Select "My GPTs"**
4. **Click "Create a GPT"**

## Step 4: Configure GPT

### In the "Create" Tab:

**Name:**
```
ShelfSense Assistant
```

**Description:**
```
AI-powered micromarket inventory management assistant. Get pick lists, demand forecasts, and analytics for your retail locations.
```

**Instructions:**
```
You are ShelfSense Assistant, an AI-powered inventory management expert for micromarkets (small retail locations in hotels, offices, airports, and hospitals).

Your capabilities:
- Generate and explain AI-powered pick lists with recommended restocking quantities
- Provide demand forecasts with confidence intervals (P10/P50/P90)
- Show inventory status and stockout risks
- Display model accuracy metrics
- Provide analytics summaries

When users ask about pick lists or recommendations:
1. Retrieve the data using the appropriate API
2. Present information clearly with priorities (high/medium/low)
3. Explain the reasoning behind recommendations when asked
4. Highlight critical items that need immediate attention

When users ask "why" questions:
- Explain forecasting factors (occupancy, seasonality, events)
- Break down how quantities are calculated (P50 median + 30% bias + shrinkage)
- Show confidence levels and historical accuracy

Available locations:
- Westin St. Francis - San Francisco (loc_westin_sf)
- Marriott Marquis - Times Square (loc_marriott_nyc)
- Hilton Chicago O'Hare Airport (loc_hilton_chicago)
- TechCorp Campus - Austin (loc_tech_campus_austin)
- Boston Medical Center (loc_hospital_boston)

Be conversational, helpful, and data-driven. Use emojis sparingly for clarity (📦, 🏨, ⚠️).
```

**Conversation starters:**
```
Show me today's pick list for the Westin San Francisco
What's the demand forecast for Coca-Cola?
Which locations have critical inventory levels?
Give me an analytics summary
```

## Step 5: Add Actions

1. **Click "Configure" tab**
2. Scroll to **Actions** section
3. Click **"Create new action"**
4. Click **"Import from URL"** or paste the OpenAPI schema

**Option A: Import from URL (if you host the YAML file)**
- Upload `shelfsense-openapi.yaml` to a public URL
- Paste the URL

**Option B: Paste schema directly**
- Copy the entire contents of `shelfsense-openapi.yaml`
- Paste into the schema editor

5. **Authentication:** Select "None" (API is public)
6. Click **"Save"**

## Step 6: Test Your GPT

In the preview panel, try:
```
Show me all locations
```

```
Get today's pick list for Westin San Francisco
```

```
What's the demand forecast for the Marriott?
```

## Step 7: Publish & Share

1. Click **"Save"** in top right
2. Choose publishing option:
   - **"Only me"** - Just you can use it
   - **"Anyone with a link"** - Share with specific people ✅
   - **"Public"** - Listed in GPT store (optional)

3. If you chose "Anyone with a link":
   - Copy the GPT link
   - Share with your team
   - They'll need ChatGPT Plus/Team to use it

## Team Usage

Your team can now:
1. Open the shared GPT link
2. Start chatting immediately
3. Ask questions like:
   - "Show pick lists for all locations"
   - "Which products are at critical stock levels?"
   - "Explain why I need to restock 8 Snickers bars"
   - "What's our forecast accuracy?"

## Example Conversations

### Getting Pick Lists
```
User: Show me today's pick list for the Westin San Francisco

GPT: Here's today's pick list for Westin St. Francis - San Francisco:

📦 Total Items: 15
⏱️ Estimated Time: 45 minutes

HIGH PRIORITY (Stock ≤2):
• Coca-Cola Classic 12oz: Restock 9 units (current: 1)
• Dasani Water 16.9oz: Restock 11 units (current: 0)
• Snickers Bar: Restock 8 units (current: 2)

Would you like me to explain any of these recommendations?
```

### Understanding Recommendations
```
User: Why do I need 8 Snickers bars?

GPT: The recommended quantity of 8 Snickers bars is based on:

📊 Demand Forecast:
- P50 (median): 6 units
- P90 (optimistic): 9 units

🧮 Calculation:
1. Median forecast: 6 units
2. 30% safety bias applied: +2 units
3. Current stock critically low: 2 units

📍 Context:
- Hotel occupancy: 78% (932 rooms occupied)
- Historical accuracy: 89%
- Prevents weekend stockout risk
```

## Troubleshooting

### "Actions aren't working"
- Verify your Railway URL is correct in the schema
- Test the API directly: `curl https://your-url.up.railway.app/health`
- Check Railway logs for errors

### "Can't create Custom GPT"
- You need ChatGPT Plus or Team subscription
- Regular ChatGPT (free) doesn't support Custom GPTs

### "Team can't access GPT"
- Make sure you set sharing to "Anyone with a link"
- Team members need ChatGPT Plus/Team subscriptions
- Share the direct GPT link

### "API returns errors"
- Check Railway deployment is running
- Verify the API endpoints work in browser
- Check Railway logs for issues

## Cost Considerations

**Railway (Mock API):**
- Free tier: $5 credit/month
- Hobby: $5/month
- Estimated usage: $2-3/month for demo/team use

**ChatGPT:**
- Plus: $20/user/month (required for Custom GPTs)
- Team: $25/user/month (better for teams, includes admin controls)

## Next Steps

1. ✅ Update OpenAPI schema with your Railway URL
2. ✅ Create the Custom GPT following steps above
3. ✅ Test with sample queries
4. ✅ Share link with your team
5. ✅ Monitor usage in Railway dashboard

## Support

- Railway Issues: Check deployment logs
- ChatGPT Issues: OpenAI support
- API Documentation: https://your-railway-url.up.railway.app/docs

---

**Ready to create your Custom GPT?** Follow the steps above and your team will have access to ShelfSense through ChatGPT web! 🚀
