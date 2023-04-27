import requests
import os
from config import load_config



class WeatherConsumer:
    __api_key=None
    host=None
    
    def __init__(self):
        cfg = load_config()
        self.__api_key = cfg['api_key']
        self.host = cfg['host']
        
    def __read(self):
        url  = f"{self.host}/VisualCrossingWebServices/rest/services/timeline/London,UK?last30days&key={self.__api_key}&contentType=json"
        return requests.get(url)
    
    
    def _transform(self):
        pass
    
    
    def last_30days(self):
        data = self.__read()
        return data.json()
        
w = WeatherConsumer()
print(w.last_30days())
