import requests
import os
from config import load_config
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

class WeatherConsumer:
    __api_key=None
    host=None
    countries = None

    def __init__(self):
        logging.debug("Init WeatherConsumer")
        cfg = load_config()
        logging.debug("Load configuration")
        self.__api_key = cfg['api_key']
        self.host = cfg['host']
        self.countries = cfg['countries']
        
    def __read(self, location):
        logging.debug(f"API Request for: {location}")        
        url  = f"{self.host}/VisualCrossingWebServices/rest/services/timeline/{location}?last30days&key={self.__api_key}&contentType=json&include=days&elements=datetime,temp,windspeed"        
        result = requests.get(url)        
        if result.status_code == 200:
            logging.debug(f"API Request result: SUCCESS")   
            return result.json()
        else:
            logging.error(f"API Request result: FAILED")
            logging.error(f"   Status code: {result.status_code}") 
            logging.error(f"   Message: {result.content.decode().replace(self.__api_key)}") 
            return {}
        
    def _transform(self, data):
        logging.debug("Transformation start")
        logging.debug(f"Checking data for future transformS")   
        war = any(not x for x in data)
        if war:
            logging.error(f"One or more record is empty please check logs above")
            return pd.DataFrame(columns=['city','temp_avg', 'temp_median', 'wind_avg', 'wind_median'])
        
        logging.debug(f"Creating DataFrame")   
        df = pd.json_normalize(data).explode('days')
                
        logging.debug(f"Extract data from subnodes")  
        df['datetime'] = df.apply(lambda x: x['days']['datetime'], axis = 1)
        df['temp'] = df.apply(lambda x: x['days']['temp'], axis = 1)
        df['windspeed'] = df.apply(lambda x: x['days']['windspeed'], axis = 1)
        
        logging.debug(f"Drop unusful columns")
        df = df.drop(['days', 'queryCost', 'latitude', 'longitude', 'resolvedAddress','timezone', 'tzoffset'], axis = 1)
        df = df.groupby('address').agg({'temp': ['mean', 'median'], 'windspeed': ['mean', 'median']})
        
        logging.debug(f"Columns rename")
        df.columns = ['temp_avg', 'temp_median', 'wind_avg', 'wind_median']
        
        logging.debug(f"Update index")
        df = df.reset_index(drop=False).rename(columns={'address':"city"}) 
        return df

    def preety_print(self, df, output_format='df'):
        for column in ['temp_avg', 'temp_median', 'wind_avg', 'wind_median']:
            df[column] = df[column].apply(lambda x: "{:.2f}".format(x))

        max_len = df.apply(lambda x: x.str.len()).max()
        df = df.apply(lambda x: x.str.ljust(max_len[x.name]))
        df = df.to_string(justify='left', index=False)
        
        print(df)
    
    def last_30days(self):
        def format_country(country):            
            return ','.join((country['city'].lower(),country['country'].upper()))        
        raw_data = [self.__read(format_country(country)) for country in self.countries]
        result = self._transform(raw_data)
        return self.preety_print(result)
    
        
w = WeatherConsumer()
w.last_30days()
