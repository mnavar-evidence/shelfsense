#!/bin/bash

# ShelfSense Railway Deployment Script
# This script helps deploy both servers to Railway

set -e  # Exit on error

echo "🚀 ShelfSense Railway Deployment"
echo "================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "📝 Logging into Railway..."
railway login

echo ""
echo "Step 1: Deploy Mock API Server"
echo "==============================="
cd shelfsense-mock-api

if [ ! -d ".git" ]; then
    echo "Initializing Railway project for Mock API..."
    railway init
fi

echo "Deploying Mock API..."
railway up

echo ""
echo "Getting Mock API URL..."
MOCK_API_URL=$(railway domain 2>/dev/null || echo "")

if [ -z "$MOCK_API_URL" ]; then
    echo "⚠️  No domain found. Generating one..."
    railway domain
    MOCK_API_URL=$(railway domain)
fi

echo "✅ Mock API deployed at: https://$MOCK_API_URL"
echo ""

# Save the URL for MCP server
echo "$MOCK_API_URL" > ../mock_api_url.txt

cd ..

echo ""
echo "Step 2: Deploy MCP Server (Optional - typically runs locally)"
echo "=============================================================="
read -p "Do you want to deploy the MCP server to Railway? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd shelfsense-mcp-server

    if [ ! -d ".git" ]; then
        echo "Initializing Railway project for MCP Server..."
        railway init
    fi

    echo "Setting SHELFSENSE_API_URL environment variable..."
    railway variables set SHELFSENSE_API_URL="https://$MOCK_API_URL"

    echo "Deploying MCP Server..."
    railway up

    echo "✅ MCP Server deployed"
    cd ..
else
    echo "⏭️  Skipping MCP Server deployment (will run locally)"
fi

echo ""
echo "✅ Deployment Complete!"
echo "======================"
echo ""
echo "Mock API URL: https://$MOCK_API_URL"
echo "API Documentation: https://$MOCK_API_URL/docs"
echo ""
echo "Next steps:"
echo "1. Test the API: curl https://$MOCK_API_URL/health"
echo "2. Configure ChatGPT with MCP server (see SHELFSENSE_CHATGPT_README.md)"
echo "3. Update mcp-config.json with your API URL"
echo ""
echo "To configure ChatGPT Desktop:"
echo "  Update SHELFSENSE_API_URL in mcp-config.json to: https://$MOCK_API_URL"
echo ""
