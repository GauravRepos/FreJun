import requests
port = 8000
def inbound_sms_param_misssing(port):
    url = "http://127.0.0.1:{}/API/inbound/sms/".format(port)
    body = {"username" : "azr1",
"auth_id": "20S0KPNOIM",
"to" : "4924195509192",
"text": "STOP/n"}
    r = requests.post(url,json = body)
    content = r.content
    return content
def inbound_sms_param_invalid(port):
    url = "http://127.0.0.1:{}/API/inbound/sms/".format(port)
    body = {"username" : "azr1",
    "auth_id": "20S0KPNOIM",
    "from" : "44415415641544145545415",
    "to" : "4924195509192",
    "text": "STOP/n"}
    r = requests.post(url,json = body)
    content = r.content
    return content

def inbound_to_not_found(port):
    url = "http://127.0.0.1:{}/API/inbound/sms/".format(port)
    body = {"username" : "azr1",
    "auth_id": "20S0KPNOIM",
    "from" : "4441541564154",
    "to" : "12345678",
    "text": "STOP/n"}
    r = requests.post(url,json = body)
    content = r.content
    return content

def inbound_valid(port):
    url = "http://127.0.0.1:{}/API/inbound/sms/".format(port)
    body = {"username" : "azr1",
    "auth_id": "20S0KPNOIM",
    "from" : "61871112946",
    "to" : "4924195509194",
    "text": "STOP/n"}
    r = requests.post(url,json = body)
    content = r.content
    return content







def outbound_sms_param_misssing(port):
    url = "http://127.0.0.1:{}/API/outbound/sms/".format(port)
    body = {"username" : "azr2",
"auth_id": "54P2EOKQ47",
"to" : "4924195509049",
"text": "SOME NEW TEXT SENT"}
    r = requests.post(url,json = body)
    content = r.content
    return content




def outbound_sms_param_invalid(port):
    url = "http://127.0.0.1:{}/API/outbound/sms/".format(port)
    body = {"username" : "azr2",
    "from" : "1234",
"auth_id": "54P2EOKQ47",
"to" : "4924195509049",
"text": "SOME NEW TEXT SENT"}
    r = requests.post(url,json = body)
    content = r.content
    return content


def outbound_to_from_match(port):
    url = "http://127.0.0.1:{}/API/outbound/sms/".format(port)
    body = {"username" : "azr2",
    "from" : "441887480051",
"auth_id": "54P2EOKQ47",
"to" : "4924195509194",
"text": "SOME NEW TEXT SENT"}
    r = requests.post(url,json = body)
    content = r.content
    return content


def outbound_from_not_found(port):
    url = "http://127.0.0.1:{}/API/outbound/sms/".format(port)
    body = {"username" : "azr2",
    "from" : "441235330075",
"auth_id": "54P2EOKQ47",
"to" : "4924195509194",
"text": "SOME NEW TEXT SENT"}
    r = requests.post(url,json = body)
    content = r.content
    return content


def outbound_valid(port):
    url = "http://127.0.0.1:{}/API/outbound/sms/".format(port)
    body = {"username" : "azr2",
    "from" : "441224980091",
"auth_id": "54P2EOKQ47",
"to" : "4924195509194",
"text": "SOME NEW TEXT SENT"}
    r = requests.post(url,json = body)
    content = r.content
    return content










result = inbound_sms_param_misssing(port)
print("inbound_sms_param_misssing" + str(result))
result = inbound_sms_param_invalid(port)
print("inbound_sms_param_invalid" +str(result))
result = inbound_to_not_found(port)
print("inbound_to_not_found" + str(result))
result = inbound_valid(port)
print("inbound_valid" + str(result))



result = outbound_sms_param_invalid(port)
print("outbound_sms_param_invalid" + str(result))
result = outbound_to_from_match(port)
print("outbound_to_from_match" + str(result))
result = outbound_sms_param_misssing(port)
print("outbound_sms_param_misssing" + str(result))
result = outbound_from_not_found(port)
print("outbound_from_not_found" + str(result))

result = outbound_valid(port)
print("outbound_valid" + str(result))

