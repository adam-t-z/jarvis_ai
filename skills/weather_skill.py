"""
Weather Skill for Jarvis AI
Handles weather information retrieval through API
"""

import os
import requests
from typing import Dict, Optional
from datetime import datetime, timedelta


class WeatherSkill:
    """Skill for weather information retrieval"""
    
    def __init__(self):
        # Support multiple weather APIs
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.weatherapi_key = os.getenv("WEATHERAPI_KEY")
        self.default_location = os.getenv("DEFAULT_LOCATION", "New York")
        
        # API endpoints
        self.openweather_base = "https://api.openweathermap.org/data/2.5"
        self.weatherapi_base = "https://api.weatherapi.com/v1"
    
    def get_current_weather_openweather(self, location: str) -> Optional[Dict]:
        """
        Get current weather using OpenWeatherMap API
        
        Args:
            location: City name or coordinates
            
        Returns:
            Dict: Weather data or None if failed
        """
        if not self.openweather_api_key:
            return None
        
        try:
            url = f"{self.openweather_base}/weather"
            params = {
                "q": location,
                "appid": self.openweather_api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"OpenWeather API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching weather from OpenWeather: {str(e)}")
            return None
    
    def get_current_weather_weatherapi(self, location: str) -> Optional[Dict]:
        """
        Get current weather using WeatherAPI
        
        Args:
            location: City name or coordinates
            
        Returns:
            Dict: Weather data or None if failed
        """
        if not self.weatherapi_key:
            return None
        
        try:
            url = f"{self.weatherapi_base}/current.json"
            params = {
                "key": self.weatherapi_key,
                "q": location,
                "aqi": "no"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"WeatherAPI error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching weather from WeatherAPI: {str(e)}")
            return None
    
    def get_weather_forecast_openweather(self, location: str, days: int = 5) -> Optional[Dict]:
        """
        Get weather forecast using OpenWeatherMap API
        
        Args:
            location: City name or coordinates
            days: Number of days for forecast (max 5 for free tier)
            
        Returns:
            Dict: Forecast data or None if failed
        """
        if not self.openweather_api_key:
            return None
        
        try:
            url = f"{self.openweather_base}/forecast"
            params = {
                "q": location,
                "appid": self.openweather_api_key,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"OpenWeather forecast API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching forecast from OpenWeather: {str(e)}")
            return None
    
    def get_weather_forecast_weatherapi(self, location: str, days: int = 3) -> Optional[Dict]:
        """
        Get weather forecast using WeatherAPI
        
        Args:
            location: City name or coordinates
            days: Number of days for forecast (max 3 for free tier)
            
        Returns:
            Dict: Forecast data or None if failed
        """
        if not self.weatherapi_key:
            return None
        
        try:
            url = f"{self.weatherapi_base}/forecast.json"
            params = {
                "key": self.weatherapi_key,
                "q": location,
                "days": min(days, 3),  # Free tier limit
                "aqi": "no",
                "alerts": "no"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"WeatherAPI forecast error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching forecast from WeatherAPI: {str(e)}")
            return None
    
    def format_current_weather(self, weather_data: Dict, api_source: str) -> str:
        """
        Format current weather data into readable text
        
        Args:
            weather_data: Weather data from API
            api_source: Source API ('openweather' or 'weatherapi')
            
        Returns:
            str: Formatted weather description
        """
        try:
            if api_source == "openweather":
                location = weather_data['name']
                country = weather_data['sys']['country']
                temp = round(weather_data['main']['temp'])
                feels_like = round(weather_data['main']['feels_like'])
                humidity = weather_data['main']['humidity']
                description = weather_data['weather'][0]['description'].title()
                wind_speed = weather_data['wind']['speed']
                
                return (f"Current weather in {location}, {country}:\n"
                       f"Temperature: {temp}°C (feels like {feels_like}°C)\n"
                       f"Condition: {description}\n"
                       f"Humidity: {humidity}%\n"
                       f"Wind speed: {wind_speed} m/s")
            
            elif api_source == "weatherapi":
                location = weather_data['location']['name']
                country = weather_data['location']['country']
                temp = round(weather_data['current']['temp_c'])
                feels_like = round(weather_data['current']['feelslike_c'])
                humidity = weather_data['current']['humidity']
                condition = weather_data['current']['condition']['text']
                wind_speed = weather_data['current']['wind_kph']
                
                return (f"Current weather in {location}, {country}:\n"
                       f"Temperature: {temp}°C (feels like {feels_like}°C)\n"
                       f"Condition: {condition}\n"
                       f"Humidity: {humidity}%\n"
                       f"Wind speed: {wind_speed} km/h")
            
        except KeyError as e:
            return f"Error formatting weather data: missing key {str(e)}"
    
    def format_forecast(self, forecast_data: Dict, api_source: str, days: int = 3) -> str:
        """
        Format forecast data into readable text
        
        Args:
            forecast_data: Forecast data from API
            api_source: Source API ('openweather' or 'weatherapi')
            days: Number of days to format
            
        Returns:
            str: Formatted forecast description
        """
        try:
            if api_source == "openweather":
                location = forecast_data['city']['name']
                forecast_text = f"Weather forecast for {location}:\n\n"
                
                # Group by days
                current_date = None
                daily_forecasts = []
                
                for item in forecast_data['list']:
                    date = datetime.fromtimestamp(item['dt']).date()
                    if date != current_date:
                        if len(daily_forecasts) >= days:
                            break
                        current_date = date
                        temp = round(item['main']['temp'])
                        description = item['weather'][0]['description'].title()
                        daily_forecasts.append(f"{date.strftime('%A, %B %d')}: {temp}°C, {description}")
                
                return forecast_text + "\n".join(daily_forecasts)
            
            elif api_source == "weatherapi":
                location = forecast_data['location']['name']
                forecast_text = f"Weather forecast for {location}:\n\n"
                
                daily_forecasts = []
                for day in forecast_data['forecast']['forecastday'][:days]:
                    date = datetime.strptime(day['date'], '%Y-%m-%d').date()
                    max_temp = round(day['day']['maxtemp_c'])
                    min_temp = round(day['day']['mintemp_c'])
                    condition = day['day']['condition']['text']
                    daily_forecasts.append(
                        f"{date.strftime('%A, %B %d')}: {max_temp}°C/{min_temp}°C, {condition}"
                    )
                
                return forecast_text + "\n".join(daily_forecasts)
            
        except KeyError as e:
            return f"Error formatting forecast data: missing key {str(e)}"


