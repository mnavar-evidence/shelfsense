"""Realistic sample data for ShelfSense Mock API"""
from datetime import datetime, timedelta
from models import (
    Product, Location, PickListItem, PickList, ModelAccuracy,
    InventoryStatus, DemandForecast, ForecastConfidence, AnalyticsSummary
)
import random


# Locations - Micromarkets at various venues
LOCATIONS = [
    Location(
        id="loc_westin_sf",
        name="Westin St. Francis - San Francisco",
        type="hotel",
        address="335 Powell St, San Francisco, CA 94102",
        contact="operations@westin-sf.com",
        capacity=1195,
        occupancy_rate=0.78
    ),
    Location(
        id="loc_marriott_nyc",
        name="Marriott Marquis - Times Square",
        type="hotel",
        address="1535 Broadway, New York, NY 10036",
        contact="inventory@marriott-marquis.com",
        capacity=1966,
        occupancy_rate=0.85
    ),
    Location(
        id="loc_hilton_chicago",
        name="Hilton Chicago O'Hare Airport",
        type="hotel",
        address="O'Hare International Airport, Chicago, IL 60666",
        contact="micromarket@hilton-ohare.com",
        capacity=858,
        occupancy_rate=0.72
    ),
    Location(
        id="loc_tech_campus_austin",
        name="TechCorp Campus - Austin",
        type="office",
        address="300 W 6th St, Austin, TX 78701",
        contact="facilities@techcorp.com",
        capacity=2500,
        occupancy_rate=0.65  # hybrid work
    ),
    Location(
        id="loc_hospital_boston",
        name="Boston Medical Center - Staff Lounge",
        type="hospital",
        address="1 Boston Medical Center Pl, Boston, MA 02118",
        contact="nutrition@bmc.org",
        capacity=None,
        occupancy_rate=0.95  # 24/7 operation
    ),
]


# Products - Typical micromarket items
PRODUCTS = [
    # Beverages
    Product(id="prod_coke_can", name="Coca-Cola Classic 12oz", category="Beverages", price=2.50, supplier="Coca-Cola Co"),
    Product(id="prod_pepsi_can", name="Pepsi 12oz", category="Beverages", price=2.50, supplier="PepsiCo"),
    Product(id="prod_water_bottle", name="Dasani Water 16.9oz", category="Beverages", price=2.00, supplier="Coca-Cola Co"),
    Product(id="prod_redbull", name="Red Bull Energy 8.4oz", category="Beverages", price=3.50, supplier="Red Bull GmbH"),
    Product(id="prod_coffee_cold", name="Starbucks Frappuccino 13.7oz", category="Beverages", price=4.25, supplier="Starbucks"),
    Product(id="prod_gatorade", name="Gatorade Fruit Punch 20oz", category="Beverages", price=2.75, supplier="PepsiCo"),
    Product(id="prod_orange_juice", name="Tropicana Orange Juice 14oz", category="Beverages", price=3.50, supplier="PepsiCo"),

    # Snacks
    Product(id="prod_lays_classic", name="Lay's Classic Chips 1.5oz", category="Snacks", price=1.75, supplier="Frito-Lay"),
    Product(id="prod_doritos", name="Doritos Nacho Cheese 1.75oz", category="Snacks", price=1.75, supplier="Frito-Lay"),
    Product(id="prod_pringles", name="Pringles Original 5.5oz", category="Snacks", price=3.25, supplier="Kellogg's"),
    Product(id="prod_snickers", name="Snickers Bar 1.86oz", category="Snacks", price=1.50, supplier="Mars Inc"),
    Product(id="prod_kind_bar", name="KIND Bar Almond & Coconut", category="Snacks", price=2.25, supplier="KIND LLC"),
    Product(id="prod_trail_mix", name="Nature Valley Trail Mix 1.2oz", category="Snacks", price=2.00, supplier="General Mills"),

    # Ready-to-eat meals
    Product(id="prod_sandwich_turkey", name="Turkey & Swiss Sandwich", category="Fresh Food", price=6.99, supplier="Local Deli"),
    Product(id="prod_salad_caesar", name="Caesar Salad Bowl", category="Fresh Food", price=7.50, supplier="Fresh Express"),
    Product(id="prod_yogurt_greek", name="Chobani Greek Yogurt 5.3oz", category="Fresh Food", price=2.25, supplier="Chobani"),
    Product(id="prod_fruit_cup", name="Fresh Fruit Cup 8oz", category="Fresh Food", price=4.50, supplier="Del Monte"),

    # Miscellaneous
    Product(id="prod_gum_mint", name="Extra Mint Gum", category="Miscellaneous", price=1.25, supplier="Mars Wrigley"),
    Product(id="prod_advil", name="Advil Pain Reliever 2-pack", category="Health", price=2.50, supplier="Pfizer"),
    Product(id="prod_hand_sanitizer", name="Purell Hand Sanitizer 2oz", category="Health", price=3.00, supplier="GOJO"),
]


