# ShelfSense MCP Server

Model Context Protocol (MCP) server that exposes ShelfSense functionality to ChatGPT and other AI assistants.

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI assistants to external data sources and tools. This server allows ChatGPT to interact with ShelfSense inventory management features through a set of well-defined tools.

## Features

### Available Tools

1. **get_locations** - List micromarket locations with optional filtering
2. **get_pick_list** - Get AI-generated pick lists for restocking
3. **get_all_pick_lists** - Get pick lists for all locations
4. **get_demand_forecast** - Get demand forecasts with confidence intervals
5. **get_model_accuracy** - View ML model performance metrics
6. **get_inventory_status** - Check current inventory levels
7. **get_analytics_summary** - Overall analytics dashboard
8. **explain_pick_quantity** - Get detailed explanations for pick quantities

## Local Development

### Prerequisites
- Python 3.11+
- ShelfSense Mock API running (locally or on Railway)

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set API URL (if not using localhost:8000)
export SHELFSENSE_API_URL=https://your-railway-api.up.railway.app

# Run the server
python server.py
```

### Testing with MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run the inspector
mcp-inspector python server.py
```

## Railway Deployment

### Deploy to Railway

1. **Create a new Railway project**
   ```bash
   railway login
   railway init
   ```

2. **Deploy**
   ```bash
   railway up
   ```

3. **Set environment variables**
   ```bash
   railway variables set SHELFSENSE_API_URL=https://your-mock-api.up.railway.app
   ```

### Environment Variables

- `SHELFSENSE_API_URL` - URL of the ShelfSense Mock API (required)

## Integrating with ChatGPT

### Option 1: ChatGPT Desktop App (Recommended)

1. Open ChatGPT Desktop settings
2. Navigate to "Model Context Protocol"
3. Add a new server:
   ```json
   {
     "shelfsense": {
       "command": "python",
       "args": ["/path/to/server.py"],
       "env": {
         "SHELFSENSE_API_URL": "https://your-railway-api.up.railway.app"
       }
     }
   }
   ```

### Option 2: API Integration

Use the MCP server as a bridge in your own application:

```python
import asyncio
from server import shelfsense, ShelfSenseClient

# Initialize client
client = ShelfSenseClient("https://your-api.up.railway.app")

# Get data
locations = await client.get_locations()
pick_list = await client.get_pick_list("loc_westin_sf")
```

## Example Interactions

Once integrated with ChatGPT, you can ask:

- "Show me today's pick list for the Westin San Francisco"
- "What's the demand forecast for Coca-Cola at the Marriott?"
- "Explain why the recommended quantity for Snickers is 8 units"
- "What locations have critical inventory levels?"
- "Show me the model accuracy for the Chicago location"
- "Give me an analytics summary across all locations"

## Architecture

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   ChatGPT   │ ◄─MCP─► │  MCP Server      │ ◄─HTTP─►│  Mock API       │
│             │         │  (This Project)  │         │  (FastAPI)      │
└─────────────┘         └──────────────────┘         └─────────────────┘
                               │
                               │ Uses
                               ▼
                        ┌──────────────┐
                        │ ShelfSense   │
                        │ Client       │
                        └──────────────┘
```

## Tech Stack

- **MCP SDK** - Model Context Protocol Python implementation
- **httpx** - Async HTTP client
- **Pydantic** - Data validation
- **Python 3.11** - Runtime

## Tool Schemas

All tools follow OpenAPI-compatible schemas and return structured JSON data. Each tool includes:
- Clear descriptions
- Typed parameters with validation
- Optional parameters for filtering
- Human-readable responses with summaries

## Development Tips

### Adding New Tools

1. Add the tool definition to `list_tools()`
2. Implement the handler in `call_tool()`
3. Use the ShelfSenseClient to fetch data
4. Format responses with summaries + full JSON

### Error Handling

The server catches and returns errors gracefully:
- API connection errors
- Invalid parameters
- Missing data

### Logging

Add logging for debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Troubleshooting

**MCP server not connecting:**
- Check that `SHELFSENSE_API_URL` is set correctly
- Verify the Mock API is running and accessible
- Check firewall/network settings

**Tools not appearing in ChatGPT:**
- Restart ChatGPT Desktop app
- Verify MCP server configuration in settings
- Check server logs for errors

**Empty or error responses:**
- Verify Mock API is returning data
- Check API endpoint URLs match
- Review server logs for exceptions
