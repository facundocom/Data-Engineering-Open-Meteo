from datapipeline.gestorAPI import APIconfig
from datapipeline.gestorEXT import extraccion
from datapipeline.gestorCARGA import carga
from datapipeline.MINIOconfig import configMINIO
#from datapipeline.gestorTRF import transformacion
from datetime import date
from deltalake.exceptions import TableNotFoundError
from apscheduler.schedulers.background import BlockingScheduler
import time

def dia_de_hoy():

        hoy=date.today()
        anio=hoy.strftime("%Y")
        mes=hoy.strftime("%m")
        dia=hoy.strftime("%d")
        return f"/{anio}/{mes}/{dia}"

def extincremental(gc, ge, ac, gm):
        hoy= dia_de_hoy()
        try:
                gc.upsertforecast(ge, ac, gm, hoy)
        except TableNotFoundError:
                gc.carga_forecast_overw(ge, gm, ac, hoy)
      
if __name__ == "__main__":

        # parametros específicos para Cuesta del Viento:
        latitud_cuesta = -30.183
        longitud_cuesta = -69.066
        timezone_cuesta = "America/Argentina/San_Juan"
        hourly=["temperature_2m", "wind_speed_10m", "wind_gusts_10m", "wind_direction_10m"]
        
        # cargamos los parametros en la ejecución del pipeline
        ac = APIconfig(latitud_cuesta, longitud_cuesta, timezone_cuesta, hourly)
        ge=extraccion()
        gc=carga()
        gm=configMINIO()
        #gt=transformacion()

        hoy=dia_de_hoy()
        #gc.carga_forecast_overw(ge, gm, ac, hoy)
        extincremental(gc, ge, ac, gm)
        gc.carga_historical_overw(ge, gm, ac)

        #scheduler=BlockingScheduler()
        #scheduler.add_job(extincremental(gc,ge,ac,gm), 'cron', hour=8, minute=0, timezone='America/Argentina/Buenos_Aires')

        # try: 
        #         scheduler.start()
        # except KeyboardInterrupt:
        #         print("pipeline cancelado por teclado")
        # except SystemExit:
        #         print ("Error en el pipeline")
    