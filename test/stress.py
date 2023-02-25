import time
import requests
import datetime
import concurrent.futures

HOST = 'http://127.0.0.1:5002'
API_PATH = '/query?user=mingy'
ENDPOINT = HOST + API_PATH
MAX_THREADS = 5005
CONCURRENT_THREADS = 5000

def send_api_request():
    r = requests.get(ENDPOINT)

start_time = datetime.datetime.now()
print ('Starting:', start_time)

with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
    futures = [ executor.submit(send_api_request) for x in range (CONCURRENT_THREADS) ]
end_time = datetime.datetime.now()
print ('Finished start time:', start_time, 'duration: ', end_time-start_time)