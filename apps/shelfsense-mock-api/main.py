"""ShelfSense Mock API Server - FastAPI Application"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn

from models import (
    Product, Location, PickList, ModelAccuracy,
    InventoryStatus, DemandForecast, AnalyticsSummary,
    ProductPerformance, TrendData, AlertsSummary
)
from sample_data import (
    PRODUCTS, LOCATIONS,
    generate_pick_list, generate_model_accuracy,
    generate_inventory_status, generate_demand_forecast,
    generate_analytics_summary, generate_product_performance,
    generate_trend_data, generate_alerts
)


app = FastAPI(
    title="ShelfSense Mock API",
    description="Mock API server for ShelfSense micromarket inventory management",
    version="1.0.0",
)

# Enable CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "ShelfSense Mock API",
        "version": "1.0.0",
        "endpoints": {
            "locations": "/api/locations",
            "products": "/api/products",
            "pick_list": "/api/pick-list",
            "model_accuracy": "/api/models/product-accuracy",
            "inventory_status": "/api/inventory/status",
            "demand_forecast": "/api/forecast/demand",
            "analytics": "/api/analytics/summary"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ==================== Locations ====================

@app.get("/api/locations", response_model=List[Location])
async def get_locations(
    location_type: Optional[str] = Query(None, description="Filter by type: hotel, office, airport, hospital")
):
    """Get all micromarket locations"""
    if location_type:
        filtered = [loc for loc in LOCATIONS if loc.type == location_type]
        return filtered
    return LOCATIONS


@app.get("/api/locations/{location_id}", response_model=Location)
async def get_location(location_id: str):
    """Get a specific location by ID"""
    location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location {location_id} not found")
    return location


# ==================== Products ====================

@app.get("/api/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Get all products"""
    if category:
        filtered = [prod for prod in PRODUCTS if prod.category.lower() == category.lower()]
        return filtered
    return PRODUCTS


