import openmeteo_requests
import requests_cache
from retry_requests import retry

class APIconfig:

	def __init__(self, latitud, longitud, timezone, hourly):
		
		# Setup the Open-Meteo API client with cache and retry on error (DOCUMENTACION)
		cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
		retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
		self.openmeteo = openmeteo_requests.Client(session = retry_session)

		self.urlf = "https://api.open-meteo.com/v1/forecast"
		self.urlh = "https://archive-api.open-meteo.com/v1/archive"
		self.paramsforecast = {
			"latitude": latitud,
			"longitude": longitud,
			"timezone": timezone,
			"hourly": hourly,
			"forecast_days":1
		}

		
	#pasamos los atributos y datos para no romper el encapsulamiento
	def pasar_parametrosforecast(self):
		return self.paramsforecast
	
	def pasar_parametroshistorical(self, year, month):
		self.paramshistorical = {
                    "latitude": -30.183,
                    "longitude": -69.066,
                    "start_date": f"{year}-{month:02d}-01",
                    "end_date": f"{year}-{month:02d}-31",
                    "hourly": ["temperature_2m", "wind_speed_10m", "wind_gusts_10m", "wind_direction_10m"],
                }
		return self.paramshistorical
	
	def pasar_urlforecast(self):
		return f"{self.urlf}"
	
	def pasar_urlhistorical(self):
		return f"{self.urlh}"

	def pasar_openmeteo(self):
		return self.openmeteo