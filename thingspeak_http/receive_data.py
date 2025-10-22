# Channel ID: 3125997
# Author: toltalbiuh
# API Key (Write): GWIECJSRB36N2SXJ
# API Key (Read): L83C8R1J5XYDS7G7

from urllib import request, parse
from time import sleep
import json

def thingspeak_get():
    api_key_read = "L83C8R1J5XYDS7G7"
    channel_ID = "3125997"
    # GET https://api.thingspeak.com/channels/3125997/fields/1.json?results=2
    req = request.Request(f'https://api.thingspeak.com/channels/{channel_ID}/fields/1/last.json?api_key={api_key_read}', method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    respone_data = json.loads(response_data)
    value = respone_data['field1']
    return value

value = thingspeak_get()
print(value)