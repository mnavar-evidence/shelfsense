"""Data models for ShelfSense Mock API"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Product(BaseModel):
    """Product model"""
    id: str
    name: str
    category: str
    price: float
    unit: str = "each"
    supplier: Optional[str] = None


class Location(BaseModel):
    """Micromarket location model"""
    id: str
    name: str
    type: str  # hotel, office, airport, hospital
    address: str
    contact: Optional[str] = None
    capacity: Optional[int] = None  # e.g., hotel rooms
    occupancy_rate: Optional[float] = None  # percentage


class ForecastConfidence(BaseModel):
    """Forecast confidence intervals"""
    p10: float = Field(description="10th percentile (pessimistic)")
    p50: float = Field(description="50th percentile (median)")
    p90: float = Field(description="90th percentile (optimistic)")


class PickListItem(BaseModel):
    """Individual pick list item"""
    id: str
    product_id: str
    product_name: str
    location_id: str
    location_name: str
    current_stock: int
    forecast: ForecastConfidence
    recommended_quantity: int
    priority: str  # high, medium, low
    confidence_score: float = Field(ge=0, le=1)
    reason: Optional[str] = None  # AI explanation for the quantity
    last_restocked: Optional[datetime] = None


class PickList(BaseModel):
    """Complete pick list for a date"""
    date: str
    location_id: str
    location_name: str
    items: List[PickListItem]
    total_items: int
    estimated_time_minutes: int
    status: str = "pending"  # pending, in_progress, completed


class ModelAccuracy(BaseModel):
    """Model accuracy metrics for a product"""
    product_id: str
    product_name: str
    location_id: str
    location_name: str
    accuracy_percentage: float
    mae: float = Field(description="Mean Absolute Error")
    rmse: float = Field(description="Root Mean Squared Error")
    bias: float = Field(description="Average prediction bias")
    samples_count: int
    last_updated: datetime


class InventoryStatus(BaseModel):
    """Current inventory status"""
    product_id: str
    product_name: str
    location_id: str
    location_name: str
    current_stock: int
    min_stock: int
    max_stock: int
    status: str  # optimal, low, critical, overstock
    days_until_stockout: Optional[float] = None


class DemandForecast(BaseModel):
    """Demand forecast for a product at a location"""
    product_id: str
    product_name: str
    location_id: str
    location_name: str
    forecast_date: str
    forecast: ForecastConfidence
    factors: dict = Field(default_factory=dict, description="Contributing factors like occupancy, weather, events")
    model_version: str = "v2.1-lstm"


class AnalyticsSummary(BaseModel):
    """Analytics summary across locations"""
    total_locations: int
    total_products: int
    avg_forecast_accuracy: float
    total_picks_today: int
    stockout_risk_count: int
    overstock_count: int
    optimal_stock_count: int
    top_selling_products: List[dict]
    underperforming_locations: List[dict]
