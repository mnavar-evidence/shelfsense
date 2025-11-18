# ShelfSense ChatGPT Integration

> MCP server and mock API for integrating ShelfSense micromarket inventory management into ChatGPT

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![MCP](https://img.shields.io/badge/MCP-1.1.2-purple.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

**ShelfSense** is an AI-powered micromarket inventory management platform. This repository provides:

- **🤖 MCP Server** - Connects ChatGPT to ShelfSense functionality via Model Context Protocol
- **🌐 Mock API** - FastAPI backend with realistic sample data for hotels, offices, and hospitals
- **📊 AI Forecasting** - Demand predictions with confidence intervals (P10/P50/P90)
- **☁️ Railway Ready** - Deploy to Railway in minutes

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/mnavar-evidence/shelfsense.git
cd shelfsense/apps

# 2. Deploy to Railway (automated)
./deploy.sh

# 3. Configure ChatGPT Desktop
# See QUICKSTART.md for detailed instructions
```

**Complete setup in 10 minutes!** → [QUICKSTART.md](QUICKSTART.md)

## Features

### ChatGPT Integration

Ask ChatGPT natural language questions:
- ✅ "Show me today's pick list for the Westin San Francisco"
- ✅ "What's the demand forecast for Coca-Cola at the Marriott?"
- ✅ "Explain why the recommended quantity is 8 units"
- ✅ "Give me an analytics summary across all locations"
- ✅ "Which products have critical inventory levels?"

### Available Tools

1. **get_locations** - List micromarket locations (hotels, offices, hospitals)
2. **get_pick_list** - AI-generated restocking recommendations
3. **get_demand_forecast** - Demand predictions with confidence ranges
4. **get_model_accuracy** - ML model performance metrics
5. **get_inventory_status** - Current stock levels and alerts
6. **get_analytics_summary** - Overall performance dashboard
7. **explain_pick_quantity** - Detailed reasoning for recommendations

### Sample Data

- **5 Locations**: Westin SF, Marriott NYC, Hilton Chicago, Austin Office, Boston Hospital
- **20+ Products**: Beverages, snacks, fresh food, health items
- **Realistic Scenarios**: Dynamic forecasts based on occupancy, seasonality, events

## Project Structure

```
shelfsense/
└── apps/
    ├── shelfsense-mock-api/        # FastAPI backend server
    │   ├── main.py                 # API endpoints
    │   ├── models.py               # Data models
    │   ├── sample_data.py          # Realistic test data
    │   └── README.md
    │
    ├── shelfsense-mcp-server/      # MCP server for ChatGPT
    │   ├── server.py               # MCP implementation
    │   └── README.md
    │
    ├── QUICKSTART.md               # 10-minute setup guide
    ├── SHELFSENSE_CHATGPT_README.md # Complete documentation
    ├── README.md                   # This file
    ├── mcp-config.json             # ChatGPT configuration
    └── deploy.sh                   # Automated Railway deployment
```

## Local Development

### Run Mock API

```bash
cd shelfsense-mock-api
pip install -r requirements.txt
python main.py
```

API runs at `http://localhost:8000` with docs at `/docs`

### Run MCP Server

```bash
cd shelfsense-mcp-server
pip install -r requirements.txt
export SHELFSENSE_API_URL=http://localhost:8000
python server.py
```

### Test

```bash
# Test Mock API
cd shelfsense-mock-api
python test_api.py

# Test MCP Client
cd shelfsense-mcp-server
python test_mcp.py
```

## Railway Deployment

### Automated

```bash
./deploy.sh
```

### Manual

```bash
# Deploy Mock API
cd shelfsense-mock-api
railway init
railway up
railway domain

# Deploy MCP Server (optional - typically runs locally)
cd shelfsense-mcp-server
railway init
railway variables set SHELFSENSE_API_URL=https://your-api.up.railway.app
railway up
```

## ChatGPT Configuration

Add to ChatGPT Desktop settings (Settings → Model Context Protocol):

```json
{
  "mcpServers": {
    "shelfsense": {
      "command": "python",
      "args": ["/path/to/shelfsense/apps/shelfsense-mcp-server/server.py"],
      "env": {
        "SHELFSENSE_API_URL": "https://your-railway-api.up.railway.app"
      }
    }
  }
}
```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## API Endpoints

- `GET /api/locations` - List all locations
- `GET /api/products` - List all products
- `GET /api/pick-list` - Get pick list for a location
- `GET /api/forecast/demand` - Get demand forecasts
- `GET /api/models/product-accuracy` - Model accuracy metrics
- `GET /api/inventory/status` - Inventory status
- `GET /api/analytics/summary` - Analytics dashboard

Full API documentation: `https://your-api.up.railway.app/docs`

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 10 minutes
- **[SHELFSENSE_CHATGPT_README.md](SHELFSENSE_CHATGPT_README.md)** - Complete integration guide
- **[shelfsense-mock-api/README.md](shelfsense-mock-api/README.md)** - Mock API documentation
- **[shelfsense-mcp-server/README.md](shelfsense-mcp-server/README.md)** - MCP server details

## Tech Stack

- **Python 3.11** - Runtime
- **FastAPI** - Web framework
- **MCP SDK** - Model Context Protocol
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **Railway** - Cloud hosting

## Use Cases

- 🏨 Hotel micromarkets (lobby, gym, rooftop)
- 🏢 Office break rooms
- ✈️ Airport terminals
- 🏥 Hospital cafeterias & staff lounges
- 🎓 University campus markets
- 🚂 Transit hubs

## Example Session

```
You: Show me today's pick list for the Westin San Francisco

ChatGPT: Here's today's pick list for Westin St. Francis - San Francisco:

📦 Total Items: 15
⏱️ Estimated Time: 45 minutes

HIGH PRIORITY (Stock ≤2):
• Coca-Cola Classic 12oz: Restock 9 units (current: 1)
  Reason: 78% occupancy, high demand forecast (P50: 7 units)

• Dasani Water 16.9oz: Restock 11 units (current: 0)
  Reason: Critical stock level, weekend surge expected

• Snickers Bar: Restock 8 units (current: 2)
  Reason: Historical accuracy 89%, preventing stockout

[Additional items...]

Would you like me to explain any specific quantities?
```

## Contributing

This is a demonstration project for integrating ShelfSense with ChatGPT via MCP. Feel free to:
- Fork and customize for your use case
- Add new MCP tools and API endpoints
- Improve sample data and forecasting algorithms
- Submit issues and pull requests

## License

MIT License - See LICENSE file for details

## Support

- 📖 **Documentation**: See docs in this repository
- 🐛 **Issues**: [GitHub Issues](https://github.com/mnavar-evidence/shelfsense/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mnavar-evidence/shelfsense/discussions)

## Roadmap

- [ ] Authentication & API keys
- [ ] Real database integration (PostgreSQL)
- [ ] Advanced ML models (LSTM/XGBoost)
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Real-time inventory sync
- [ ] Webhook notifications

## Acknowledgments

Built with:
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [FastAPI](https://fastapi.tiangolo.com)
- [Railway](https://railway.app)
- [OpenAI ChatGPT](https://openai.com/chatgpt)

---

**Ready to get started?** → [QUICKSTART.md](QUICKSTART.md)

**Need help?** → [SHELFSENSE_CHATGPT_README.md](SHELFSENSE_CHATGPT_README.md)
