import json
import requests
import random
import time
import ssl
import urllib.request

my_account = 'BellaZio'
url = 'https://pansophy.app:8443'

#get a list of accounts that have an amount of money above a certain threshold
def get_list_account_above_threshold(response, threshold = 1000, my_account = 'BellaZio'):
    parsed_list  = []
    
    jsonResponse = json.loads(response.decode('utf-8'))
    account_list = list(jsonResponse['accounts'].keys())
    account_data = jsonResponse['accounts']
    
    for account in account_list:
        if account == my_account:
            continue
        else:
            if account_data.get(account) > threshold:
                parsed_list.append(account)
            else:
                continue
            
    return parsed_list

#create a merit body for requesting a transaction
def create_merit_json_input_data(account, money = 1000, my_account = 'BellaZio'):
    return json.dumps({
     "operation": "merit",
     "team": my_account,
     "coin": money,
     "stealfrom": account
    })

#create a body to claim the transaction
def create_claim_json(my_account = 'BellaZio'):
    return json.dumps({
     "operation": "claim",
     "team": my_account,
    })

my_account = 'BellaZio'
index = 0

while(True):
    print("Number of transactions made:", index)
    #make a get request to see the status of the chain
    response = requests.get(url, verify=False).content
    
    #get accounts whose amount of money is above a certain threshold
    list_accounts_to_steal_from = get_list_account_above_threshold(response, threshold = 1000)
    
    #draw one to take money from and compose the body
    target = random.choice(list_accounts_to_steal_from)
    merit_body = create_merit_json_input_data(target, 1000)
    
    #make the merit request and wait 10 seconds as the proof of work
    # Post Method is invoked if data != None
    req = urllib.request.Request(url, data = bytes(merit_body.encode("utf-8")), method = "POST")
    # Add the appropriate header.
    req.add_header("Content-type", "application/json; charset=UTF-8")
    with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as resp:
        response_data = json.loads(resp.read().decode("utf-8"))
        if response_data.get('msg') != 'accepted':
            print("Request failed", response_data)
            break
    time.sleep(10)

    
    #make the claim request
    claim_body = create_claim_json()
    req = urllib.request.Request(url, data = bytes(claim_body.encode("utf-8")), method = "POST")
    # Add the appropriate header.
    req.add_header("Content-type", "application/json; charset=UTF-8")
    with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as resp:
        response_data = json.loads(resp.read().decode("utf-8"))
        if response_data.get('msg') != 'request claimed':
            print("Request failed", response_data)
            break
    index += 1 