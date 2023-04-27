# wether-consumer
Weather consumer api 

## Install require packages 
Clone repository, go to main app directory and install packages with following command:
```sh
pip install -r requirements.txt
```

## Get last 30 days data
To get avg and median for temperature and windspeed you can use 
```sh
from main import WeatherConsumer
w = WeatherConsumer()
w.last_30days()
```

## Configuration 
Config file is located in config directory, to change parameters please edit file config.py
```
main:
  host: https://weather.visualcrossing.com
  api_key: <YOUR_API_KEY>
  countries:
    - country: PL
      city: lodz
    ...
    - country: BE
      city: brussels
```

For <YOUR_API_KEY> placeholder please provide you API TOKEN generated from weather.visualcrossing.com.
You can add next country without changing code, you can simple add new section under main/countries in following template:
```
    - country: <ISO2 Country code>
      city: <name of city in eng>
```