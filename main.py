import requests
import os
from config import load_config
import pandas as pd

class WeatherConsumer:
    __api_key=None
    host=None
    result = None
    def __init__(self):
        cfg = load_config()
        self.__api_key = cfg['api_key']
        self.host = cfg['host']
        
    def __read(self):
        url  = f"{self.host}/VisualCrossingWebServices/rest/services/timeline/London,UK?last30days&key={self.__api_key}&contentType=json&include=days&elements=datetime,temp,windspeed"
        self.result = requests.get(url).json()
        return self.result
    
    
    def _transform(self):
        df = pd.json_normalize(self.result).explode('days')
        df['datetime'] = df.apply(lambda x: x['days']['datetime'], axis = 1)
        df['temp'] = df.apply(lambda x: x['days']['temp'], axis = 1)
        df['windspeed'] = df.apply(lambda x: x['days']['windspeed'], axis = 1)
        df=df.drop(['days', 'queryCost', 'latitude', 'longitude','resolvedAddress','timezone', 'tzoffset'], axis = 1)
        df = df.groupby('address').agg({'temp': ['mean', 'median'],'windspeed': ['mean', 'median']})
        df.columns = ['temp_avg', 'temp_median', 'wind_avg', 'wind_median']
        return df

    
    def last_30days(self):
        data = self.__read()
        data = self._transform()
        return data
        
w = WeatherConsumer()
print(w.last_30days())
