from urllib import request, parse, error
from time import sleep
import os
import pytz
from datetime import datetime
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
def query_status() -> int:
    try: 
        response = request.urlopen("https://resi.store/lux.bool").read()
        result = int(response.decode()[0])
        return result
    except error.URLError:
        # Maybe not goood
        logging.error("lost connection")
        return 0 

pst = pytz.timezone('America/Los_Angeles')

open_msg = "The resistore has opened!"
closed_msg = "The resistore has closed..."

print("Starting loop")
prev_result = query_status()
init_status = "Open" if prev_result else "Closed"
curl_cmd = f"""curl -d \"Starting status script, current status is {init_status}\" \
                    ntfy.sh/resistore
            """
os.system(curl_cmd)
while True:
    result = query_status()
    if result != prev_result:
        pst_time = datetime.now(pst).strftime("%I:%M %p")
        tag = "green_square,grinning" if result else "red_square,frowning_face"
        curl_cmd = f"""curl -d \"{open_msg if result else closed_msg}\" \
                            -H 'Title: ResiSTORE Status @ {pst_time}' \
                            -H 'Tags: {tag}' \
                            ntfy.sh/resistore
                    """
        os.system(curl_cmd)
    prev_result = result
    sleep(30)
    
