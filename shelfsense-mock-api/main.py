"""ShelfSense Mock API Server - FastAPI Application"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn

from models import (
    Product, Location, PickList, ModelAccuracy,
    InventoryStatus, DemandForecast, AnalyticsSummary
)
from sample_data import (
    PRODUCTS, LOCATIONS,
    generate_pick_list, generate_model_accuracy,
    generate_inventory_status, generate_demand_forecast,
    generate_analytics_summary
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
    # Validate location exists
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


# ==================== Run Server ====================

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
