# ShelfSense

> AI-powered micromarket inventory management platform with ChatGPT integration

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![MCP](https://img.shields.io/badge/MCP-1.1.2-purple.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

ShelfSense is a comprehensive AI-powered retail analytics and inventory management platform designed for micromarkets (small self-service retail locations in hotels, offices, airports, and hospitals).

This repository contains:

- **iOS Mobile App** - Production SwiftUI app for warehouse operators
- **React Dashboard** - Modern management dashboard (Vite + TypeScript)
- **Marketing Website** - Public-facing site built with React
- **ChatGPT Integration** - MCP server and mock API for AI assistant integration
- **ML Models & Documentation** - Forecasting models and pilot data

## Repository Structure

```
shelf-sense/
├── apps/                          # ChatGPT Integration (MCP + Mock API)
│   ├── shelfsense-mcp-server/     # MCP server for ChatGPT
│   ├── shelfsense-mock-api/       # FastAPI mock backend
│   ├── README.md                  # Apps documentation
│   ├── QUICKSTART.md              # 10-minute setup guide
│   └── deploy.sh                  # Railway deployment script
│
├── iOSApp/                        # iOS Mobile Application (SwiftUI)
│   ├── Models/                    # Data models
│   ├── Views/                     # SwiftUI views
│   ├── Services/                  # API and AI services
│   └── ...
│
├── shelfsense-dashboard/          # React Dashboard (Vite)
│   ├── src/                       # Source files
│   └── ...
│
├── shelfsense.ai/                 # Marketing Website (React)
│   ├── src/                       # Source files
│   └── ...
│
├── GrabScanGo/                    # ML Models & Pilot Data
│   ├── forecasting/               # Model documentation
│   └── data/                      # Hotel pilot data
│
└── Diagrams/                      # Architecture diagrams
```

## Quick Links

### 🤖 ChatGPT Integration
**Start Here →** [apps/README.md](apps/README.md)

Deploy ShelfSense to ChatGPT in 10 minutes using MCP (Model Context Protocol):
```bash
cd apps
./deploy.sh
```

Features:
- AI-powered pick list generation
- Demand forecasting with confidence intervals
- Conversational inventory queries
- Real-time analytics

### 📱 iOS App
Production-ready mobile app for warehouse operators:
- Pick list management
- AI assistant chat integration
- Barcode scanning
- Offline-first architecture
- Truck routing optimization

### 🌐 Web Dashboard
Modern inventory management dashboard:
- Real-time forecasting visualization
- Pricing analysis
- Occupancy-based adjustments
- Reconciliation tools

### 🎨 Marketing Site
Public-facing website showcasing the platform

## Getting Started

### ChatGPT Integration (Most Popular)
```bash
cd apps
# See apps/QUICKSTART.md for complete setup
./deploy.sh
```

### Local Development
```bash
# iOS App
cd iOSApp
open ShelfSense.xcodeproj

# React Dashboard
cd shelfsense-dashboard
npm install
npm run dev

# Marketing Site
cd shelfsense.ai
npm install
npm start
```

## What is ShelfSense?

ShelfSense uses machine learning to optimize inventory management for micromarkets:

1. **Demand Forecasting** - LSTM/XGBoost models predict product demand with confidence ranges (P10/P50/P90)
2. **Smart Pick Lists** - AI-generated restocking recommendations with priority and reasoning
3. **Conversational Interface** - Operators can ask "Why do I need 8 units?" and get instant explanations
4. **Model Accuracy Tracking** - Continuous learning from actual vs. predicted demand
5. **Context-Aware** - Considers occupancy rates, seasonality, weather, and events

## Use Cases

- 🏨 Hotel micromarkets (lobby, gym, rooftop)
- 🏢 Office break rooms and cafeterias
- ✈️ Airport and transit terminals
- 🏥 Hospital cafeterias and staff lounges
- 🎓 University campus markets
- 🚂 Corporate gyms and break rooms

## Documentation

- **[ChatGPT Integration Guide](apps/README.md)** - MCP server setup and deployment
- **[Quick Start](apps/QUICKSTART.md)** - Get running in 10 minutes
- **[Complete Documentation](apps/SHELFSENSE_CHATGPT_README.md)** - Detailed integration guide
- **White Papers** - AI-powered retail solutions in root directory

## Tech Stack

### ChatGPT Integration
- Python 3.11, FastAPI, MCP SDK
- Railway for hosting

### Mobile
- SwiftUI, iOS native
- OpenAI GPT-4 integration

### Frontend
- React 18/19, TypeScript, Vite
- TailwindCSS, Recharts

### AI/ML
- LSTM/XGBoost models
- OpenAI GPT-4 assistant
- Context-aware intelligence

## Sample Data

The ChatGPT integration includes realistic sample data:
- **5 Locations**: Westin SF, Marriott NYC, Hilton Chicago, Austin Office, Boston Hospital
- **20+ Products**: Beverages, snacks, fresh food, health items
- **Dynamic Forecasts**: Based on occupancy, seasonality, and events

## Contributing

This project demonstrates AI-powered inventory management with ChatGPT integration. Feel free to:
- Fork and customize
- Submit issues and PRs
- Improve ML models
- Add new features

## License

MIT License - See LICENSE file for details

## Support

- 📖 **Documentation**: See docs in respective directories
- 🐛 **Issues**: [GitHub Issues](https://github.com/mnavar-evidence/shelfsense/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mnavar-evidence/shelfsense/discussions)

---

**Ready to integrate with ChatGPT?** → [apps/QUICKSTART.md](apps/QUICKSTART.md)

**Want to explore the full platform?** → Check out individual directories above