@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    product = next((prod for prod in PRODUCTS if prod.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


# ==================== Pick Lists ====================

@app.get("/api/pick-list", response_model=PickList)
async def get_pick_list(
    location_id: str = Query(..., description="Location ID"),
    date: Optional[str] = Query(None, description="Date (YYYY-MM-DD), defaults to today")
):
    """Get pick list for a specific location and date"""
    # Validate location exists unless using the aggregate "all" view
    if location_id != "all":
        location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")

    # Use today if no date provided
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Generate pick list
    pick_list = generate_pick_list(location_id, date)
    return pick_list


@app.get("/api/pick-list/all", response_model=List[PickList])
async def get_all_pick_lists(
    date: Optional[str] = Query(None, description="Date (YYYY-MM-DD), defaults to today")
):
    """Get pick lists for all locations"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    pick_lists = [generate_pick_list(loc.id, date) for loc in LOCATIONS]
    return pick_lists


# ==================== Model Accuracy ====================

@app.get("/api/models/product-accuracy", response_model=List[ModelAccuracy])
async def get_model_accuracy(
    location_id: Optional[str] = Query(None, description="Filter by location"),
    product_id: Optional[str] = Query(None, description="Filter by product")
):
    """Get model accuracy metrics"""
    results = []

    if product_id and location_id:
        # Specific product at specific location
        results.append(generate_model_accuracy(product_id, location_id))
    elif product_id:
        # Product across all locations
        for loc in LOCATIONS:
            results.append(generate_model_accuracy(product_id, loc.id))
    elif location_id:
        # All products at a location
        for prod in PRODUCTS[:10]:  # Limit to 10 for performance
            results.append(generate_model_accuracy(prod.id, location_id))
    else:
        # Overall summary - sample products at sample locations
        import random
        sample_combos = [(random.choice(PRODUCTS).id, random.choice(LOCATIONS).id) for _ in range(15)]
        for prod_id, loc_id in sample_combos:
            results.append(generate_model_accuracy(prod_id, loc_id))

    return results


# ==================== Inventory Status ====================

@app.get("/api/inventory/status", response_model=List[InventoryStatus])
async def get_inventory_status(
    location_id: Optional[str] = Query(None, description="Filter by location"),
    status_filter: Optional[str] = Query(None, description="Filter by status: optimal, low, critical, overstock")
):
    """Get current inventory status"""
    results = []

    if location_id:
        # All products at a location
        location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")

        for prod in PRODUCTS:
            inv_status = generate_inventory_status(prod.id, location_id)
            if not status_filter or inv_status.status == status_filter:
                results.append(inv_status)
    else:
        # Sample across all locations
        import random
        sample_combos = [(random.choice(PRODUCTS).id, random.choice(LOCATIONS).id) for _ in range(20)]
        for prod_id, loc_id in sample_combos:
            inv_status = generate_inventory_status(prod_id, loc_id)
            if not status_filter or inv_status.status == status_filter:
                results.append(inv_status)

    return results


# ==================== Demand Forecasting ====================

@app.get("/api/forecast/demand", response_model=List[DemandForecast])
async def get_demand_forecast(
    location_id: str = Query(..., description="Location ID"),
    product_id: Optional[str] = Query(None, description="Product ID (optional, returns all if not specified)"),
    forecast_date: Optional[str] = Query(None, description="Forecast date (YYYY-MM-DD), defaults to tomorrow")
):
    """Get demand forecast for products at a location"""
    # Validate location
    location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location {location_id} not found")

    # Default to tomorrow
    if not forecast_date:
        forecast_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    results = []

    if product_id:
        # Specific product
        product = next((prod for prod in PRODUCTS if prod.id == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        results.append(generate_demand_forecast(product_id, location_id, forecast_date))
    else:
        # All products at location
        for prod in PRODUCTS:
            results.append(generate_demand_forecast(prod.id, location_id, forecast_date))

    return results


# ==================== Analytics ====================

@app.get("/api/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary():
    """Get overall analytics summary across all locations"""
    return generate_analytics_summary()


# ==================== Product Performance ====================

@app.get("/api/analytics/product-performance", response_model=List[ProductPerformance])
async def get_product_performance(
    location_id: Optional[str] = Query(None, description="Filter by location"),
    product_id: Optional[str] = Query(None, description="Filter by product"),
    category: Optional[str] = Query(None, description="Filter by category"),
    performance_tier: Optional[str] = Query(None, description="Filter by tier: top_performer, average, underperformer, slow_mover")
):
    """Get product performance analytics including sales velocity, turnover, and performance scores"""
    results = []

    if product_id:
        # Specific product
        product = next((p for p in PRODUCTS if p.id == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        if location_id:
            # Specific product at specific location
            location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
            if not location:
                raise HTTPException(status_code=404, detail=f"Location {location_id} not found")
            results.append(generate_product_performance(product_id, location_id))
        else:
            # Product across all locations
            for loc in LOCATIONS:
                results.append(generate_product_performance(product_id, loc.id))
    elif location_id:
        # All products at a location
        location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")

        products_to_query = PRODUCTS
        if category:
            products_to_query = [p for p in PRODUCTS if p.category.lower() == category.lower()]

        for prod in products_to_query:
            perf = generate_product_performance(prod.id, location_id)
            if not performance_tier or perf.performance_tier == performance_tier:
                results.append(perf)
    else:
        # Sample across all - top products at random locations
        import random
        products_to_query = PRODUCTS
        if category:
            products_to_query = [p for p in PRODUCTS if p.category.lower() == category.lower()]

        sample_combos = [(p.id, random.choice(LOCATIONS).id) for p in products_to_query[:15]]
        for prod_id, loc_id in sample_combos:
            perf = generate_product_performance(prod_id, loc_id)
            if not performance_tier or perf.performance_tier == performance_tier:
                results.append(perf)

    # Sort by performance score descending
    results.sort(key=lambda x: x.performance_score, reverse=True)
    return results


@app.get("/api/analytics/top-performers", response_model=List[ProductPerformance])
async def get_top_performers(
    location_id: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(10, description="Number of top performers to return", ge=1, le=50)
):
    """Get top performing products by performance score"""
    results = []

    if location_id:
        location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")

        for prod in PRODUCTS:
            results.append(generate_product_performance(prod.id, location_id))
    else:
        import random
        for prod in PRODUCTS:
            loc = random.choice(LOCATIONS)
            results.append(generate_product_performance(prod.id, loc.id))

    # Sort by performance score and return top N
    results.sort(key=lambda x: x.performance_score, reverse=True)
    return results[:limit]


# ==================== Trend Detection ====================

@app.get("/api/analytics/trends", response_model=List[TrendData])
async def get_trends(
    location_id: Optional[str] = Query(None, description="Filter by location"),
    product_id: Optional[str] = Query(None, description="Filter by product"),
    trend_direction: Optional[str] = Query(None, description="Filter by direction: increasing, decreasing, stable"),
    has_anomaly: Optional[bool] = Query(None, description="Filter for products with anomalies")
):
    """Get trend detection data including week-over-week changes, seasonality, and anomalies"""
    results = []

    if product_id:
        # Specific product
        product = next((p for p in PRODUCTS if p.id == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        if location_id:
            results.append(generate_trend_data(product_id, location_id))
        else:
            for loc in LOCATIONS:
                results.append(generate_trend_data(product_id, loc.id))
    elif location_id:
        # All products at a location
        location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")

        for prod in PRODUCTS:
            results.append(generate_trend_data(prod.id, location_id))
    else:
        # Sample across all
        import random
        sample_combos = [(p.id, random.choice(LOCATIONS).id) for p in PRODUCTS[:20]]
        for prod_id, loc_id in sample_combos:
            results.append(generate_trend_data(prod_id, loc_id))

    # Apply filters
    if trend_direction:
        results = [r for r in results if r.trend_direction == trend_direction]
    if has_anomaly is not None:
        results = [r for r in results if r.has_anomaly == has_anomaly]

    # Sort by trend strength descending
    results.sort(key=lambda x: x.trend_strength, reverse=True)
    return results


@app.get("/api/analytics/anomalies", response_model=List[TrendData])
async def get_anomalies(
    location_id: Optional[str] = Query(None, description="Filter by location"),
    severity: Optional[str] = Query(None, description="Filter by severity: low, medium, high")
):
    """Get products with detected anomalies"""
    results = []

    if location_id:
        location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")
        products_locs = [(p.id, location_id) for p in PRODUCTS]
    else:
        import random
        products_locs = [(p.id, random.choice(LOCATIONS).id) for p in PRODUCTS]

    for prod_id, loc_id in products_locs:
        trend = generate_trend_data(prod_id, loc_id)
        if trend.has_anomaly:
            if not severity or trend.anomaly_severity == severity:
                results.append(trend)

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    results.sort(key=lambda x: severity_order.get(x.anomaly_severity, 3))
    return results


# ==================== Alerts ====================

@app.get("/api/alerts", response_model=AlertsSummary)
async def get_alerts(
    location_id: Optional[str] = Query(None, description="Filter by location"),
    alert_type: Optional[str] = Query(None, description="Filter by type: stockout_risk, overstock, anomaly, trend_change, performance"),
    severity: Optional[str] = Query(None, description="Filter by severity: critical, warning, info")
):
    """Get system alerts for stockouts, overstocks, anomalies, trends, and performance issues"""
    if location_id:
        location = next((loc for loc in LOCATIONS if loc.id == location_id), None)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")

    return generate_alerts(location_id, alert_type, severity)


@app.get("/api/alerts/critical", response_model=AlertsSummary)
async def get_critical_alerts(
    location_id: Optional[str] = Query(None, description="Filter by location")
):
    """Get only critical severity alerts requiring immediate attention"""
    return generate_alerts(location_id, severity="critical")


@app.get("/api/alerts/stockout-risks", response_model=AlertsSummary)
async def get_stockout_alerts(
    location_id: Optional[str] = Query(None, description="Filter by location")
):
    """Get alerts for products at risk of stockout"""
    return generate_alerts(location_id, alert_type="stockout_risk")


# ==================== Run Server ====================

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