def generate_pick_list(location_id: str, date_str: str) -> PickList:
    """Generate a realistic pick list for a location"""
    location = next((loc for loc in LOCATIONS if loc.id == location_id), LOCATIONS[0])

    # Select subset of products based on location type
    if location.type == "hotel":
        product_sample = random.sample(PRODUCTS, min(15, len(PRODUCTS)))
    elif location.type == "office":
        # Offices prefer snacks and coffee
        product_sample = [p for p in PRODUCTS if p.category in ["Beverages", "Snacks"]]
        product_sample = random.sample(product_sample, min(12, len(product_sample)))
    else:  # hospital
        # Hospitals need variety including healthy options
        product_sample = random.sample(PRODUCTS, min(18, len(PRODUCTS)))

    items = []
    for idx, product in enumerate(product_sample):
        # Generate realistic forecasts based on product category and location
        base_demand = random.randint(3, 15)
        if location.occupancy_rate:
            base_demand = int(base_demand * location.occupancy_rate)

        p10 = max(1, base_demand - random.randint(2, 4))
        p50 = base_demand
        p90 = base_demand + random.randint(2, 5)

        # Apply 30% bias for conservative stocking
        recommended = int(p50 * 1.3)

        current_stock = random.randint(0, 8)

        # Determine priority based on stock levels
        if current_stock <= 2:
            priority = "high"
        elif current_stock <= 5:
            priority = "medium"
        else:
            priority = "low"

        # Generate AI reason
        reasons = [
            f"Based on {location.occupancy_rate*100:.0f}% occupancy rate and historical trends",
            f"Accounts for weekend demand surge and {product.category.lower()} popularity",
            f"Seasonal adjustment applied, 3% shrinkage factored in",
            f"Stock level critical, preventing potential stockout",
            f"High confidence forecast based on 90-day historical accuracy",
        ]

        item = PickListItem(
            id=f"pick_{location_id}_{product.id}_{date_str}",
            product_id=product.id,
            product_name=product.name,
            location_id=location.id,
            location_name=location.name,
            current_stock=current_stock,
            forecast=ForecastConfidence(p10=p10, p50=p50, p90=p90),
            recommended_quantity=recommended,
            priority=priority,
            confidence_score=random.uniform(0.75, 0.95),
            reason=random.choice(reasons),
            last_restocked=datetime.now() - timedelta(days=random.randint(1, 5))
        )
        items.append(item)

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda x: priority_order[x.priority])

    return PickList(
        date=date_str,
        location_id=location.id,
        location_name=location.name,
        items=items,
        total_items=len(items),
        estimated_time_minutes=len(items) * 2 + 15,  # ~2 min per item + overhead
        status="pending"
    )


