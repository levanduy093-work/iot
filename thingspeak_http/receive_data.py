# Channel ID: 3127848
# Author: toltalbiuh
# API Key (Write): AHHO5UL59ZCYUYCV
# API Key (Read): N251PNZ5EG0MWI2Y

from urllib import request, parse
from time import sleep
import json

def thingspeak_get():
    api_key_read = "6J9SVD7Y3A39AY16"
    channel_ID = "3142608"
    # GET https://api.thingspeak.com/channels/3125997/fields/1.json?results=2
    # https://api.thingspeak.com/channels/3127848/fields/1/last.json?api_key=N251PNZ5EG0MWI2Y
    req = request.Request(f'https://api.thingspeak.com/channels/{channel_ID}/fields/1/last.json?api_key={api_key_read}', method="GET")
    r = request.urlopen(req)
    response_data = r.read().decode()
    respone_data = json.loads(response_data)
    value = respone_data['field1']
    return value

value = thingspeak_get()
print(value)