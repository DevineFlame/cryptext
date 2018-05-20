import json
import requests
import threading
import time
import logging
from collections import defaultdict

 
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-9s) %(message)s',)


api_url_base="https://koinex.in/api/ticker"
headers = {'Content-Type': 'application/json'}
coin_file="coin.json"
test_file="ticker.json"
tracking_coins=""

price_track = defaultdict(list)
time_track=defaultdict(list)
fluct_max=defaultdict(list)
fluct_min=defaultdict(list)
fluct_curr=defaultdict(list)
fluct_old=defaultdict(list)

api_data={}
api_data_lock=threading.Lock()
print_coin_lock=threading.Lock()

delay=5;


delete_time=10*60






def analyze_coin(curr_coin):
    logging.debug('in the analyze_coin with coin'+curr_coin)
    global api_data
    global price_track
    global time_track
    global delete_time

    while  True :    
        if is_empty(api_data)  :
            time.sleep(delay)
        else:    
            curr_coin_data=get_data(curr_coin)
            #print(curr_coin_data)

            try:
                logging.debug('Acquired  lock on print_coin ')
                print_coin_lock.acquire()
                
                if len(price_track[curr_coin])<100:
                    price_track[curr_coin].append(curr_coin_data[curr_coin]["price"])
                    time_track[curr_coin].append(time.time())   

                else:
                    price_track[curr_coin].pop(0)
                    time_track[curr_coin].pop(0)

                t1=time_track[curr_coin][0];
                t2=time_track[curr_coin][-1];

                while (delete_time < (t2-t1)):
                    price_track[curr_coin].pop(0)
                    time_track[curr_coin].pop(0)
                    t1=time_track[curr_coin][0];


                fluct_max[curr_coin]=max(price_track[curr_coin])
                fluct_min[curr_coin]=min(price_track[curr_coin])
                curr_price=curr_coin_data[curr_coin]["price"]

                verdict=get_verdict(curr_coin,fluct_max[curr_coin],fluct_min[curr_coin],curr_price)
                fluct_curr[curr_coin]=verdict
                if fluct_curr[curr_coin] != fluct_old[curr_coin]:
                    notify(fluct_curr[curr_coin])
                    fluct_old[curr_coin]=fluct_curr[curr_coin]








                print_coin(curr_coin_data,curr_coin)

            finally:
                logging.debug('Released  lock on print_coin')
                print_coin_lock.release()
        
        time.sleep(delay)


def notify(verdict):
	url = "https://onesignal.com/api/v1/notifications"
	payload = "{\n  \"app_id\": \"*****************\",\n  \"included_segments\": [\"All\"],\n  \"data\": {\"foo\": \"bar\"},\n  \"contents\": {\"en\": \""+str(verdict)+"\"}\n}"
	headers = {
	    'authorization': "Basic ********************",
	    'content-type': "application/json",
	    'cache-control': "no-cache",
	    'postman-token': "416a974f-5d1e-e900-be6c-943f0d8bd4f3"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.text)

def get_verdict(curr_coin,max_val,min_val,curr_val):
    verdict=""
    if curr_val== max_val:
        verdict=curr_coin+"::   "+str(curr_val)+"      "+str(min_val)+"  U"
    elif curr_val==min_val:            
        verdict=curr_coin+"::   "+str(curr_val)+"      "+str(max_val)+"  D"
    else:
        verdict=curr_coin+"::   "+str(min_val)+"--> "+str(curr_val)+" <--"+str(max_val)+"  B"
    return verdict




def track_coins():
    coins=""
    if coin_file:
        with open(coin_file, 'r') as f:
            coins = json.load(f)
    tracking_coins=coins["coins"]
    return tracking_coins







#get data from api every 5 seconds
def get_data_from_api():
    api_url=api_url_base
    response = requests.get(api_url, headers=headers)
    global api_data

    while True:
        curr_api_data=""
        if response.status_code == 200:
            curr_api_data=json.loads(response.content.decode('utf-8'))
            print("success")
        else:
            curr_api_data=""
        #if data get is success
        if curr_api_data:    
            logging.debug('Waiting for a lock on api_data')
            api_data_lock.acquire()
            try:
                logging.debug('Acquired  lock on api_data')
                #print(curr_api_data["prices"])
                api_data=curr_api_data
                
            finally:
                logging.debug('Released  lock on api_data')
                api_data_lock.release()
        time.sleep(delay)

#format data
def get_data(curr_coin):
    global api_data
    logging.debug("getting data of  coin "+curr_coin)
   
    coin_data={}
    curr_data=""
    try:
        logging.debug('Acquired  lock on api_data ')
        api_data_lock.acquire()        
        curr_data=api_data
        #print(api_data)

    finally:
        logging.debug('Released  lock on api_data')
        api_data_lock.release()
    if curr_data:
        prices=curr_data["prices"]["inr"]
        stats=curr_data["stats"]["inr"]
        
        coin_data[curr_coin]=stats[curr_coin]
        coin_data[curr_coin]["price"]=prices[curr_coin]
    else:
        coin_data[curr_coin]=""
        coin_data[curr_coin]["price"]=0


    return coin_data   
    #print(type(coin_data))
    # return api_data
    

    
    
def is_empty(any_structure):
    if any_structure:        
        return False
    else:       
        return True



def print_coin(curr_coin_data,coin):
     name=   curr_coin_data[coin]["currency_full_form"]
     low_ask=curr_coin_data[coin]["lowest_ask"]
     last_price=curr_coin_data[coin]["price"]
     highest_bid=curr_coin_data[coin]["highest_bid"]
     change_24=curr_coin_data[coin]["per_change"]

     fluctuation=0;
     print("=="*20)
     print(coin+":"+name+"--")
     print("Ask: "+low_ask+"     Last Price:"+last_price+"   Bid: "+highest_bid+" ")
     
     print('24 hrs change :{:0.2f}          fluctuation:{}% '.format(float(change_24), fluctuation))

     print("=="*20)




if __name__ == "__main__":
    # creating thread
    tracking_coins=track_coins()
    coin_threads={}
    
    api_thread=threading.Thread(target=get_data_from_api)
    api_thread.setDaemon(True)
    api_thread.start()
    
 
    

    for coin in tracking_coins:
        coin_threads[coin]=threading.Thread(target=analyze_coin,args=(coin,))

    for coin in tracking_coins:
        coin_threads[coin].start()

   # api_thread.join()
    for coin in tracking_coins:
        coin_threads[coin].join()
