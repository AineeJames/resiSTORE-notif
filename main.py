from urllib import request, parse
from time import sleep
import os
prev_result = 1
while True:
    response = request.urlopen("https://resi.store/lux.bool").read()
    result = int(response.decode()[0])
    if result != prev_result:
        curl_cmd = f"curl -d \"{'RESISORE OPEN' if result else 'RESISORE CLOSED'}\" -H 'Title: ResiSTORE Status' ntfy.sh/resistore"
        os.system(curl_cmd)
    prev_result = result
    sleep(30)
    
