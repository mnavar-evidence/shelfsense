"""ShelfSense MCP Server - Expose ShelfSense functionality to ChatGPT"""
import asyncio
import os
from datetime import datetime, timedelta
from typing import Optional, Any
import httpx
import json

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server


# API Base URL - will be set to Railway URL after deployment
API_BASE_URL = os.getenv("SHELFSENSE_API_URL", "http://localhost:8000")


class ShelfSenseClient:
    """Client to interact with ShelfSense Mock API"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_locations(self, location_type: Optional[str] = None) -> list:
        """Get all locations"""
        params = {}
        if location_type:
            params["location_type"] = location_type

        response = await self.client.get(f"{self.base_url}/api/locations", params=params)
        response.raise_for_status()
        return response.json()

    async def get_location(self, location_id: str) -> dict:
        """Get specific location"""
        response = await self.client.get(f"{self.base_url}/api/locations/{location_id}")
        response.raise_for_status()
        return response.json()

    async def get_products(self, category: Optional[str] = None) -> list:
        """Get all products"""
        params = {}
        if category:
            params["category"] = category

        response = await self.client.get(f"{self.base_url}/api/products", params=params)
        response.raise_for_status()
        return response.json()

    async def get_pick_list(self, location_id: str, date: Optional[str] = None) -> dict:
        """Get pick list for a location"""
        params = {"location_id": location_id}
        if date:
            params["date"] = date

        response = await self.client.get(f"{self.base_url}/api/pick-list", params=params)
        response.raise_for_status()
        return response.json()

    async def get_all_pick_lists(self, date: Optional[str] = None) -> list:
        """Get pick lists for all locations"""
        params = {}
        if date:
            params["date"] = date

        response = await self.client.get(f"{self.base_url}/api/pick-list/all", params=params)
        response.raise_for_status()
        return response.json()

    async def get_demand_forecast(
        self,
        location_id: str,
        product_id: Optional[str] = None,
        forecast_date: Optional[str] = None
    ) -> list:
        """Get demand forecast"""
        params = {"location_id": location_id}
        if product_id:
            params["product_id"] = product_id
        if forecast_date:
            params["forecast_date"] = forecast_date

        response = await self.client.get(f"{self.base_url}/api/forecast/demand", params=params)
        response.raise_for_status()
        return response.json()

    async def get_model_accuracy(
        self,
        location_id: Optional[str] = None,
        product_id: Optional[str] = None
    ) -> list:
        """Get model accuracy metrics"""
        params = {}
        if location_id:
            params["location_id"] = location_id
        if product_id:
            params["product_id"] = product_id

        response = await self.client.get(f"{self.base_url}/api/models/product-accuracy", params=params)
        response.raise_for_status()
        return response.json()

    async def get_inventory_status(
        self,
        location_id: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> list:
        """Get inventory status"""
        params = {}
        if location_id:
            params["location_id"] = location_id
        if status_filter:
            params["status_filter"] = status_filter

        response = await self.client.get(f"{self.base_url}/api/inventory/status", params=params)
        response.raise_for_status()
        return response.json()

    async def get_analytics_summary(self) -> dict:
        """Get analytics summary"""
        response = await self.client.get(f"{self.base_url}/api/analytics/summary")
        response.raise_for_status()
        return response.json()


# Initialize server and client
app = Server("shelfsense-mcp-server")
shelfsense = ShelfSenseClient(API_BASE_URL)


# ==================== MCP Tools ====================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available ShelfSense tools"""
    return [
        Tool(
            name="get_locations",
            description="Get all micromarket locations (hotels, offices, airports, hospitals). Optionally filter by type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_type": {
                        "type": "string",
                        "description": "Filter by type: hotel, office, airport, or hospital (optional)",
                        "enum": ["hotel", "office", "airport", "hospital"]
                    }
                }
            }
        ),
        Tool(
            name="get_pick_list",
            description="Get the AI-generated pick list for restocking a specific micromarket location. Shows recommended quantities for each product based on demand forecasts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "The location ID (e.g., 'loc_westin_sf')"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format (optional, defaults to today)"
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="get_all_pick_lists",
            description="Get pick lists for all locations at once. Useful for seeing the complete daily restocking plan.",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format (optional, defaults to today)"
                    }
                }
            }
        ),
        Tool(
            name="get_demand_forecast",
            description="Get AI-powered demand forecast with confidence intervals (P10/P50/P90) for products at a location. Shows factors influencing the forecast like occupancy and events.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "The location ID"
                    },
                    "product_id": {
                        "type": "string",
                        "description": "Specific product ID (optional, returns all products if omitted)"
                    },
                    "forecast_date": {
                        "type": "string",
                        "description": "Date to forecast for in YYYY-MM-DD format (optional, defaults to tomorrow)"
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="get_model_accuracy",
            description="Get machine learning model accuracy metrics showing how well forecasts match actual demand. Includes MAE, RMSE, and accuracy percentage.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Filter by location ID (optional)"
                    },
                    "product_id": {
                        "type": "string",
                        "description": "Filter by product ID (optional)"
                    }
                }
            }
        ),
        Tool(
            name="get_inventory_status",
            description="Get current inventory levels and status (optimal, low, critical, overstock) across products and locations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "Filter by location ID (optional)"
                    },
                    "status_filter": {
                        "type": "string",
                        "description": "Filter by status (optional)",
                        "enum": ["optimal", "low", "critical", "overstock"]
                    }
                }
            }
        ),
        Tool(
            name="get_analytics_summary",
            description="Get overall analytics summary including total locations, forecast accuracy, stockout risks, and top-selling products.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="explain_pick_quantity",
            description="Get a detailed explanation for why a specific quantity was recommended for a product at a location.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "The location ID"
                    },
                    "product_name": {
                        "type": "string",
                        "description": "The product name to explain"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format (optional, defaults to today)"
                    }
                },
                "required": ["location_id", "product_name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "get_locations":
            location_type = arguments.get("location_type")
            data = await shelfsense.get_locations(location_type)
            return [TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )]

        elif name == "get_pick_list":
            location_id = arguments["location_id"]
            date = arguments.get("date")
            data = await shelfsense.get_pick_list(location_id, date)
            return [TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )]

        elif name == "get_all_pick_lists":
            date = arguments.get("date")
            data = await shelfsense.get_all_pick_lists(date)

            # Format nicely
            summary = f"# Pick Lists for {date or 'Today'}\n\n"
            for pick_list in data:
                summary += f"## {pick_list['location_name']}\n"
                summary += f"- Total items: {pick_list['total_items']}\n"
                summary += f"- Estimated time: {pick_list['estimated_time_minutes']} minutes\n"
                summary += f"- High priority items: {sum(1 for item in pick_list['items'] if item['priority'] == 'high')}\n\n"

            return [TextContent(
                type="text",
                text=summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
            )]

        elif name == "get_demand_forecast":
            location_id = arguments["location_id"]
            product_id = arguments.get("product_id")
            forecast_date = arguments.get("forecast_date")
            data = await shelfsense.get_demand_forecast(location_id, product_id, forecast_date)
            return [TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )]

        elif name == "get_model_accuracy":
            location_id = arguments.get("location_id")
            product_id = arguments.get("product_id")
            data = await shelfsense.get_model_accuracy(location_id, product_id)

            # Format summary
            if data:
                avg_accuracy = sum(item["accuracy_percentage"] for item in data) / len(data)
                summary = f"# Model Accuracy Summary\n\n"
                summary += f"Average Accuracy: {avg_accuracy:.1f}%\n"
                summary += f"Total Samples: {len(data)}\n\n"

                return [TextContent(
                    type="text",
                    text=summary + "Full data:\n" + json.dumps(data, indent=2)
                )]
            else:
                return [TextContent(type="text", text="No accuracy data found.")]

        elif name == "get_inventory_status":
            location_id = arguments.get("location_id")
            status_filter = arguments.get("status_filter")
            data = await shelfsense.get_inventory_status(location_id, status_filter)

            # Group by status
            status_counts = {}
            for item in data:
                status = item["status"]
                status_counts[status] = status_counts.get(status, 0) + 1

            summary = f"# Inventory Status Summary\n\n"
            for status, count in sorted(status_counts.items()):
                summary += f"- {status.upper()}: {count} items\n"

            return [TextContent(
                type="text",
                text=summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
            )]

        elif name == "get_analytics_summary":
            data = await shelfsense.get_analytics_summary()

            # Format nicely
            summary = f"""# ShelfSense Analytics Summary

## Overview
- Total Locations: {data['total_locations']}
- Total Products: {data['total_products']}
- Average Forecast Accuracy: {data['avg_forecast_accuracy']:.1f}%

## Today's Picks
- Total picks scheduled: {data['total_picks_today']}

## Inventory Health
- Stockout risks: {data['stockout_risk_count']}
- Overstock items: {data['overstock_count']}
- Optimal stock: {data['optimal_stock_count']}

## Top Selling Products
"""
            for product in data['top_selling_products']:
                summary += f"- {product['product_name']}: {product['units_sold']} units (${product['revenue']:.2f})\n"

            return [TextContent(
                type="text",
                text=summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
            )]

        elif name == "explain_pick_quantity":
            location_id = arguments["location_id"]
            product_name = arguments["product_name"]
            date = arguments.get("date")

            # Get pick list
            pick_list = await shelfsense.get_pick_list(location_id, date)

            # Find the product
            item = next(
                (item for item in pick_list["items"] if item["product_name"].lower() == product_name.lower()),
                None
            )

            if not item:
                return [TextContent(
                    type="text",
                    text=f"Product '{product_name}' not found in pick list for {location_id}"
                )]

            explanation = f"""# Pick Quantity Explanation: {product_name}

**Location:** {item['location_name']}
**Recommended Quantity:** {item['recommended_quantity']}
**Priority:** {item['priority'].upper()}
**Confidence:** {item['confidence_score']*100:.1f}%

## Current State
- Current stock: {item['current_stock']} units
- Last restocked: {item['last_restocked']}

## Demand Forecast
- P10 (pessimistic): {item['forecast']['p10']} units
- P50 (median): {item['forecast']['p50']} units
- P90 (optimistic): {item['forecast']['p90']} units

## Reasoning
{item['reason']}

## Calculation
The recommended quantity of {item['recommended_quantity']} is calculated by:
1. Using the median forecast (P50: {item['forecast']['p50']} units)
2. Applying a 30% safety bias for conservative stocking
3. Accounting for 3% shrinkage
4. Considering current stock levels ({item['current_stock']} units)

This ensures we maintain adequate inventory while minimizing stockouts.
"""

            return [TextContent(type="text", text=explanation)]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error calling {name}: {str(e)}"
        )]


# ==================== Run Server ====================

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
