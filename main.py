from urllib import request, parse
from time import sleep
import os
import pytz
from datetime import datetime

pst = pytz.timezone('America/Los_Angeles')

open_msg = "The resistore has opened!"
closed_msg = "The resistore has closed..."

prev_result = 1
while True:
    response = request.urlopen("https://resi.store/lux.bool").read()
    result = int(response.decode()[0])
    if result != prev_result:
        pst_time = datetime.now(pst).strftime("%H:%M")
        tag = "green_square,grinning" if result else "red_square,frowning_face"
        curl_cmd = f"""curl -d \"{open_msg if result else closed_msg}\" \
                            -H 'Title: ResiSTORE Status @ {pst_time}' \
                            -H 'Tags: {tag}' \
                            ntfy.sh/resistore
                    """
        os.system(curl_cmd)
    prev_result = result
    sleep(30)
    
