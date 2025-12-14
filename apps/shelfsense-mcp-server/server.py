"""ShelfSense MCP Server - Expose ShelfSense functionality to ChatGPT via HTTP/SSE"""
import asyncio
import os
from datetime import datetime, timedelta
from typing import Optional, Any
import httpx
import json

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
import uvicorn


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

    async def get_product_performance(
        self,
        location_id: Optional[str] = None,
        product_id: Optional[str] = None,
        category: Optional[str] = None,
        performance_tier: Optional[str] = None
    ) -> list:
        """Get product performance analytics"""
        params = {}
        if location_id:
            params["location_id"] = location_id
        if product_id:
            params["product_id"] = product_id
        if category:
            params["category"] = category
        if performance_tier:
            params["performance_tier"] = performance_tier

        response = await self.client.get(f"{self.base_url}/api/analytics/product-performance", params=params)
        response.raise_for_status()
        return response.json()

    async def get_top_performers(self, location_id: Optional[str] = None, limit: int = 10) -> list:
        """Get top performing products"""
        params = {"limit": limit}
        if location_id:
            params["location_id"] = location_id

        response = await self.client.get(f"{self.base_url}/api/analytics/top-performers", params=params)
        response.raise_for_status()
        return response.json()

    async def get_trends(
        self,
        location_id: Optional[str] = None,
        product_id: Optional[str] = None,
        trend_direction: Optional[str] = None,
        has_anomaly: Optional[bool] = None
    ) -> list:
        """Get trend detection data"""
        params = {}
        if location_id:
            params["location_id"] = location_id
        if product_id:
            params["product_id"] = product_id
        if trend_direction:
            params["trend_direction"] = trend_direction
        if has_anomaly is not None:
            params["has_anomaly"] = str(has_anomaly).lower()

        response = await self.client.get(f"{self.base_url}/api/analytics/trends", params=params)
        response.raise_for_status()
        return response.json()

    async def get_anomalies(self, location_id: Optional[str] = None, severity: Optional[str] = None) -> list:
        """Get products with anomalies"""
        params = {}
        if location_id:
            params["location_id"] = location_id
        if severity:
            params["severity"] = severity

        response = await self.client.get(f"{self.base_url}/api/analytics/anomalies", params=params)
        response.raise_for_status()
        return response.json()

    async def get_alerts(
        self,
        location_id: Optional[str] = None,
        alert_type: Optional[str] = None,
        severity: Optional[str] = None
    ) -> dict:
        """Get system alerts"""
        params = {}
        if location_id:
            params["location_id"] = location_id
        if alert_type:
            params["alert_type"] = alert_type
        if severity:
            params["severity"] = severity

        response = await self.client.get(f"{self.base_url}/api/alerts", params=params)
        response.raise_for_status()
        return response.json()

    async def get_critical_alerts(self, location_id: Optional[str] = None) -> dict:
        """Get critical alerts"""
        params = {}
        if location_id:
            params["location_id"] = location_id

        response = await self.client.get(f"{self.base_url}/api/alerts/critical", params=params)
        response.raise_for_status()
        return response.json()

    async def get_stockout_alerts(self, location_id: Optional[str] = None) -> dict:
        """Get stockout risk alerts"""
        params = {}
        if location_id:
            params["location_id"] = location_id

        response = await self.client.get(f"{self.base_url}/api/alerts/stockout-risks", params=params)
        response.raise_for_status()
        return response.json()


# Initialize MCP server and API client
mcp = FastMCP("shelfsense-mcp-server")
shelfsense = ShelfSenseClient(API_BASE_URL)


# ==================== MCP Tools ====================

