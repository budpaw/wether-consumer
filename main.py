import requests

API_TOKEN='<YOUR_TOKEN>'


url  = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK?last30days&key={API_TOKEN}&contentType=json"

data = requests.get(url)

print(data.content)
