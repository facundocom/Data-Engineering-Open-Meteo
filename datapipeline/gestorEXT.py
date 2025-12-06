import requests, requests.exceptions
import pandas as pd

class extraccion:

    def obtener_urlforecast(self, ac):
        return ac.pasar_urlforecast()
    
    def obtener_urlhistorical(self, ac):
        return ac.pasar_urlhistorical()
    
    def obtener_openmeteo(self, ac):
        return ac.pasar_openmeteo()
    
    def obtener_parametrosf(self, ac):
        return ac.pasar_parametrosforecast()
    
    def obtener_parametrosh(self, ac, year, month):
       return ac.pasar_parametroshistorical(year, month)

    def apitest(self, ac):

        params= self.obtener_parametrosf(ac)
        url= self.obtener_urlforecast(ac)
        openmeteo= self.obtener_openmeteo(ac)

        print(" Obteniendo datos meteorológicos desde Open-Meteo API...")

        try:
            responses = openmeteo.weather_api(url, params=params)

			# Process first location. Add a for-loop for multiple locations or weather models (DOCUMENTACION)
            response = responses[0]
            print(f"Conexión Exitosa con Cuesta del Viento:")
            print(f"Coordenadas: {response.Latitude()}°N {response.Longitude()}°E")
            print(f"Elevación: {response.Elevation()} m asl")
            print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
            print(f"Modelo Meteorológico: {response.Model()}")

            return response

        except requests.exceptions.HTTPError as e:
            ep = f" ERROR DE RESPUESTA DE API (HTTP): {e}"
            return ep
        #Captura errores logicos o de servidor (400, 500, etc.)

        except requests.exceptions.ConnectionError as e:
            ep = f" ERROR DE CONEXIÓN DE RED: {e}"
            return ep
        #Captura errores de red
            
        except Exception as e:
            ep = f" ERROR INESPERADO: {e}"
            return ep
        #Captura cualquier otro error inesperado (fallo interno de la libreria)

    def get_dataforecast(self, ac):

        params= self.obtener_parametrosf(ac)
        urlforecast= self.obtener_urlforecast(ac)
        openmeteo= self.obtener_openmeteo(ac)

        #llamamos al test para ver si anda la api
        response = self.apitest(ac)
        if isinstance(response, Exception):
            print(f"Hubo algún error al obtener los datos. {response}")
            return None
        
        else:
            #cargamos como nos dice la documentacion 
            respuesta = openmeteo.weather_api(urlforecast, params=params) #pasaje de la url con el endpoint (lat y long y los parametros necesarios para la informacion deseada)
            hourly = respuesta[0].Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy() #temperatura
            hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy() #velocidad del viento
            hourly_wind_gusts_10m = hourly.Variables(2).ValuesAsNumpy() #racha de viento
            hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy() #direccion del viento

            hourly_data = {"date": pd.date_range(
	            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	            end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	            freq = pd.Timedelta(seconds = hourly.Interval()),
	            inclusive = "left"
            ),}

            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
            hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
            hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

            hourly_dataframe = pd.DataFrame(data = hourly_data)
            #print("\nPronostico cada una hora\n", hourly_dataframe)
            return hourly_dataframe
        
    def get_datahistorical(self, ac, year, month):
        params= self.obtener_parametrosh(ac, year, month)
        urlhistorical= self.obtener_urlhistorical(ac)
        openmeteo= self.obtener_openmeteo(ac)
        
        #llamamos al test para ver si anda la api
        response = self.apitest(ac)
        if isinstance(response, Exception):
            print(f"Hubo algún error al obtener los datos. {response}")
            return None
        
        else:
                #cargamos como nos dice la documentacion 
                respuesta = openmeteo.weather_api(urlhistorical, params=params) #pasaje de la url con el endpoint (lat y long y los parametros necesarios para la informacion deseada)
                hourly = respuesta[0].Hourly()
                hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy() #temperatura
                hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy() #velocidad del viento
                hourly_wind_gusts_10m = hourly.Variables(2).ValuesAsNumpy() #racha de viento
                hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy() #direccion del viento

                hourly_data = {"date": pd.date_range(
                    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                    end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                    freq = pd.Timedelta(seconds = hourly.Interval()),
                    inclusive = "left"
                )}

                hourly_data["temperature_2m"] = hourly_temperature_2m
                hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
                hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
                hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

                hourly_dataframe = pd.DataFrame(data = hourly_data)
                
                #print("\nPronostico cada una hora\n", hourly_dataframe)
                return hourly_dataframe