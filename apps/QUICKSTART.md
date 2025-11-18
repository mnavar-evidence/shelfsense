# ShelfSense ChatGPT Integration - Quick Start

Get ShelfSense running in ChatGPT in 10 minutes!

## Prerequisites

- Python 3.11+
- Railway account (free tier works)
- ChatGPT Desktop App
- Terminal/Command Line

## Step 1: Deploy to Railway (5 minutes)

### Option A: Automated Deployment

```bash
cd shelfsense/apps
./deploy.sh
```

The script will:
1. Deploy the Mock API server
2. Get the API URL
3. Optionally deploy the MCP server
4. Display configuration instructions

### Option B: Manual Deployment

**Deploy Mock API:**
```bash
cd shelfsense-mock-api
railway login
railway init
railway up
railway domain
```

Save the URL (e.g., `your-api.up.railway.app`)

**Configure MCP Server:**
```bash
cd ../shelfsense-mcp-server
# Update the URL below with your Railway URL
export SHELFSENSE_API_URL=https://your-api.up.railway.app
```

## Step 2: Test the API (1 minute)

```bash
# Replace with your Railway URL
curl https://your-api.up.railway.app/health

# Test locations endpoint
curl https://your-api.up.railway.app/api/locations
```

You should see JSON responses with ShelfSense data.

## Step 3: Configure ChatGPT (2 minutes)

1. **Open ChatGPT Desktop App**

2. **Go to Settings** → **Model Context Protocol**

3. **Add this configuration:**

   Update the file path and URL in `mcp-config.json`:
   ```json
   {
     "mcpServers": {
       "shelfsense": {
         "command": "python",
         "args": [
           "/Users/mnavar/Work/coding/projects/shelf-sense/apps/shelfsense-mcp-server/server.py"
         ],
         "env": {
           "SHELFSENSE_API_URL": "https://your-api.up.railway.app"
         }
       }
     }
   }
   ```

4. **Restart ChatGPT Desktop**

## Step 4: Test in ChatGPT (2 minutes)

Start a new chat and try:

### Basic Commands
```
Show me all ShelfSense locations
```

```
Get today's pick list for the Westin San Francisco
```

```
What's the demand forecast for Coca-Cola at the Marriott?
```

### Advanced Queries
```
Explain why I need to restock 8 Snickers bars at the Westin
```

```
Give me an analytics summary across all locations
```

```
Show me which products have critical inventory levels
```

```
What's the model accuracy for the Chicago location?
```

## Troubleshooting

### "No tools available" in ChatGPT

✅ **Solution:**
- Verify the file path in `mcp-config.json` is correct (use absolute path)
- Restart ChatGPT Desktop completely
- Check that Python is accessible from command line: `python --version`

### "Connection refused" errors

✅ **Solution:**
- Test the Mock API URL: `curl https://your-api.up.railway.app/health`
- Verify `SHELFSENSE_API_URL` in the MCP config matches your Railway URL
- Check Railway logs: `railway logs`

### MCP server not starting

✅ **Solution:**
```bash
# Test locally first
cd shelfsense-mcp-server
pip install -r requirements.txt
export SHELFSENSE_API_URL=https://your-api.up.railway.app
python server.py
```

If it works locally but not in ChatGPT, check the file paths in `mcp-config.json`.

### Railway deployment fails

✅ **Solution:**
- Check you're logged in: `railway whoami`
- Verify requirements.txt exists
- Check Railway build logs for specific errors
- Ensure Procfile is present

## What's Next?

### Explore Features

Try asking ChatGPT:
- "What locations do you have data for?"
- "Show me the pick list for all locations"
- "Which products are top sellers?"
- "What's the forecast accuracy?"
- "Show inventory status for Boston Medical Center"

### Customize Data

Edit sample data in `shelfsense-mock-api/sample_data.py`:
- Add your own locations
- Customize products
- Adjust forecasting parameters

### Add Authentication

For production, add API keys:
```python
# In main.py
from fastapi import Header, HTTPException

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != "your-secret-key":
        raise HTTPException(status_code=401)
```

## Railway URLs

After deployment, bookmark these:
- **API Docs**: `https://your-api.up.railway.app/docs`
- **Health Check**: `https://your-api.up.railway.app/health`
- **Locations**: `https://your-api.up.railway.app/api/locations`
- **Pick Lists**: `https://your-api.up.railway.app/api/pick-list/all`

## Cost Estimate

Railway free tier includes:
- $5 free credit per month
- Plenty for development and demos
- Upgrade to Hobby ($5/month) for production

Estimated usage:
- Mock API: ~$2-3/month on free tier
- MCP Server: Runs locally (no cost)

## Support

**Documentation:**
- Main README: `SHELFSENSE_CHATGPT_README.md`
- Mock API: `shelfsense-mock-api/README.md`
- MCP Server: `shelfsense-mcp-server/README.md`

**Testing:**
```bash
# Test Mock API
cd shelfsense-mock-api
python test_api.py https://your-api.up.railway.app

# Test MCP Client
cd shelfsense-mcp-server
python test_mcp.py https://your-api.up.railway.app
```

**Railway Commands:**
```bash
railway status     # Check deployment status
railway logs       # View application logs
railway open       # Open project in browser
railway down       # Pause deployment
```

## Success Checklist

- [ ] Mock API deployed to Railway
- [ ] API health check returns 200
- [ ] MCP config added to ChatGPT
- [ ] ChatGPT shows ShelfSense tools
- [ ] Can query locations successfully
- [ ] Can get pick lists
- [ ] Can ask for explanations

Once all checked, you're ready to go! 🎉

## Example Session

```
You: Show me all locations

ChatGPT: I found 5 ShelfSense micromarket locations:

1. Westin St. Francis - San Francisco (Hotel)
   - 1195 rooms, 78% occupancy

2. Marriott Marquis - Times Square (Hotel)
   - 1966 rooms, 85% occupancy

3. Hilton Chicago O'Hare Airport (Hotel)
   - 858 rooms, 72% occupancy

4. TechCorp Campus - Austin (Office)
   - 2500 capacity, 65% occupancy

5. Boston Medical Center - Staff Lounge (Hospital)
   - 95% utilization

Which location would you like to explore?
```

Perfect! You're all set up. Start exploring ShelfSense through ChatGPT!