def get_current_weather(location: str = None) -> str:
    """
    Get current weather for a location
    
    Args:
        location: Location name (uses default if not provided)
        
    Returns:
        str: Current weather description
    """
    skill = WeatherSkill()
    location = location or skill.default_location
    
    # Try WeatherAPI first, then OpenWeather
    weather_data = skill.get_current_weather_weatherapi(location)
    if weather_data:
        return skill.format_current_weather(weather_data, "weatherapi")
    
    weather_data = skill.get_current_weather_openweather(location)
    if weather_data:
        return skill.format_current_weather(weather_data, "openweather")
    
    return f"Unable to get weather information for {location}. Please check API keys and internet connection."


def get_weather_forecast(location: str = None, days: int = 3) -> str:
    """
    Get weather forecast for a location
    
    Args:
        location: Location name (uses default if not provided)
        days: Number of days for forecast
        
    Returns:
        str: Weather forecast description
    """
    skill = WeatherSkill()
    location = location or skill.default_location
    
    # Try WeatherAPI first, then OpenWeather
    forecast_data = skill.get_weather_forecast_weatherapi(location, days)
    if forecast_data:
        return skill.format_forecast(forecast_data, "weatherapi", days)
    
    forecast_data = skill.get_weather_forecast_openweather(location, days)
    if forecast_data:
        return skill.format_forecast(forecast_data, "openweather", days)
    
    return f"Unable to get weather forecast for {location}. Please check API keys and internet connection."


def get_weather_summary(location: str = None) -> str:
    """
    Get a comprehensive weather summary (current + forecast)
    
    Args:
        location: Location name (uses default if not provided)
        
    Returns:
        str: Complete weather summary
    """
    current = get_current_weather(location)
    forecast = get_weather_forecast(location, 3)
    
    return f"{current}\n\n{forecast}"


def check_rain_forecast(location: str = None, days: int = 1) -> str:
    """
    Check if rain is expected in the forecast
    
    Args:
        location: Location name (uses default if not provided)
        days: Number of days to check
        
    Returns:
        str: Rain forecast information
    """
    skill = WeatherSkill()
    location = location or skill.default_location
    
    forecast_data = skill.get_weather_forecast_weatherapi(location, days)
    if not forecast_data:
        forecast_data = skill.get_weather_forecast_openweather(location, days)
    
    if not forecast_data:
        return f"Unable to check rain forecast for {location}"
    
    rain_days = []
    try:
        if 'forecast' in forecast_data:  # WeatherAPI format
            for day in forecast_data['forecast']['forecastday'][:days]:
                condition = day['day']['condition']['text'].lower()
                if 'rain' in condition or 'shower' in condition or 'drizzle' in condition:
                    date = datetime.strptime(day['date'], '%Y-%m-%d').date()
                    rain_days.append(date.strftime('%A, %B %d'))
        else:  # OpenWeather format
            # Check for rain in forecast list
            for item in forecast_data['list']:
                if 'rain' in item['weather'][0]['description'].lower():
                    date = datetime.fromtimestamp(item['dt']).date()
                    if date.strftime('%A, %B %d') not in rain_days:
                        rain_days.append(date.strftime('%A, %B %d'))
                    if len(rain_days) >= days:
                        break
    except Exception as e:
        return f"Error checking rain forecast: {str(e)}"
    
    if rain_days:
        return f"Rain expected on: {', '.join(rain_days)}"
    else:
        return f"No rain expected in the next {days} day(s) for {location}"