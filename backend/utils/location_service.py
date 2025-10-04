import os
import httpx
from typing import Dict, Any, Optional

class LocationService:
    """
    Handle location-based carbon calculation adjustments
    Uses OpenWeatherMap API for climate data
    """
    
    # Indian states with baseline climate multipliers
    REGIONAL_BASELINE = {
        # High rainfall, tropical zones
        "kerala": {"multiplier": 1.3, "zone": "tropical_wet"},
        "karnataka": {"multiplier": 1.15, "zone": "tropical_mixed"},
        "tamil nadu": {"multiplier": 1.2, "zone": "tropical_dry"},
        
        # Fertile plains
        "punjab": {"multiplier": 1.1, "zone": "subtropical_semiarid"},
        "haryana": {"multiplier": 1.05, "zone": "subtropical_semiarid"},
        "uttar pradesh": {"multiplier": 1.1, "zone": "subtropical_humid"},
        "bihar": {"multiplier": 1.05, "zone": "subtropical_humid"},
        "west bengal": {"multiplier": 1.15, "zone": "subtropical_humid"},
        
        # Deccan plateau
        "maharashtra": {"multiplier": 1.0, "zone": "tropical_semiarid"},
        "telangana": {"multiplier": 1.0, "zone": "tropical_semiarid"},
        "andhra pradesh": {"multiplier": 1.05, "zone": "tropical_dry"},
        
        # Western states
        "gujarat": {"multiplier": 0.95, "zone": "arid_semiarid"},
        "rajasthan": {"multiplier": 0.7, "zone": "arid"},
        
        # Eastern states
        "odisha": {"multiplier": 1.1, "zone": "tropical_humid"},
        "jharkhand": {"multiplier": 1.0, "zone": "subtropical_humid"},
        "chhattisgarh": {"multiplier": 1.05, "zone": "tropical_dry"},
        
        # Central states
        "madhya pradesh": {"multiplier": 0.95, "zone": "subtropical_dry"},
        
        # Himalayan states
        "himachal pradesh": {"multiplier": 1.2, "zone": "temperate"},
        "uttarakhand": {"multiplier": 1.15, "zone": "temperate"},
        
        # Northeast
        "assam": {"multiplier": 1.25, "zone": "tropical_wet"},
        "meghalaya": {"multiplier": 1.3, "zone": "tropical_wet"},
        "manipur": {"multiplier": 1.2, "zone": "tropical_humid"},
        "mizoram": {"multiplier": 1.2, "zone": "tropical_humid"},
        "nagaland": {"multiplier": 1.2, "zone": "tropical_humid"},
        "tripura": {"multiplier": 1.15, "zone": "tropical_humid"},
        "arunachal pradesh": {"multiplier": 1.15, "zone": "subtropical_humid"},
        "sikkim": {"multiplier": 1.15, "zone": "temperate"},
        
        # Other states
        "goa": {"multiplier": 1.25, "zone": "tropical_wet"},
        "punjab": {"multiplier": 1.1, "zone": "subtropical_semiarid"}
    }
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_baseline_multiplier(self, state: str) -> Dict[str, Any]:
        """Get baseline climate multiplier for a state"""
        state_lower = state.lower().strip()
        baseline = self.REGIONAL_BASELINE.get(state_lower, {
            "multiplier": 1.0,
            "zone": "unknown"
        })
        return baseline
    
    async def get_weather_data(self, city: str, state: str) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data from OpenWeatherMap
        
        Returns climate factors that affect carbon sequestration:
        - Temperature
        - Humidity
        - Rainfall (if available)
        """
        
        if not self.api_key:
            return None
        
        # Construct location query (city, state, India)
        location = f"{city},{state},IN"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        "q": location,
                        "appid": self.api_key,
                        "units": "metric"  # Celsius
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "weather": data["weather"][0]["main"],
                        "description": data["weather"][0]["description"],
                        "coordinates": {
                            "lat": data["coord"]["lat"],
                            "lon": data["coord"]["lon"]
                        }
                    }
                else:
                    return None
                    
        except Exception as e:
            print(f"Weather API error: {str(e)}")
            return None
    
    def calculate_climate_multiplier(
        self, 
        baseline_multiplier: float,
        weather_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate final climate multiplier based on:
        1. Regional baseline
        2. Real-time weather adjustments
        
        Returns multiplier + explanation
        """
        
        final_multiplier = baseline_multiplier
        adjustments = []
        
        if weather_data:
            temp = weather_data.get("temperature", 25)
            humidity = weather_data.get("humidity", 60)
            
            # Temperature adjustment
            # Optimal range: 20-30°C for most vegetation
            if 20 <= temp <= 30:
                temp_adj = 1.0
                adjustments.append(f"Optimal temperature ({temp}°C)")
            elif temp > 35:
                temp_adj = 0.9
                adjustments.append(f"High temperature ({temp}°C) slightly reduces sequestration")
            elif temp < 15:
                temp_adj = 0.85
                adjustments.append(f"Cool temperature ({temp}°C) reduces growth rate")
            else:
                temp_adj = 0.95
                adjustments.append(f"Moderate temperature ({temp}°C)")
            
            # Humidity adjustment
            # Higher humidity generally better for carbon sequestration
            if humidity > 70:
                humidity_adj = 1.05
                adjustments.append(f"High humidity ({humidity}%) favorable for growth")
            elif humidity < 40:
                humidity_adj = 0.95
                adjustments.append(f"Low humidity ({humidity}%) limits sequestration")
            else:
                humidity_adj = 1.0
                adjustments.append(f"Moderate humidity ({humidity}%)")
            
            # Apply adjustments
            final_multiplier = baseline_multiplier * temp_adj * humidity_adj
            
        else:
            adjustments.append("Using regional baseline (weather data unavailable)")
        
        return {
            "multiplier": round(final_multiplier, 2),
            "baseline": baseline_multiplier,
            "adjustments": adjustments,
            "weather_data_used": weather_data is not None
        }
    
    async def get_location_analysis(
        self, 
        city: str, 
        state: str
    ) -> Dict[str, Any]:
        """
        Complete location-based analysis
        
        Args:
            city: User's city
            state: User's state
            
        Returns:
            Complete location context + climate multiplier
        """
        
        # Get baseline
        baseline = self.get_baseline_multiplier(state)
        
        # Get weather data
        weather_data = await self.get_weather_data(city, state)
        
        # Calculate final multiplier
        climate_result = self.calculate_climate_multiplier(
            baseline["multiplier"],
            weather_data
        )
        
        return {
            "location": {
                "city": city,
                "state": state,
                "climate_zone": baseline["zone"]
            },
            "climate_multiplier": climate_result["multiplier"],
            "baseline_multiplier": baseline["multiplier"],
            "weather_data": weather_data,
            "adjustments": climate_result["adjustments"],
            "explanation": self._generate_explanation(
                state, 
                baseline["zone"],
                climate_result
            )
        }
    
    def _generate_explanation(
        self, 
        state: str, 
        zone: str, 
        climate_result: Dict[str, Any]
    ) -> str:
        """Generate human-readable explanation"""
        
        explanation = f"Location: {state.title()} ({zone.replace('_', ' ').title()} zone)\n"
        explanation += f"Climate multiplier: {climate_result['multiplier']}x\n\n"
        explanation += "Adjustments applied:\n"
        
        for adj in climate_result['adjustments']:
            explanation += f"- {adj}\n"
        
        return explanation
    
    @staticmethod
    def get_state_list() -> list:
        """Return list of supported Indian states"""
        return sorted([
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
            "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
            "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
            "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
            "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
            "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
            "West Bengal"
        ])