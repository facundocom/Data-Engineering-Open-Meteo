from deltalake import write_deltalake, DeltaTable
import pandas as pd
import pyarrow as pa
import os


class carga:
    def getforecast(self, ge, ac):
        return ge.get_dataforecast(ac)
    
    def gethistorical(self, ge, ac, year, month):
        return ge.get_datahistorical(ac, year, month)
    
    def carga_forecast_overw(self, ge, gm, ac, hoy):

        ruta= self.define_route_forecast(gm, hoy)
        df = self.getforecast(ge, ac)
        print ("Obteniendo datos para S3", flush=True)

        write_deltalake(
            f"s3://{ruta}", # ruta de guardado
            df, # dataframe con los datos
            mode="overwrite",
            storage_options=gm.pasar_stgopt(),
        )
        print ("Carga exitosa en el bucket", flush=True)

    def carga_historical_overw(self, ge, gm, ac):
        startyear=2019
        endyear=2024
        startmonth=1
        endmonth=12
        ruta= self.define_route_historical(gm)

        for year in range(startyear, endyear+1):
            for month in range(startmonth, endmonth+1):
                df = self.gethistorical(ge, ac, year, month)
                #print ("Obteniendo datos para S3", flush=True)

                write_deltalake(
                    f"s3://{ruta}/{year}/{month}", # ruta de guardado
                    df, # dataframe con los datos
                    mode="overwrite",
                    storage_options=gm.pasar_stgopt(),
                )
            print (f"Carga exitosa en el bucket de los datos de {year}", flush=True)
    
    def conversion_pyarrow_forecast(self, gm, hoy):
        stgop= gm.pasar_stgopt()
        ruta=self.define_route_forecast(gm, hoy)
        actual_data = DeltaTable(f"s3://{ruta}", storage_options=stgop)
        return actual_data

    def upsertforecast(self, ge, ac, gm, hoy):
        #stgopt=gm.pasarstgopt()
        actual_data=self.conversion_pyarrow_forecast(gm, hoy)
        (
        actual_data.merge(
            source=pa.Table.from_pandas(ge.get_dataforecast(ac)),
            source_alias="src", #data nueva
            target_alias="tgt", #data actual
            predicate="src.date = tgt.date"
        ) \
        .when_matched_update_all() \
            #.when_matched_update(
            #    updates={
            #        "hourly_temperature_2m" = "src.hourly_temperature_2m"
            #        "hourly_wind_speed_10m" = "src.hourly_wind_speed_10m"
            #       "hourly_wind_gusts_10m" = "src.hourly_wind_gusts_10m"
            #        "hourly_wind_direction_10m" = "src.hourly_wind_direction_10m"
            #    }
            #
        .when_not_matched_insert_all() \
        .execute()
        )
        print ("Upsert exitoso")
    
    def define_route_forecast(self, gm, hoy):
        bkt_name= gm.pasar_bkt()
        rutabase = f"{bkt_name}/datalake/bronze/forecast"
        rutafinal = f"{rutabase}{hoy}"
        return rutafinal
    
    def define_route_historical(self, gm):
        bkt_name= gm.pasar_bkt()
        ruta= f"{bkt_name}/datalake/bronze/historical"
        return ruta