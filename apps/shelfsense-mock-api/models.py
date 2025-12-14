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
    demand: int = Field(description="Forecasted demand for the period")
    forecast: ForecastConfidence
    recommended_quantity: int
    priority: str  # high, medium, low
    confidence_score: float = Field(ge=0, le=1)
    stockout_cost: float = Field(description="Estimated cost of a stockout in dollars")
    ai_factors: List[str] = Field(default_factory=list, description="Drivers the AI considered")
    reason: Optional[str] = None  # AI explanation for the quantity
    last_restocked: Optional[datetime] = None
    last_updated: Optional[datetime] = None


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


class ProductPerformance(BaseModel):
    """Product performance analytics"""
    product_id: str
    product_name: str
    category: str
    location_id: Optional[str] = None
    location_name: Optional[str] = None
    # Sales metrics
    units_sold_7d: int = Field(description="Units sold in last 7 days")
    units_sold_30d: int = Field(description="Units sold in last 30 days")
    revenue_7d: float = Field(description="Revenue in last 7 days")
    revenue_30d: float = Field(description="Revenue in last 30 days")
    # Velocity metrics
    daily_velocity: float = Field(description="Average units sold per day")
    turnover_rate: float = Field(description="Inventory turnover rate (times per month)")
    days_of_supply: float = Field(description="Days until stockout at current velocity")
    # Performance indicators
    sell_through_rate: float = Field(description="Percentage of stock sold", ge=0, le=100)
    gross_margin: float = Field(description="Gross margin percentage", ge=0, le=100)
    performance_score: float = Field(description="Overall performance score 0-100", ge=0, le=100)
    performance_tier: str = Field(description="top_performer, average, underperformer, or slow_mover")


class TrendData(BaseModel):
    """Trend detection data"""
    product_id: str
    product_name: str
    location_id: Optional[str] = None
    location_name: Optional[str] = None
    # Trend metrics
    trend_direction: str = Field(description="increasing, decreasing, or stable")
    trend_strength: float = Field(description="Strength of trend 0-1", ge=0, le=1)
    week_over_week_change: float = Field(description="Percentage change from last week")
    month_over_month_change: float = Field(description="Percentage change from last month")
    # Seasonality
    seasonality_factor: float = Field(description="Current seasonal multiplier")
    is_seasonal_peak: bool = Field(description="Whether currently in seasonal peak")
    seasonal_pattern: Optional[str] = Field(description="weekly, monthly, or annual pattern")
    # Anomalies
    has_anomaly: bool = Field(description="Whether an anomaly was detected")
    anomaly_type: Optional[str] = Field(description="spike, drop, or unusual_pattern")
    anomaly_severity: Optional[str] = Field(description="low, medium, or high")
    anomaly_description: Optional[str] = None


class Alert(BaseModel):
    """System alert"""
    id: str
    alert_type: str = Field(description="stockout_risk, overstock, anomaly, trend_change, or performance")
    severity: str = Field(description="critical, warning, or info")
    title: str
    description: str
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    location_id: Optional[str] = None
    location_name: Optional[str] = None
    metric_value: Optional[float] = None
    threshold_value: Optional[float] = None
    recommended_action: str
    created_at: datetime
    is_acknowledged: bool = False


class AlertsSummary(BaseModel):
    """Summary of all active alerts"""
    total_alerts: int
    critical_count: int
    warning_count: int
    info_count: int
    alerts: List[Alert]
    locations_affected: int
    products_affected: int
