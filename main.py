import requests
import os
from config import load_config
import pandas as pd

class WeatherConsumer:
    __api_key=None
    host=None
    countries = None

    def __init__(self):
        cfg = load_config()
        self.__api_key = cfg['api_key']
        self.host = cfg['host']
        self.countries = cfg['countries']
        
    def __read(self, location):        
        url  = f"{self.host}/VisualCrossingWebServices/rest/services/timeline/{location}?last30days&key={self.__api_key}&contentType=json&include=days&elements=datetime,temp,windspeed"
        result = requests.get(url).json()
        return result
    
    
    def _transform(self, data):
        df = pd.json_normalize(data).explode('days')        
        df['datetime'] = df.apply(lambda x: x['days']['datetime'], axis = 1)
        df['temp'] = df.apply(lambda x: x['days']['temp'], axis = 1)
        df['windspeed'] = df.apply(lambda x: x['days']['windspeed'], axis = 1)
        
        df = df.drop(['days', 'queryCost', 'latitude', 'longitude','resolvedAddress','timezone', 'tzoffset'], axis = 1)
        df = df.groupby('address').agg({'temp': ['mean', 'median'],'windspeed': ['mean', 'median']})
        
        df.columns = ['temp_avg', 'temp_median', 'wind_avg', 'wind_median']
        df = df.reset_index(drop=False).rename(columns={'address':"city"}) 


        return df

    def preety_print(self, df):
        df['temp_avg'] = df['temp_avg'].apply(lambda x: "{:.2f}".format(x))
        df['temp_median'] = df['temp_median'].apply(lambda x: "{:.2f}".format(x))
        df['wind_avg'] = df['wind_avg'].apply(lambda x: "{:.2f}".format(x))
        df['wind_median'] = df['wind_median'].apply(lambda x: "{:.2f}".format(x))
        
        max_len = df.apply(lambda x: x.str.len()).max()
        df = df.apply(lambda x: x.str.ljust(max_len[x.name]))
        df = df.to_string(justify='left')
        return df
    
    def last_30days(self):
        raw_data = [self.__read(','.join((country['city'].lower(),country['country'].upper()))) for country in self.countries]
        result = self._transform(raw_data)
        return self.preety_print(result)
        
w = WeatherConsumer()
print(w.last_30days())