@mcp.tool()
async def get_locations(location_type: str = None) -> str:
    """Get all micromarket locations (hotels, offices, airports, hospitals). Optionally filter by type."""
    try:
        data = await shelfsense.get_locations(location_type)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_pick_list(location_id: str, date: str = None) -> str:
    """Get the AI-generated pick list for restocking a specific micromarket location. Shows recommended quantities for each product based on demand forecasts."""
    try:
        data = await shelfsense.get_pick_list(location_id, date)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_all_pick_lists(date: str = None) -> str:
    """Get pick lists for all locations at once. Useful for seeing the complete daily restocking plan."""
    try:
        data = await shelfsense.get_all_pick_lists(date)

        # Format nicely
        summary = f"# Pick Lists for {date or 'Today'}\n\n"
        for pick_list in data:
            summary += f"## {pick_list['location_name']}\n"
            summary += f"- Total items: {pick_list['total_items']}\n"
            summary += f"- Estimated time: {pick_list['estimated_time_minutes']} minutes\n"
            summary += f"- High priority items: {sum(1 for item in pick_list['items'] if item['priority'] == 'high')}\n\n"

        return summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_demand_forecast(location_id: str, product_id: str = None, forecast_date: str = None) -> str:
    """Get AI-powered demand forecast with confidence intervals (P10/P50/P90) for products at a location. Shows factors influencing the forecast like occupancy and events."""
    try:
        data = await shelfsense.get_demand_forecast(location_id, product_id, forecast_date)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_model_accuracy(location_id: str = None, product_id: str = None) -> str:
    """Get machine learning model accuracy metrics showing how well forecasts match actual demand. Includes MAE, RMSE, and accuracy percentage."""
    try:
        data = await shelfsense.get_model_accuracy(location_id, product_id)

        if data:
            avg_accuracy = sum(item["accuracy_percentage"] for item in data) / len(data)
            summary = f"# Model Accuracy Summary\n\n"
            summary += f"Average Accuracy: {avg_accuracy:.1f}%\n"
            summary += f"Total Samples: {len(data)}\n\n"
            return summary + "Full data:\n" + json.dumps(data, indent=2)
        else:
            return "No accuracy data found."
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_inventory_status(location_id: str = None, status_filter: str = None) -> str:
    """Get current inventory levels and status (optimal, low, critical, overstock) across products and locations."""
    try:
        data = await shelfsense.get_inventory_status(location_id, status_filter)

        # Group by status
        status_counts = {}
        for item in data:
            status = item["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        summary = f"# Inventory Status Summary\n\n"
        for status, count in sorted(status_counts.items()):
            summary += f"- {status.upper()}: {count} items\n"

        return summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_analytics_summary() -> str:
    """Get overall analytics summary including total locations, forecast accuracy, stockout risks, and top-selling products."""
    try:
        data = await shelfsense.get_analytics_summary()

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

        return summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def explain_pick_quantity(location_id: str, product_name: str, date: str = None) -> str:
    """Get a detailed explanation for why a specific quantity was recommended for a product at a location."""
    try:
        pick_list = await shelfsense.get_pick_list(location_id, date)

        # Find the product
        item = next(
            (item for item in pick_list["items"] if item["product_name"].lower() == product_name.lower()),
            None
        )

        if not item:
            return f"Product '{product_name}' not found in pick list for {location_id}"

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
        return explanation
    except Exception as e:
        return f"Error: {str(e)}"


# ==================== NEW: Product Performance Tools ====================

@mcp.tool()
async def get_product_performance(location_id: str = None, product_id: str = None, category: str = None, performance_tier: str = None) -> str:
    """Get product performance analytics including sales velocity, turnover rates, revenue, and performance scores. Filter by location, product, category, or tier (top_performer, average, underperformer, slow_mover)."""
    try:
        data = await shelfsense.get_product_performance(location_id, product_id, category, performance_tier)

        if not data:
            return "No performance data found for the specified filters."

        # Create summary
        summary = f"# Product Performance Analytics\n\n"
        summary += f"**Total Products Analyzed:** {len(data)}\n\n"

        # Group by tier
        tiers = {}
        for item in data:
            tier = item['performance_tier']
            tiers[tier] = tiers.get(tier, 0) + 1

        summary += "## Performance Distribution\n"
        for tier, count in sorted(tiers.items()):
            summary += f"- {tier.replace('_', ' ').title()}: {count} products\n"

        # Top 5 by performance score
        summary += "\n## Top 5 by Performance Score\n"
        for item in data[:5]:
            summary += f"- **{item['product_name']}** ({item.get('location_name', 'All locations')}): {item['performance_score']}/100\n"
            summary += f"  - Daily velocity: {item['daily_velocity']} units/day\n"
            summary += f"  - 30-day revenue: ${item['revenue_30d']:.2f}\n"

        return summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_top_performers(location_id: str = None, limit: int = 10) -> str:
    """Get the top performing products ranked by performance score. Shows sales metrics, velocity, and revenue."""
    try:
        data = await shelfsense.get_top_performers(location_id, limit)

        summary = f"# Top {len(data)} Performing Products\n\n"

        if location_id:
            summary += f"**Location filter:** {location_id}\n\n"

        for i, item in enumerate(data, 1):
            summary += f"## {i}. {item['product_name']}\n"
            summary += f"- **Performance Score:** {item['performance_score']}/100 ({item['performance_tier']})\n"
            summary += f"- **Category:** {item['category']}\n"
            summary += f"- **Daily Velocity:** {item['daily_velocity']} units/day\n"
            summary += f"- **7-Day Revenue:** ${item['revenue_7d']:.2f}\n"
            summary += f"- **30-Day Revenue:** ${item['revenue_30d']:.2f}\n"
            summary += f"- **Turnover Rate:** {item['turnover_rate']}x/month\n"
            summary += f"- **Days of Supply:** {item['days_of_supply']} days\n\n"

        return summary
    except Exception as e:
        return f"Error: {str(e)}"


# ==================== NEW: Trend Detection Tools ====================

@mcp.tool()
async def get_trends(location_id: str = None, product_id: str = None, trend_direction: str = None) -> str:
    """Get trend detection data showing week-over-week changes, seasonality patterns, and anomalies. Filter by direction: increasing, decreasing, or stable."""
    try:
        data = await shelfsense.get_trends(location_id, product_id, trend_direction, None)

        if not data:
            return "No trend data found for the specified filters."

        summary = "# Trend Analysis\n\n"

        # Group by direction
        directions = {}
        for item in data:
            d = item['trend_direction']
            directions[d] = directions.get(d, 0) + 1

        summary += "## Trend Distribution\n"
        for direction, count in sorted(directions.items()):
            emoji = {"increasing": "📈", "decreasing": "📉", "stable": "➡️"}.get(direction, "")
            summary += f"- {emoji} {direction.title()}: {count} products\n"

        # Highlight significant trends
        significant = [item for item in data if abs(item['week_over_week_change']) > 15]
        if significant:
            summary += "\n## Significant Trends (>15% WoW change)\n"
            for item in significant[:5]:
                change = item['week_over_week_change']
                emoji = "🔺" if change > 0 else "🔻"
                summary += f"- {emoji} **{item['product_name']}**: {change:+.1f}% WoW\n"
                if item.get('location_name'):
                    summary += f"  - Location: {item['location_name']}\n"
                if item['is_seasonal_peak']:
                    summary += f"  - Currently in seasonal peak (factor: {item['seasonality_factor']}x)\n"

        # Anomalies
        anomalies = [item for item in data if item['has_anomaly']]
        if anomalies:
            summary += "\n## Detected Anomalies\n"
            for item in anomalies:
                summary += f"- ⚠️ **{item['product_name']}**: {item['anomaly_description']}\n"
                summary += f"  - Severity: {item['anomaly_severity']}\n"

        return summary + "\n\nFull data:\n" + json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_anomalies(location_id: str = None, severity: str = None) -> str:
    """Get products with detected anomalies in sales patterns. Filter by severity: low, medium, or high."""
    try:
        data = await shelfsense.get_anomalies(location_id, severity)

        if not data:
            return "No anomalies detected for the specified filters. This is good news!"

        summary = f"# Detected Anomalies\n\n"
        summary += f"**Total anomalies found:** {len(data)}\n\n"

        # Group by severity
        severities = {}
        for item in data:
            s = item['anomaly_severity']
            severities[s] = severities.get(s, 0) + 1

        summary += "## Severity Breakdown\n"
        severity_emoji = {"high": "🔴", "medium": "🟠", "low": "🟡"}
        for s in ["high", "medium", "low"]:
            if s in severities:
                summary += f"- {severity_emoji[s]} {s.title()}: {severities[s]}\n"

        summary += "\n## Anomaly Details\n"
        for item in data:
            emoji = severity_emoji.get(item['anomaly_severity'], "⚪")
            summary += f"\n### {emoji} {item['product_name']}\n"
            if item.get('location_name'):
                summary += f"- **Location:** {item['location_name']}\n"
            summary += f"- **Type:** {item['anomaly_type']}\n"
            summary += f"- **Severity:** {item['anomaly_severity']}\n"
            summary += f"- **Description:** {item['anomaly_description']}\n"
            summary += f"- **Trend:** {item['trend_direction']} ({item['week_over_week_change']:+.1f}% WoW)\n"

        return summary
    except Exception as e:
        return f"Error: {str(e)}"


# ==================== NEW: Alerts Tools ====================

@mcp.tool()
async def get_alerts(location_id: str = None, alert_type: str = None, severity: str = None) -> str:
    """Get system alerts for stockouts, overstocks, anomalies, trends, and performance issues. Filter by type (stockout_risk, overstock, anomaly, trend_change, performance) or severity (critical, warning, info)."""
    try:
        data = await shelfsense.get_alerts(location_id, alert_type, severity)

        summary = f"# ShelfSense Alerts\n\n"
        summary += f"**Total Alerts:** {data['total_alerts']}\n"
        summary += f"- 🔴 Critical: {data['critical_count']}\n"
        summary += f"- 🟠 Warning: {data['warning_count']}\n"
        summary += f"- 🔵 Info: {data['info_count']}\n\n"
        summary += f"**Locations Affected:** {data['locations_affected']}\n"
        summary += f"**Products Affected:** {data['products_affected']}\n\n"

        severity_emoji = {"critical": "🔴", "warning": "🟠", "info": "🔵"}

        for alert in data['alerts']:
            emoji = severity_emoji.get(alert['severity'], "⚪")
            summary += f"---\n\n### {emoji} {alert['title']}\n"
            summary += f"**Type:** {alert['alert_type'].replace('_', ' ').title()}\n"
            summary += f"**Severity:** {alert['severity'].upper()}\n"
            if alert.get('location_name'):
                summary += f"**Location:** {alert['location_name']}\n"
            if alert.get('product_name'):
                summary += f"**Product:** {alert['product_name']}\n"
            summary += f"\n{alert['description']}\n\n"
            summary += f"**Recommended Action:** {alert['recommended_action']}\n\n"

        return summary
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_critical_alerts(location_id: str = None) -> str:
    """Get only critical severity alerts requiring immediate attention. These are urgent issues that need to be addressed now."""
    try:
        data = await shelfsense.get_critical_alerts(location_id)

        if data['critical_count'] == 0:
            return "✅ No critical alerts at this time. All systems operating normally."

        summary = f"# 🚨 CRITICAL ALERTS\n\n"
        summary += f"**{data['critical_count']} critical issues require immediate attention!**\n\n"

        for alert in data['alerts']:
            summary += f"---\n\n### 🔴 {alert['title']}\n"
            if alert.get('location_name'):
                summary += f"**Location:** {alert['location_name']}\n"
            if alert.get('product_name'):
                summary += f"**Product:** {alert['product_name']}\n"
            if alert.get('metric_value') is not None:
                summary += f"**Current Value:** {alert['metric_value']} (threshold: {alert['threshold_value']})\n"
            summary += f"\n{alert['description']}\n\n"
            summary += f"**⚡ ACTION REQUIRED:** {alert['recommended_action']}\n\n"

        return summary
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_stockout_risks(location_id: str = None) -> str:
    """Get alerts for products at risk of stockout. Shows which products need immediate restocking attention."""
    try:
        data = await shelfsense.get_stockout_alerts(location_id)

        if data['total_alerts'] == 0:
            return "✅ No stockout risks detected. All products have adequate inventory levels."

        summary = f"# Stockout Risk Alerts\n\n"
        summary += f"**{data['total_alerts']} products at risk of stockout**\n\n"

        for alert in data['alerts']:
            severity_emoji = {"critical": "🔴", "warning": "🟠", "info": "🔵"}.get(alert['severity'], "⚪")
            summary += f"---\n\n### {severity_emoji} {alert['product_name']}\n"
            summary += f"**Location:** {alert['location_name']}\n"
            summary += f"**Severity:** {alert['severity'].upper()}\n"
            if alert.get('metric_value') is not None:
                summary += f"**Current Stock:** {int(alert['metric_value'])} units (min: {int(alert['threshold_value'])})\n"
            summary += f"\n{alert['description']}\n\n"
            summary += f"**Action:** {alert['recommended_action']}\n\n"

        return summary
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_real_time_insights(location_id: str = None) -> str:
    """Get a comprehensive real-time overview of stock insights, performance, and alerts for a location or all locations."""
    try:
        # Fetch multiple data sources
        alerts_data = await shelfsense.get_alerts(location_id)
        inventory_data = await shelfsense.get_inventory_status(location_id)

        summary = f"# Real-Time Stock Insights\n\n"
        summary += f"*Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"

        # Alerts Overview
        summary += f"## 🚨 Alert Status\n"
        if alerts_data['critical_count'] > 0:
            summary += f"- **🔴 {alerts_data['critical_count']} CRITICAL** - Immediate action required!\n"
        if alerts_data['warning_count'] > 0:
            summary += f"- 🟠 {alerts_data['warning_count']} warnings\n"
        if alerts_data['info_count'] > 0:
            summary += f"- 🔵 {alerts_data['info_count']} informational\n"
        if alerts_data['total_alerts'] == 0:
            summary += "- ✅ No active alerts\n"

        # Inventory Health
        status_counts = {}
        for item in inventory_data:
            status = item["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        summary += f"\n## 📦 Inventory Health\n"
        status_emoji = {"critical": "🔴", "low": "🟠", "optimal": "🟢", "overstock": "🔵"}
        for status in ["critical", "low", "optimal", "overstock"]:
            if status in status_counts:
                summary += f"- {status_emoji[status]} {status.title()}: {status_counts[status]} items\n"

        # Critical items detail
        critical_items = [i for i in inventory_data if i['status'] == 'critical']
        if critical_items:
            summary += f"\n## ⚠️ Critical Stock Items\n"
            for item in critical_items[:5]:
                summary += f"- **{item['product_name']}** at {item['location_name']}: {item['current_stock']} units "
                if item.get('days_until_stockout'):
                    summary += f"({item['days_until_stockout']:.1f} days until stockout)\n"
                else:
                    summary += "\n"

        # Top critical alerts
        critical_alerts = [a for a in alerts_data['alerts'] if a['severity'] == 'critical']
        if critical_alerts:
            summary += f"\n## 🚨 Critical Actions Required\n"
            for alert in critical_alerts[:3]:
                summary += f"- **{alert['title']}**\n"
                summary += f"  → {alert['recommended_action']}\n"

        return summary
    except Exception as e:
        return f"Error: {str(e)}"


# ==================== SSE Transport Setup ====================

def create_sse_server(mcp_server: FastMCP):
    """Create a Starlette app that handles SSE connections for MCP"""
    transport = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server._mcp_server.run(
                streams[0], streams[1],
                mcp_server._mcp_server.create_initialization_options()
            )

    routes = [
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=transport.handle_post_message),
    ]

    return Starlette(routes=routes)


# Create FastAPI app
app = FastAPI(
    title="ShelfSense MCP Server",
    description="MCP server for ShelfSense inventory management - connects to ChatGPT via SSE",
    version="2.0.0"
)


@app.get("/")
async def root():
    """Root endpoint with server info"""
    return {
        "name": "ShelfSense MCP Server",
        "version": "2.0.0",
        "transport": "SSE",
        "sse_endpoint": "/sse",
        "api_backend": API_BASE_URL,
        "tools": [
            "get_locations",
            "get_pick_list",
            "get_all_pick_lists",
            "get_demand_forecast",
            "get_model_accuracy",
            "get_inventory_status",
            "get_analytics_summary",
            "explain_pick_quantity",
            "get_product_performance",
            "get_top_performers",
            "get_trends",
            "get_anomalies",
            "get_alerts",
            "get_critical_alerts",
            "get_stockout_risks",
            "get_real_time_insights"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_backend": API_BASE_URL
    }


# Mount the SSE server
app.mount("/", create_sse_server(mcp))


# ==================== Run Server ====================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
