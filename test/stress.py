import datetime, random, requests, time
import concurrent.futures

HOST = 'http://10.103.23.169:500'
API_PATH = '/query?user=mingy'
ENDPOINT = HOST + API_PATH
MAX_THREADS = 6
CONCURRENT_THREADS = 10000

def send_api_request():
    r = requests.get("http://10.103.23.169:5001/query?user=mingy")

start_time = datetime.datetime.now()
print ('Starting:', start_time)

with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
    futures = [ executor.submit(send_api_request) for x in range (CONCURRENT_THREADS) ]
end_time = datetime.datetime.now()
print ('Finished start time:', start_time, 'duration: ', end_time-start_time)