def generate_model_accuracy(product_id: str, location_id: str) -> ModelAccuracy:
    """Generate model accuracy metrics"""
    product = next((p for p in PRODUCTS if p.id == product_id), PRODUCTS[0])
    location = next((loc for loc in LOCATIONS if loc.id == location_id), LOCATIONS[0])

    # Hotels have better predictability
    if location.type == "hotel":
        accuracy = random.uniform(0.82, 0.94)
        mae = random.uniform(0.8, 2.5)
    elif location.type == "office":
        accuracy = random.uniform(0.70, 0.85)  # More variability with hybrid work
        mae = random.uniform(1.5, 3.5)
    else:
        accuracy = random.uniform(0.75, 0.88)
        mae = random.uniform(1.0, 3.0)

    return ModelAccuracy(
        product_id=product.id,
        product_name=product.name,
        location_id=location.id,
        location_name=location.name,
        accuracy_percentage=accuracy * 100,
        mae=mae,
        rmse=mae * 1.2,
        bias=random.uniform(-0.5, 0.5),
        samples_count=random.randint(30, 120),
        last_updated=datetime.now()
    )


def generate_inventory_status(product_id: str, location_id: str) -> InventoryStatus:
    """Generate current inventory status"""
    product = next((p for p in PRODUCTS if p.id == product_id), PRODUCTS[0])
    location = next((loc for loc in LOCATIONS if loc.id == location_id), LOCATIONS[0])

    min_stock = random.randint(3, 8)
    max_stock = min_stock + random.randint(10, 25)
    current = random.randint(0, max_stock + 5)

    if current < min_stock:
        status = "critical" if current < min_stock * 0.5 else "low"
        days_until_stockout = current / random.uniform(2, 5)
    elif current > max_stock:
        status = "overstock"
        days_until_stockout = None
    else:
        status = "optimal"
        days_until_stockout = None

    return InventoryStatus(
        product_id=product.id,
        product_name=product.name,
        location_id=location.id,
        location_name=location.name,
        current_stock=current,
        min_stock=min_stock,
        max_stock=max_stock,
        status=status,
        days_until_stockout=days_until_stockout
    )


def generate_demand_forecast(product_id: str, location_id: str, forecast_date: str) -> DemandForecast:
    """Generate demand forecast for a product"""
    product = next((p for p in PRODUCTS if p.id == product_id), PRODUCTS[0])
    location = next((loc for loc in LOCATIONS if loc.id == location_id), LOCATIONS[0])

    base_demand = random.randint(5, 20)

    # Factor in occupancy
    if location.occupancy_rate:
        base_demand = int(base_demand * location.occupancy_rate)

    factors = {
        "occupancy_rate": location.occupancy_rate or 0.8,
        "day_of_week": "Monday",  # Would be dynamic
        "weather_impact": random.choice(["neutral", "positive", "negative"]),
        "special_events": random.choice([None, "conference", "holiday"]),
        "seasonality_factor": round(random.uniform(0.9, 1.1), 2)
    }

    # Adjust for factors
    if factors["special_events"]:
        base_demand = int(base_demand * 1.2)

    p10 = max(1, base_demand - random.randint(2, 5))
    p50 = base_demand
    p90 = base_demand + random.randint(3, 7)

    return DemandForecast(
        product_id=product.id,
        product_name=product.name,
        location_id=location.id,
        location_name=location.name,
        forecast_date=forecast_date,
        forecast=ForecastConfidence(p10=p10, p50=p50, p90=p90),
        factors=factors,
        model_version="v2.1-lstm"
    )


def generate_analytics_summary() -> AnalyticsSummary:
    """Generate overall analytics summary"""
    return AnalyticsSummary(
        total_locations=len(LOCATIONS),
        total_products=len(PRODUCTS),
        avg_forecast_accuracy=86.5,
        total_picks_today=sum(random.randint(12, 18) for _ in LOCATIONS),
        stockout_risk_count=random.randint(5, 15),
        overstock_count=random.randint(3, 10),
        optimal_stock_count=random.randint(50, 80),
        top_selling_products=[
            {"product_name": "Coca-Cola Classic 12oz", "units_sold": 1250, "revenue": 3125.0},
            {"product_name": "Dasani Water 16.9oz", "units_sold": 1180, "revenue": 2360.0},
            {"product_name": "Snickers Bar 1.86oz", "units_sold": 890, "revenue": 1335.0},
        ],
        underperforming_locations=[
            {"location_name": "TechCorp Campus - Austin", "accuracy": 72.5, "reason": "Hybrid work variability"},
        ]
    )
