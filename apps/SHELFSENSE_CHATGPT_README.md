# ShelfSense ChatGPT Integration

Complete guide to embedding ShelfSense inventory management inside ChatGPT using MCP (Model Context Protocol).

## Overview

This project enables ChatGPT to interact with ShelfSense micromarket inventory management through:

1. **Mock API Server** - FastAPI backend simulating ShelfSense with realistic data
2. **MCP Server** - Bridge connecting ChatGPT to ShelfSense functionality
3. **Railway Deployment** - Cloud hosting for both servers

## Architecture

```
┌──────────────────┐
│   ChatGPT App    │
│                  │
│  "Show me the    │
│   pick list for  │
│   Westin SF"     │
└────────┬─────────┘
         │ MCP Protocol
         ▼
┌──────────────────┐
│  MCP Server      │  ← shelfsense-mcp-server/
│  (Railway)       │     Python MCP implementation
└────────┬─────────┘
         │ REST API
         ▼
┌──────────────────┐
│  Mock API        │  ← shelfsense-mock-api/
│  (Railway)       │     FastAPI server with sample data
└──────────────────┘
```

## Quick Start

### 1. Deploy Mock API to Railway

```bash
cd shelfsense-mock-api

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up

# Get the URL
railway domain
# Save this URL: https://your-api.up.railway.app
```

### 2. Deploy MCP Server to Railway

```bash
cd ../shelfsense-mcp-server

# Initialize Railway project
railway init

# Set the Mock API URL
railway variables set SHELFSENSE_API_URL=https://your-api.up.railway.app

# Deploy
railway up
```

### 3. Configure ChatGPT Desktop

#### For ChatGPT Desktop App:

1. Open ChatGPT Desktop
2. Go to Settings → Model Context Protocol
3. Add new MCP server configuration:

**If running locally:**
```json
{
  "mcpServers": {
    "shelfsense": {
      "command": "python",
      "args": ["/Users/mnavar/Work/coding/projects/shelf-sense/apps/shelfsense-mcp-server/server.py"],
      "env": {
        "SHELFSENSE_API_URL": "https://your-railway-api.up.railway.app"
      }
    }
  }
}
```

**If using Railway for MCP (Advanced):**
MCP servers typically run locally to connect to ChatGPT. For production deployments, you'd integrate via custom ChatGPT Actions or GPT configuration.

### 4. Test in ChatGPT

Ask ChatGPT:
- "Show me all ShelfSense locations"
- "Get today's pick list for Westin San Francisco"
- "What's the demand forecast for Coca-Cola at the Marriott?"
- "Explain why I need to restock 8 Snickers bars"
- "Give me an analytics summary"

## Features

### Available ChatGPT Commands

Once integrated, ChatGPT can:

#### Location Management
- ✅ List all micromarket locations (hotels, offices, hospitals, airports)
- ✅ Filter locations by type
- ✅ Get detailed location information (occupancy, capacity, contact)

#### Pick Lists & Restocking
- ✅ Generate daily pick lists with AI-recommended quantities
- ✅ See prioritized items (high/medium/low)
- ✅ Get explanations for recommended quantities
- ✅ View estimated restocking time

#### Demand Forecasting
- ✅ Get demand forecasts with confidence intervals (P10/P50/P90)
- ✅ See contributing factors (occupancy, weather, events)
- ✅ Forecast specific products or entire locations

#### Analytics & Insights
- ✅ Model accuracy metrics (MAE, RMSE, accuracy %)
- ✅ Inventory status (optimal/low/critical/overstock)
- ✅ Overall analytics summary
- ✅ Top-selling products
- ✅ Stockout risk detection

## Sample Data

### Locations (5 micromarkets)
1. **Westin St. Francis** - San Francisco hotel (1195 rooms, 78% occupancy)
2. **Marriott Marquis** - NYC Times Square (1966 rooms, 85% occupancy)
3. **Hilton O'Hare** - Chicago airport hotel (858 rooms, 72% occupancy)
4. **TechCorp Campus** - Austin office (2500 capacity, 65% occupancy)
5. **Boston Medical Center** - Hospital staff lounge (95% utilization)

### Products (20+ items)
- **Beverages**: Coke, Pepsi, Water, Red Bull, Starbucks, Gatorade, OJ
- **Snacks**: Lay's, Doritos, Pringles, Snickers, KIND bars, Trail mix
- **Fresh Food**: Sandwiches, salads, yogurt, fruit cups
- **Miscellaneous**: Gum, Advil, hand sanitizer

## Example ChatGPT Conversations

### Getting a Pick List
```
You: Show me today's pick list for the Westin San Francisco

ChatGPT: Here's today's pick list for Westin St. Francis - San Francisco:

Total Items: 15
Estimated Time: 45 minutes

HIGH PRIORITY (Stock ≤2):
- Coca-Cola Classic 12oz: Restock 9 units (current: 1)
- Dasani Water 16.9oz: Restock 11 units (current: 0)
- Snickers Bar: Restock 8 units (current: 2)

MEDIUM PRIORITY (Stock 3-5):
- Red Bull Energy: Restock 7 units (current: 4)
...
```

### Explaining a Quantity
```
You: Why do I need 8 Snickers bars?

ChatGPT: The recommended quantity of 8 Snickers bars is based on:

📊 Demand Forecast:
- P50 (median): 6 units
- P90 (optimistic): 9 units

🧮 Calculation:
1. Median forecast: 6 units
2. 30% safety bias: +2 units
3. 3% shrinkage accounted for
4. Current stock: 2 units (critically low)

📍 Context:
- Occupancy rate: 78% (932 rooms occupied)
- Historical accuracy: 89%
- This prevents stockout risk based on weekend demand surge
```

