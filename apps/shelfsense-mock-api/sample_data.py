"""Realistic sample data for ShelfSense Mock API"""
from datetime import datetime, timedelta
from models import (
    Product, Location, PickListItem, PickList, ModelAccuracy,
    InventoryStatus, DemandForecast, ForecastConfidence, AnalyticsSummary,
    ProductPerformance, TrendData, Alert, AlertsSummary
)
import random
import hashlib


# Locations - Micromarkets at various venues
LOCATIONS = [
    Location(
        id="loc_usc_campus",
        name="USC Campus Center",
        type="office",
        address="3607 Trousdale Pkwy, Los Angeles, CA 90089",
        contact="operations@usc.edu",
        capacity=1200,
        occupancy_rate=0.82
    ),
    Location(
        id="loc_tech_campus",
        name="Tech Campus",
        type="office",
        address="1 Silicon Alley, Los Angeles, CA 90001",
        contact="facilities@techcampus.com",
        capacity=1500,
        occupancy_rate=0.78
    ),
    Location(
        id="loc_hotel_dena",
        name="Hotel Dena",
        type="hotel",
        address="303 Cordova St, Pasadena, CA 91101",
        contact="ops@hoteldena.com",
        capacity=500,
        occupancy_rate=0.89
    ),
    Location(
        id="loc_airport_terminal_b",
        name="Airport Terminal B",
        type="airport",
        address="1 World Way, Los Angeles, CA 90045",
        contact="terminalb@lawa.org",
        capacity=2500,
        occupancy_rate=0.76
    ),
    Location(
        id="loc_downtown_plaza",
        name="Downtown Plaza",
        type="retail",
        address="100 Market St, Los Angeles, CA 90012",
        contact="retail@downtownplaza.com",
        capacity=900,
        occupancy_rate=0.71
    ),
    Location(
        id="loc_medical_center",
        name="Medical Center",
        type="hospital",
        address="1200 N State St, Los Angeles, CA 90033",
        contact="nutrition@medcenter.org",
        capacity=600,
        occupancy_rate=0.95
    ),
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
    # UI demo items
    Product(id="prod_healthy_protein_bar", name="Healthy Protein Bar", category="Snacks", price=2.25, supplier="Protein Co"),
    Product(id="prod_coffee_to_go_premium", name="Coffee To-Go Premium", category="Beverages", price=3.50, supplier="Local Roastery"),
    Product(id="prod_pepsi_diet_20oz", name="Pepsi Diet 20oz", category="Beverages", price=2.75, supplier="PepsiCo"),
    Product(id="prod_monster_energy", name="Monster Energy", category="Beverages", price=3.15, supplier="Monster"),
    Product(id="prod_travel_snack_mix", name="Travel Snack Mix", category="Snacks", price=2.25, supplier="Travel Snacks"),
    Product(id="prod_coke_20oz", name="Coca-Cola 20oz", category="Beverages", price=2.75, supplier="Coca-Cola Co"),
    Product(id="prod_life_water_20oz", name="Life Water Premium 20oz", category="Beverages", price=2.75, supplier="PepsiCo"),
    Product(id="prod_starbucks_frappuccino", name="Starbucks Frappuccino", category="Beverages", price=4.25, supplier="Starbucks"),
    Product(id="prod_red_bull_energy", name="Red Bull Energy", category="Beverages", price=3.15, supplier="Red Bull"),
    Product(id="prod_gatorade_sports", name="Gatorade Sports", category="Beverages", price=2.75, supplier="PepsiCo"),
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

DEMO_PICK_ROWS = [
    {
        "location_id": "loc_usc_campus",
        "location_name": "USC Campus Center",
        "product_id": "prod_healthy_protein_bar",
        "product_name": "Healthy Protein Bar",
        "stock": 18,
        "demand": 22,
        "pick_qty": 4,
        "confidence": 0.79,
        "stockout_cost": 45,
        "ai_factors": ["Summer fitness focus (+10%)"],
        "updated_minutes_ago": 240,
        "priority": "medium",
    },
    {
        "location_id": "loc_usc_campus",
        "location_name": "USC Campus Center",
        "product_id": "prod_coffee_to_go_premium",
        "product_name": "Coffee To-Go Premium",
        "stock": 12,
        "demand": 28,
        "pick_qty": 16,
        "confidence": 0.85,
        "stockout_cost": 134,
        "ai_factors": ["Summer session: 30% enrollment (+8%)"],
        "updated_minutes_ago": 180,
        "priority": "medium",
    },
    {
        "location_id": "loc_hotel_dena",
        "location_name": "Hotel Dena",
        "product_id": "prod_pepsi_diet_20oz",
        "product_name": "Pepsi Diet 20oz",
        "stock": 12,
        "demand": 28,
        "pick_qty": 16,
        "confidence": 0.87,
        "stockout_cost": 95,
        "ai_factors": ["Business travelers prefer diet (+3%)"],
        "updated_minutes_ago": 180,
        "priority": "high",
    },
    {
        "location_id": "loc_tech_campus",
        "location_name": "Tech Campus",
        "product_id": "prod_monster_energy",
        "product_name": "Monster Energy",
        "stock": 24,
        "demand": 45,
        "pick_qty": 21,
        "confidence": 0.88,
        "stockout_cost": 156,
        "ai_factors": ["Summer coding bootcamp (+15%)"],
        "updated_minutes_ago": 45,
        "priority": "medium",
    },
    {
        "location_id": "loc_airport_terminal_b",
        "location_name": "Airport Terminal B",
        "product_id": "prod_travel_snack_mix",
        "product_name": "Travel Snack Mix",
        "stock": 5,
        "demand": 48,
        "pick_qty": 43,
        "confidence": 0.89,
        "stockout_cost": 356,
        "ai_factors": ["Summer vacation surge (+35%)"],
        "updated_minutes_ago": 15,
        "priority": "medium",
    },
    {
        "location_id": "loc_hotel_dena",
        "location_name": "Hotel Dena",
        "product_id": "prod_snickers",
        "product_name": "Snickers Bar",
        "stock": 15,
        "demand": 42,
        "pick_qty": 27,
        "confidence": 0.91,
        "stockout_cost": 67,
        "ai_factors": ["Checkout impulse buying (+15%)"],
        "updated_minutes_ago": 60,
        "priority": "high",
    },
    {
        "location_id": "loc_tech_campus",
        "location_name": "Tech Campus",
        "product_id": "prod_coke_20oz",
        "product_name": "Coca-Cola 20oz",
        "stock": 16,
        "demand": 38,
        "pick_qty": 22,
        "confidence": 0.91,
        "stockout_cost": 89,
        "ai_factors": ["Cafeteria partnership (+10%)"],
        "updated_minutes_ago": 60,
        "priority": "medium",
    },
    {
        "location_id": "loc_hotel_dena",
        "location_name": "Hotel Dena",
        "product_id": "prod_life_water_20oz",
        "product_name": "Life Water Premium 20oz",
        "stock": 8,
        "demand": 32,
        "pick_qty": 24,
        "confidence": 0.92,
        "stockout_cost": 180,
        "ai_factors": ["Hotel: 89% occupancy (+12%)"],
        "updated_minutes_ago": 120,
        "priority": "high",
    },
    {
        "location_id": "loc_downtown_plaza",
        "location_name": "Downtown Plaza",
        "product_id": "prod_starbucks_frappuccino",
        "product_name": "Starbucks Frappuccino",
        "stock": 8,
        "demand": 52,
        "pick_qty": 44,
        "confidence": 0.93,
        "stockout_cost": 298,
        "ai_factors": ["Office workers: 85% occupancy (+15%)"],
        "updated_minutes_ago": 20,
        "priority": "low",
    },
    {
        "location_id": "loc_hotel_dena",
        "location_name": "Hotel Dena",
        "product_id": "prod_red_bull_energy",
        "product_name": "Red Bull Energy",
        "stock": 6,
        "demand": 35,
        "pick_qty": 29,
        "confidence": 0.94,
        "stockout_cost": 245,
        "ai_factors": ["Business meetings surge (+20%)"],
        "updated_minutes_ago": 30,
        "priority": "high",
    },
    {
        "location_id": "loc_medical_center",
        "location_name": "Medical Center",
        "product_id": "prod_gatorade_sports",
        "product_name": "Gatorade Sports",
        "stock": 18,
        "demand": 41,
        "pick_qty": 23,
        "confidence": 0.96,
        "stockout_cost": 187,
        "ai_factors": ["Summer heat increasing dehydration cases (+18%)"],
        "updated_minutes_ago": 15,
        "priority": "high",
    },
]


def generate_pick_list(location_id: str, date_str: str) -> PickList:
    """Generate a realistic pick list for a location"""
    location = next((loc for loc in LOCATIONS if loc.id == location_id), LOCATIONS[0])

    # If "all" or a known demo location, return the curated UI-aligned rows
    demo_rows = (
        DEMO_PICK_ROWS
        if location_id == "all"
        else [row for row in DEMO_PICK_ROWS if row["location_id"] == location_id]
    )

    items: list[PickListItem] = []
    if demo_rows:
        for idx, row in enumerate(demo_rows):
            product = next((p for p in PRODUCTS if p.id == row["product_id"]), None)
            p50 = row["demand"]
            p10 = max(1, int(p50 * 0.7))
            p90 = int(p50 * 1.2)
            last_updated = datetime.now() - timedelta(minutes=row["updated_minutes_ago"])

            items.append(
                PickListItem(
                    id=f"pick_{row['location_id']}_{row['product_id']}_{date_str}_{idx}",
                    product_id=row["product_id"],
                    product_name=row["product_name"],
                    location_id=row["location_id"],
                    location_name=row["location_name"],
                    current_stock=row["stock"],
                    demand=row["demand"],
                    forecast=ForecastConfidence(p10=p10, p50=p50, p90=p90),
                    recommended_quantity=row["pick_qty"],
                    priority=row["priority"],
                    confidence_score=row["confidence"],
                    stockout_cost=row["stockout_cost"],
                    ai_factors=row["ai_factors"],
                    reason=row["ai_factors"][0],
                    last_restocked=last_updated - timedelta(days=1),
                    last_updated=last_updated,
                )
            )

        location_name = "All Locations" if location_id == "all" else demo_rows[0]["location_name"]
        return PickList(
            date=date_str,
            location_id=location_id,
            location_name=location_name,
            items=items,
            total_items=len(items),
            estimated_time_minutes=len(items) * 2 + 15,
            status="pending",
        )

    # Otherwise fall back to synthetic generation with richer fields
    if location.type == "hotel":
        product_sample = random.sample(PRODUCTS, min(15, len(PRODUCTS)))
    elif location.type == "office":
        product_sample = [p for p in PRODUCTS if p.category in ["Beverages", "Snacks"]]
        product_sample = random.sample(product_sample, min(12, len(product_sample)))
    else:
        product_sample = random.sample(PRODUCTS, min(18, len(PRODUCTS)))

    reasons = [
        "Based on occupancy rate and historical trends",
        "Weekend demand surge and category popularity",
        "Seasonal adjustment with shrinkage factored in",
        "Critical stock level, preventing potential stockout",
        "High confidence forecast from 90-day accuracy",
    ]

    for idx, product in enumerate(product_sample):
        base_demand = random.randint(3, 15)
        if location.occupancy_rate:
            base_demand = int(base_demand * location.occupancy_rate)

        p10 = max(1, base_demand - random.randint(2, 4))
        p50 = base_demand
        p90 = base_demand + random.randint(2, 5)
        recommended = int(p50 * 1.3)
        current_stock = random.randint(0, 8)

        if current_stock <= 2:
            priority = "high"
        elif current_stock <= 5:
            priority = "medium"
        else:
            priority = "low"

        last_updated = datetime.now() - timedelta(minutes=random.randint(5, 240))
        factor = random.choice(reasons)
        ai_factor_list = [factor]

        items.append(
            PickListItem(
                id=f"pick_{location_id}_{product.id}_{date_str}_{idx}",
                product_id=product.id,
                product_name=product.name,
                location_id=location.id,
                location_name=location.name,
                current_stock=current_stock,
                demand=p50,
                forecast=ForecastConfidence(p10=p10, p50=p50, p90=p90),
                recommended_quantity=recommended,
                priority=priority,
                confidence_score=random.uniform(0.75, 0.95),
                stockout_cost=round(recommended * (product.price or 2.0) * 0.9, 2),
                ai_factors=ai_factor_list,
                reason=factor,
                last_restocked=datetime.now() - timedelta(days=random.randint(1, 5)),
                last_updated=last_updated,
            )
        )

    priority_order = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda x: priority_order[x.priority])

    return PickList(
        date=date_str,
        location_id=location.id,
        location_name=location.name,
        items=items,
        total_items=len(items),
        estimated_time_minutes=len(items) * 2 + 15,
        status="pending",
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


def generate_product_performance(product_id: str, location_id: str = None) -> ProductPerformance:
    """Generate product performance analytics"""
    product = next((p for p in PRODUCTS if p.id == product_id), PRODUCTS[0])
    location = next((loc for loc in LOCATIONS if loc.id == location_id), None) if location_id else None

    # Base metrics vary by category
    category_multipliers = {
        "Beverages": {"velocity": 1.5, "margin": 0.35},
        "Snacks": {"velocity": 1.2, "margin": 0.40},
        "Fresh Food": {"velocity": 0.8, "margin": 0.45},
        "Health": {"velocity": 0.5, "margin": 0.50},
        "Miscellaneous": {"velocity": 0.6, "margin": 0.38},
    }

    multiplier = category_multipliers.get(product.category, {"velocity": 1.0, "margin": 0.35})

    # Generate realistic sales data
    base_daily = random.uniform(3, 12) * multiplier["velocity"]
    if location and location.occupancy_rate:
        base_daily *= location.occupancy_rate

    units_7d = int(base_daily * 7 * random.uniform(0.85, 1.15))
    units_30d = int(base_daily * 30 * random.uniform(0.9, 1.1))

    revenue_7d = round(units_7d * product.price, 2)
    revenue_30d = round(units_30d * product.price, 2)

    daily_velocity = round(units_30d / 30, 2)
    current_stock = random.randint(5, 30)
    days_of_supply = round(current_stock / max(daily_velocity, 0.1), 1)

    # Turnover = units sold / average inventory
    avg_inventory = random.randint(15, 40)
    turnover_rate = round((units_30d / max(avg_inventory, 1)), 2)

    # Performance scoring
    sell_through = min(100, round((units_30d / max(avg_inventory * 30 / 7, 1)) * 100, 1))
    gross_margin = round(multiplier["margin"] * 100 * random.uniform(0.9, 1.1), 1)

    # Calculate performance score (weighted: velocity 30%, margin 25%, turnover 25%, sell-through 20%)
    velocity_score = min(100, (daily_velocity / 10) * 100)
    turnover_score = min(100, (turnover_rate / 4) * 100)
    performance_score = round(
        velocity_score * 0.30 +
        gross_margin * 0.25 +
        turnover_score * 0.25 +
        sell_through * 0.20,
        1
    )

    # Determine tier
    if performance_score >= 75:
        tier = "top_performer"
    elif performance_score >= 50:
        tier = "average"
    elif performance_score >= 30:
        tier = "underperformer"
    else:
        tier = "slow_mover"

    return ProductPerformance(
        product_id=product.id,
        product_name=product.name,
        category=product.category,
        location_id=location.id if location else None,
        location_name=location.name if location else None,
        units_sold_7d=units_7d,
        units_sold_30d=units_30d,
        revenue_7d=revenue_7d,
        revenue_30d=revenue_30d,
        daily_velocity=daily_velocity,
        turnover_rate=turnover_rate,
        days_of_supply=days_of_supply,
        sell_through_rate=sell_through,
        gross_margin=gross_margin,
        performance_score=performance_score,
        performance_tier=tier
    )


def generate_trend_data(product_id: str, location_id: str = None) -> TrendData:
    """Generate trend detection data for a product"""
    product = next((p for p in PRODUCTS if p.id == product_id), PRODUCTS[0])
    location = next((loc for loc in LOCATIONS if loc.id == location_id), None) if location_id else None

    # Generate trend direction and strength
    trend_roll = random.random()
    if trend_roll < 0.3:
        trend_direction = "increasing"
        wow_change = random.uniform(5, 25)
        mom_change = random.uniform(10, 40)
    elif trend_roll < 0.6:
        trend_direction = "decreasing"
        wow_change = random.uniform(-25, -5)
        mom_change = random.uniform(-35, -10)
    else:
        trend_direction = "stable"
        wow_change = random.uniform(-5, 5)
        mom_change = random.uniform(-8, 8)

    trend_strength = abs(wow_change) / 30  # Normalize to 0-1

    # Seasonality
    month = datetime.now().month
    # Summer months have higher beverage sales
    if product.category == "Beverages" and month in [6, 7, 8]:
        seasonality_factor = random.uniform(1.15, 1.35)
        is_seasonal_peak = True
        seasonal_pattern = "annual"
    # Snacks peak on weekends
    elif product.category == "Snacks":
        seasonality_factor = random.uniform(1.05, 1.20)
        is_seasonal_peak = datetime.now().weekday() >= 4
        seasonal_pattern = "weekly"
    else:
        seasonality_factor = random.uniform(0.95, 1.05)
        is_seasonal_peak = False
        seasonal_pattern = None

    # Anomaly detection (10% chance of anomaly)
    has_anomaly = random.random() < 0.10
    anomaly_type = None
    anomaly_severity = None
    anomaly_description = None

    if has_anomaly:
        anomaly_type = random.choice(["spike", "drop", "unusual_pattern"])
        anomaly_severity = random.choice(["low", "medium", "high"])

        if anomaly_type == "spike":
            anomaly_description = f"Unusual demand spike detected - {random.randint(40, 80)}% above normal"
        elif anomaly_type == "drop":
            anomaly_description = f"Unexpected demand drop - {random.randint(30, 60)}% below normal"
        else:
            anomaly_description = "Irregular sales pattern detected over the past 48 hours"

    return TrendData(
        product_id=product.id,
        product_name=product.name,
        location_id=location.id if location else None,
        location_name=location.name if location else None,
        trend_direction=trend_direction,
        trend_strength=round(trend_strength, 3),
        week_over_week_change=round(wow_change, 1),
        month_over_month_change=round(mom_change, 1),
        seasonality_factor=round(seasonality_factor, 2),
        is_seasonal_peak=is_seasonal_peak,
        seasonal_pattern=seasonal_pattern,
        has_anomaly=has_anomaly,
        anomaly_type=anomaly_type,
        anomaly_severity=anomaly_severity,
        anomaly_description=anomaly_description
    )


def generate_alerts(location_id: str = None, alert_type: str = None, severity: str = None) -> AlertsSummary:
    """Generate system alerts"""
    alerts = []
    now = datetime.now()

    # Pre-defined realistic alerts
    alert_templates = [
        # Stockout risks
        {
            "alert_type": "stockout_risk",
            "severity": "critical",
            "title": "Critical: Coca-Cola 20oz stockout imminent",
            "description": "Stock will be depleted within 4 hours at current sales velocity. Immediate restocking required.",
            "product_id": "prod_coke_20oz",
            "product_name": "Coca-Cola 20oz",
            "location_id": "loc_hotel_dena",
            "location_name": "Hotel Dena",
            "metric_value": 2,
            "threshold_value": 5,
            "recommended_action": "Add 24 units to today's pick list immediately"
        },
        {
            "alert_type": "stockout_risk",
            "severity": "critical",
            "title": "Critical: Red Bull Energy at 0 stock",
            "description": "Product is currently out of stock. Lost sales estimated at $47/hour.",
            "product_id": "prod_red_bull_energy",
            "product_name": "Red Bull Energy",
            "location_id": "loc_airport_terminal_b",
            "location_name": "Airport Terminal B",
            "metric_value": 0,
            "threshold_value": 8,
            "recommended_action": "Emergency restock - add 36 units"
        },
        {
            "alert_type": "stockout_risk",
            "severity": "warning",
            "title": "Low stock: Snickers Bar",
            "description": "Stock level at 3 units, below minimum threshold of 10. Estimated 6 hours until stockout.",
            "product_id": "prod_snickers",
            "product_name": "Snickers Bar",
            "location_id": "loc_tech_campus",
            "location_name": "Tech Campus",
            "metric_value": 3,
            "threshold_value": 10,
            "recommended_action": "Include in next scheduled pick list with 20 units"
        },
        # Overstock alerts
        {
            "alert_type": "overstock",
            "severity": "warning",
            "title": "Overstock: Greek Yogurt approaching expiration",
            "description": "28 units in stock, only 5 units sold in past 7 days. Product expires in 4 days.",
            "product_id": "prod_yogurt_greek",
            "product_name": "Chobani Greek Yogurt 5.3oz",
            "location_id": "loc_tech_campus_austin",
            "location_name": "TechCorp Campus - Austin",
            "metric_value": 28,
            "threshold_value": 15,
            "recommended_action": "Consider markdown pricing or transfer to higher-velocity location"
        },
        {
            "alert_type": "overstock",
            "severity": "info",
            "title": "Excess inventory: Dasani Water",
            "description": "Stock level 45 units, 15 above optimal. 12 days of supply at current velocity.",
            "product_id": "prod_water_bottle",
            "product_name": "Dasani Water 16.9oz",
            "location_id": "loc_hilton_chicago",
            "location_name": "Hilton Chicago O'Hare Airport",
            "metric_value": 45,
            "threshold_value": 30,
            "recommended_action": "Skip this product in next 2 restocking cycles"
        },
        # Anomaly alerts
        {
            "alert_type": "anomaly",
            "severity": "warning",
            "title": "Demand spike: Monster Energy +85%",
            "description": "Unusual demand increase detected. Sales 85% above 7-day average, possibly due to nearby event.",
            "product_id": "prod_monster_energy",
            "product_name": "Monster Energy",
            "location_id": "loc_usc_campus",
            "location_name": "USC Campus Center",
            "metric_value": 85,
            "threshold_value": 50,
            "recommended_action": "Increase pick quantity by 50% for next 3 days"
        },
        {
            "alert_type": "anomaly",
            "severity": "info",
            "title": "Sales pattern change: Coffee sales shifting earlier",
            "description": "Peak coffee sales shifted from 9-10 AM to 7-8 AM over past week.",
            "product_id": "prod_coffee_to_go_premium",
            "product_name": "Coffee To-Go Premium",
            "location_id": "loc_marriott_nyc",
            "location_name": "Marriott Marquis - Times Square",
            "metric_value": None,
            "threshold_value": None,
            "recommended_action": "Adjust restocking schedule to ensure morning availability"
        },
        # Trend alerts
        {
            "alert_type": "trend_change",
            "severity": "info",
            "title": "Upward trend: Healthy Protein Bar +22% WoW",
            "description": "Consistent demand increase over past 3 weeks. Fitness season driving sales.",
            "product_id": "prod_healthy_protein_bar",
            "product_name": "Healthy Protein Bar",
            "location_id": "loc_medical_center",
            "location_name": "Medical Center",
            "metric_value": 22,
            "threshold_value": 15,
            "recommended_action": "Increase baseline stock level from 15 to 22 units"
        },
        {
            "alert_type": "trend_change",
            "severity": "warning",
            "title": "Declining trend: Pringles -18% MoM",
            "description": "Month-over-month decline in sales. May indicate preference shift or quality issue.",
            "product_id": "prod_pringles",
            "product_name": "Pringles Original 5.5oz",
            "location_id": "loc_downtown_plaza",
            "location_name": "Downtown Plaza",
            "metric_value": -18,
            "threshold_value": -15,
            "recommended_action": "Review customer feedback and consider product placement optimization"
        },
        # Performance alerts
        {
            "alert_type": "performance",
            "severity": "warning",
            "title": "Underperforming: Fresh Fruit Cup",
            "description": "Performance score 28/100. Low velocity (0.8/day) and high spoilage rate (12%).",
            "product_id": "prod_fruit_cup",
            "product_name": "Fresh Fruit Cup 8oz",
            "location_id": "loc_hilton_chicago",
            "location_name": "Hilton Chicago O'Hare Airport",
            "metric_value": 28,
            "threshold_value": 40,
            "recommended_action": "Reduce stock levels or discontinue at this location"
        },
        {
            "alert_type": "performance",
            "severity": "info",
            "title": "Top performer: Starbucks Frappuccino",
            "description": "Performance score 92/100. Highest revenue per square foot in beverage category.",
            "product_id": "prod_starbucks_frappuccino",
            "product_name": "Starbucks Frappuccino",
            "location_id": "loc_westin_sf",
            "location_name": "Westin St. Francis - San Francisco",
            "metric_value": 92,
            "threshold_value": 80,
            "recommended_action": "Consider expanding facings and ensuring consistent availability"
        },
    ]

    # Filter and create alerts
    for idx, template in enumerate(alert_templates):
        # Apply filters
        if location_id and template["location_id"] != location_id:
            continue
        if alert_type and template["alert_type"] != alert_type:
            continue
        if severity and template["severity"] != severity:
            continue

        # Generate unique ID
        alert_id = hashlib.md5(f"{template['title']}_{template['location_id']}".encode()).hexdigest()[:12]

        alerts.append(Alert(
            id=f"alert_{alert_id}",
            alert_type=template["alert_type"],
            severity=template["severity"],
            title=template["title"],
            description=template["description"],
            product_id=template["product_id"],
            product_name=template["product_name"],
            location_id=template["location_id"],
            location_name=template["location_name"],
            metric_value=template["metric_value"],
            threshold_value=template["threshold_value"],
            recommended_action=template["recommended_action"],
            created_at=now - timedelta(minutes=random.randint(5, 180)),
            is_acknowledged=False
        ))

    # Sort by severity (critical first)
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    alerts.sort(key=lambda x: severity_order[x.severity])

    # Calculate summary stats
    critical_count = sum(1 for a in alerts if a.severity == "critical")
    warning_count = sum(1 for a in alerts if a.severity == "warning")
    info_count = sum(1 for a in alerts if a.severity == "info")
    locations_affected = len(set(a.location_id for a in alerts if a.location_id))
    products_affected = len(set(a.product_id for a in alerts if a.product_id))

    return AlertsSummary(
        total_alerts=len(alerts),
        critical_count=critical_count,
        warning_count=warning_count,
        info_count=info_count,
        alerts=alerts,
        locations_affected=locations_affected,
        products_affected=products_affected
    )
