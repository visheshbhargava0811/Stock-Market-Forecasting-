import requests
import pandas as pd
from datetime import datetime, timedelta 
#from config import MARKETAUX_KEY

def get_news(api_token, symbols, publish_date, filter_entities=True, language='en'):

    url = f"https://api.marketaux.com/v1/news/all?symbols={symbols}&filter_entities={filter_entities}&published_on={publish_date}&language={language}&api_token={api_token}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        highlights = []
        for item in news_data['data']:
            for entity in item['entities']:
                if entity['symbol'] == symbols:
                    for highlight in entity['highlights']:
                        highlights.append(highlight['highlight'].replace('<em>', '').replace('</em>', ''))

        return highlights
    else:
        print(f"Error: {response.status_code}")
        return None
    
api_token = "o5zPUnIxmNXFXj8HugZbc3i340JuOUSY29uWoLPv"
symbols = 'AMZN'

start_date = datetime.strptime('2022-07-01', '%Y-%m-%d')
num_days = 30

try:
    df = pd.read_csv('Amazon1_news.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['date', 'news'])
for i in range(0, num_days):
    publish_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
    summary = get_news(api_token, symbols, publish_date)
    new_df = pd.DataFrame({"date":[publish_date],"news":[summary]})
    df = pd.concat([df,new_df], ignore_index=True)
    df.to_csv ('Amazon1_news.csv', index=False)