### Getting Analytics
```
You: Give me a ShelfSense analytics summary

ChatGPT: ShelfSense Analytics Summary

📊 Overview:
- Total Locations: 5
- Total Products: 20
- Average Forecast Accuracy: 86.5%

📦 Today's Operations:
- Total picks scheduled: 73 items
- Stockout risks: 12 items
- Overstock: 5 items
- Optimal stock: 68 items

🏆 Top Sellers:
1. Coca-Cola Classic: 1,250 units ($3,125)
2. Dasani Water: 1,180 units ($2,360)
3. Snickers Bar: 890 units ($1,335)
```

## Project Structure

```
shelf-sense/
├── shelfsense-mock-api/          # FastAPI backend
│   ├── main.py                   # API endpoints
│   ├── models.py                 # Pydantic data models
│   ├── sample_data.py            # Realistic test data
│   ├── requirements.txt          # Python dependencies
│   ├── Procfile                  # Railway config
│   └── README.md
│
├── shelfsense-mcp-server/        # MCP server for ChatGPT
│   ├── server.py                 # MCP implementation
│   ├── requirements.txt          # Python dependencies
│   ├── Procfile                  # Railway config
│   └── README.md
│
└── SHELFSENSE_CHATGPT_README.md  # This file
```

## Deployment Guide

### Railway Setup

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Deploy Mock API**
   ```bash
   cd shelfsense-mock-api
   railway init
   railway up
   railway domain  # Get your URL
   ```

3. **Deploy MCP Server** (Optional - typically runs locally)
   ```bash
   cd shelfsense-mcp-server
   railway init
   railway variables set SHELFSENSE_API_URL=<your-mock-api-url>
   railway up
   ```

4. **Monitor Deployments**
   ```bash
   railway logs
   railway status
   ```

### Local Development

**Run Mock API locally:**
```bash
cd shelfsense-mock-api
pip install -r requirements.txt
python main.py
# Access at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Run MCP Server locally:**
```bash
cd shelfsense-mcp-server
pip install -r requirements.txt
export SHELFSENSE_API_URL=http://localhost:8000
python server.py
```

## Testing

### Test Mock API
```bash
# Health check
curl https://your-api.up.railway.app/health

# Get locations
curl https://your-api.up.railway.app/api/locations

# Get pick list
curl "https://your-api.up.railway.app/api/pick-list?location_id=loc_westin_sf"
```

### Test MCP Server
```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
cd shelfsense-mcp-server
mcp-inspector python server.py
```

## Customization

### Adding New Products
Edit `shelfsense-mock-api/sample_data.py`:
```python
PRODUCTS.append(
    Product(
        id="prod_new_item",
        name="New Product Name",
        category="Beverages",
        price=2.99,
        supplier="Supplier Co"
    )
)
```

### Adding New Locations
Edit `shelfsense-mock-api/sample_data.py`:
```python
LOCATIONS.append(
    Location(
        id="loc_new_location",
        name="New Location Name",
        type="hotel",
        address="123 Main St",
        capacity=500,
        occupancy_rate=0.80
    )
)
```

### Adding New MCP Tools
Edit `shelfsense-mcp-server/server.py`:
1. Add tool definition in `list_tools()`
2. Add handler in `call_tool()`
3. Optionally add API endpoint in mock server

## Troubleshooting

### Mock API Issues
- **Port already in use**: Change PORT in Railway or use different local port
- **Dependencies not installing**: Verify `runtime.txt` specifies Python 3.11
- **CORS errors**: Already configured for `*` origins, check Railway deployment

### MCP Server Issues
- **Can't connect to API**: Verify `SHELFSENSE_API_URL` is set correctly
- **ChatGPT not showing tools**: Restart ChatGPT Desktop, check MCP config
- **Timeout errors**: Increase `httpx.AsyncClient` timeout in `server.py`

### Railway Issues
- **Build failing**: Check logs with `railway logs`
- **Service not starting**: Verify Procfile and requirements.txt
- **Environment variables**: Set with `railway variables set KEY=value`

## Production Considerations

For production deployment:

1. **Authentication**: Add API keys to Mock API endpoints
2. **Rate Limiting**: Implement rate limiting on API
3. **Database**: Replace sample data with real PostgreSQL/MongoDB
4. **Caching**: Add Redis for frequently accessed data
5. **Monitoring**: Set up logging and error tracking (Sentry, DataDog)
6. **HTTPS**: Railway provides HTTPS by default
7. **Backup**: Set up regular database backups

## Tech Stack

- **Python 3.11** - Runtime
- **FastAPI** - Web framework for Mock API
- **MCP SDK** - Model Context Protocol implementation
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **Railway** - Cloud hosting platform

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Railway Docs](https://docs.railway.app)
- [ChatGPT Desktop](https://openai.com/chatgpt/desktop)

## License

MIT License - See individual project files

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Railway deployment logs
3. Test API endpoints directly
4. Verify MCP server configuration

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Configure ChatGPT Desktop
3. ✅ Test basic queries
4. 🔄 Customize data for your use case
5. 🔄 Add authentication
6. 🔄 Connect to real database
7. 🔄 Monitor usage and performance
