# ShelfSense Mock API Server

FastAPI-based mock server that simulates the ShelfSense micromarket inventory management backend.

## Features

- **Realistic sample data** for hotels, offices, airports, and hospitals
- **Complete REST API** matching production ShelfSense endpoints
- **AI-powered forecasting** with confidence intervals (P10/P50/P90)
- **Pick list generation** with priority and reasoning
- **Model accuracy metrics** and analytics
- **CORS enabled** for cross-origin requests

## API Endpoints

### Locations
- `GET /api/locations` - List all micromarket locations
- `GET /api/locations/{location_id}` - Get specific location

### Products
- `GET /api/products` - List all products
- `GET /api/products/{product_id}` - Get specific product

### Pick Lists
- `GET /api/pick-list?location_id={id}&date={date}` - Get pick list for location
- `GET /api/pick-list/all?date={date}` - Get all pick lists

### Forecasting
- `GET /api/forecast/demand?location_id={id}&product_id={id}&forecast_date={date}` - Get demand forecasts

### Analytics
- `GET /api/models/product-accuracy?location_id={id}&product_id={id}` - Model accuracy metrics
- `GET /api/inventory/status?location_id={id}&status_filter={status}` - Inventory status
- `GET /api/analytics/summary` - Overall analytics summary

## Local Development

### Prerequisites
- Python 3.11+
- pip or uv

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Server runs on `http://localhost:8000`

View API documentation at `http://localhost:8000/docs`

### Example Request

```bash
curl http://localhost:8000/api/locations
```

## Railway Deployment

### Deploy to Railway

1. **Create a new Railway project**
   ```bash
   railway login
   railway init
   ```

2. **Deploy**
   ```bash
   railway up
   ```

3. **Set environment variables** (optional)
   - Railway auto-detects Python and uses the Procfile
   - `PORT` is automatically set by Railway

4. **Get your URL**
   ```bash
   railway domain
   ```

### Environment Variables

- `PORT` - Server port (automatically set by Railway)

## Sample Data

The mock API includes:
- **5 locations**: Hotels in SF, NYC, Chicago + office in Austin + hospital in Boston
- **20+ products**: Beverages, snacks, fresh food, health items
- **Dynamic data**: Forecasts, pick lists, and analytics generated on-the-fly

### Sample Locations
- Westin St. Francis - San Francisco (1195 rooms, 78% occupancy)
- Marriott Marquis - Times Square (1966 rooms, 85% occupancy)
- Hilton Chicago O'Hare Airport (858 rooms, 72% occupancy)
- TechCorp Campus - Austin (2500 capacity, 65% occupancy)
- Boston Medical Center - Staff Lounge (24/7 operation)

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python 3.11** - Runtime

## Health Check

`GET /health` - Returns server health status

## API Documentation

Interactive API docs available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
