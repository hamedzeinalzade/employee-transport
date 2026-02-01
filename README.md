# Employee Route Optimization

A lightweight Streamlit application for optimizing employee shuttle routes using **Google OR-Tools** and **Google Maps APIs**.  
The system converts employee addresses into optimized bus routes based on real travel times.

---

## Key Features

- Address geocoding via Google Geocoding API
- Travel time calculation using Google Distance Matrix API
- True route optimization with Google OR-Tools (VRP)
- Single-process Streamlit application (no separate backend)
- Modular and maintainable codebase
- Persian (Farsi) user interface

---

## Architecture

- **Streamlit**: User interface
- **Service layer**: Orchestrates the workflow
- **Core modules**: Maps integration and routing logic
- **OR-Tools**: Vehicle Routing Problem solver

---

## Project Structure

employee_transport/
├── app.py
├── core/
│ ├── config.py
│ ├── maps.py
│ ├── routing.py
│ └── service.py
├── requirements.txt
└── README.md


---

## Requirements

- Python 3.9+
- Google Maps API key with:
  - Geocoding API
  - Distance Matrix API

---

## Configuration

Edit `core/config.py`:

```python
COMPANY_LOCATION = (35.6892, 51.3890)
BUS_CAPACITY = 20
MAX_ROUTE_TIME = 60
GOOGLE_API_KEY = "YOUR_API_KEY"
```

---


## Installation

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```  


Open the provided local URL in your browser.

---


## How It Works

1. User enters employee addresses

2. Addresses are geocoded to coordinates

3. A travel-time matrix is built

4. OR-Tools computes optimized shuttle routes

5. Results are displayed per bus

---


## Notes

- The company location is treated as the route depot

- Routes start and end at the company

---


