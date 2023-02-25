import datetime, random, requests, time
import concurrent.futures

HOST = 'http://127.0.0.1:500'
API_PATH = '/query?user=mingy'
ENDPOINT = HOST + API_PATH
MAX_THREADS = 5005
CONCURRENT_THREADS = 5000

def send_api_request():
    url = HOST+str(random.randrange(0, 10))+API_PATH
    r = requests.get(url)

start_time = datetime.datetime.now()
print ('Starting:', start_time)

with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
    futures = [ executor.submit(send_api_request) for x in range (CONCURRENT_THREADS) ]
end_time = datetime.datetime.now()
print ('Finished start time:', start_time, 'duration: ', end_time-start_time)