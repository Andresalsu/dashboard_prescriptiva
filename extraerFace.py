import urllib3
import facebook
import requests
from urllib.request import urlopen
import json
from urllib.parse import urlencode
 
page_id="15640987134"
#Replace this with your access token generated from Graph API Explorer
token="EAAlW0PQxZC24BAGsJgIEJbZCSZA9eZCI9ViAfBsKmI2y8TD3eLHNwe3ZCGGt2CZC7UuHE9GlvqGmUzjR6ajy5NvgVltIRauoni0Js3pNElYDzDTZBZBhnDWcFDxZA1HBNxV1mB0ZA0t02ZBG6euLs33Ve6jrOD2rVG1wPt1mwKbARRa6djHrjkDEiK8lBZB1DQxIrSbUEVt5MwoOEgZDZD"
 
url="https://graph.facebook.com/"+page_id+"/posts/?fields=id,created_time,message,shares.summary(true).limit(0),comments.summary(true).limit(0),likes.summary(true),reactions.type(LOVE).limit(0).summary(total_count).as(Love),reactions.type(WOW).limit(0).summary(total_count).as(Wow),reactions.type(HAHA).limit(0).summary(total_count).as(Haha),reactions.type(SAD).limit(0).summary(1).as(Sad),reactions.type(ANGRY).limit(0).summary(1).as(Angry)&access_token="+token+"&limit=50"
try:
    facebook_connection = urlopen(url)
    data = facebook_connection.read().decode('utf8')
    json_object = json.loads(data)
    posts=json_object["data"]
    
    df=pd.DataFrame(posts)
    
    
    df['Angry'] = df['Angry'].astype(str).str.replace('{\'data\':(.*?)count\': ','')
    df['Angry'] = df['Angry'].str.replace(',(.*?)}}','')
    
    df['Haha'] = df['Haha'].astype(str).str.replace('{\'data\':(.*?)count\': ','')
    df['Haha'] = df['Haha'].str.replace('}}','')
    
    df['Love'] = df['Love'].astype(str).str.replace('{\'data\':(.*?)count\': ','')
    df['Love'] = df['Love'].str.replace('}}','')
    
    df['Sad'] = df['Sad'].astype(str).str.replace('{\'data\':(.*?)count\': ','')
    df['Sad'] = df['Sad'].str.replace(',(.*?)}}','')
    
    df['Wow'] = df['Wow'].astype(str).str.replace('{\'data\':(.*?)count\': ','')
    df['Wow'] = df['Wow'].str.replace('}}','')
    
    df['comments'] = df['comments'].astype(str).str.replace('{\'data\':(.*?)count\': ','')
    df['comments'] = df['comments'].str.replace(',(.*?)}}','')
    
    df['likes'] = df['likes'].astype(str).str.replace('{\'(.*?)count\':','')
    df['likes'] = df['likes'].str.replace(',(.*?)}}','')
    
    df['shares'] = df['shares'].astype(str).str.replace('{\'count\': ','')
    df['shares'] = df['shares'].str.replace('}','')
    
    df['date'], df['time'] = df['created_time'].astype(str).str.split('T', 1).str
    df['time'] = df['time'].str.replace('[+]0000','')
    
    df.to_csv("Facebook Posts.csv")
    
    print(df)
    
except Exception as ex:
    print (ex)