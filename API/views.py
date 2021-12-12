from django.contrib import auth
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from API.models import Account, PhoneNumber
from rest_framework.response import Response
from API import validators
import json, datetime
import redis

r = redis.Redis(host='localhost', port=6379, db=0,
                charset="utf-8", decode_responses=True)
EXPIRE_TIME = 24*60*60

class InboundSMS(APIView):
    def post(self, request):
        res = {}
        message = ""
        try:
            try:
                req = json.loads(request.body.decode("utf-8"))

            except Exception as e:
                res["details"] = "Invalid request body"
                res["status"] = status.HTTP_405_METHOD_NOT_ALLOWED
                return Response({"message": message, "error": res})
            username = req['username']
            auth_id = req["auth_id"]
            p = Account.objects.filter(username=username).first()
            try:
                result = p.to_Dict()
            except:
                res["errors"] = "Authentication Failed"
                res["status"] = status.HTTP_403_FORBIDDEN
                return Response({"message": "", "error": res})
            result = p.to_Dict()
            if auth_id == result["auth_id"]:
                validation = validators.validate_api(req)
                if not validation["success"]:
                    res["errors"] = validation["errors"]
                else:
                    retreived_id = result["id"]
                    phone_details = PhoneNumber.objects.filter(
                        account=retreived_id)
                    phone_result = [x.to_Dict() for x in phone_details]
                    for dictionary in phone_result:
                        if dictionary["number"] == str(req["to"]):
                            message = "inbound sms ok"
                            res = ""
                            text = req["text"]
                            if text == "STOP" or text == "STOP/n" or text == "STOP/r/n":
                                final_dict = {"from": str(
                                    req["from"]), "to": str(req["to"])}
                                if cache(final_dict, 14400):
                                    print("REDIS CACHED")
                                else:
                                    print("Error caching")
                            else:
                                print("INVALID TEXT FOR CACHING")
                            break      
                        else:
                            res = "to parameter not found"
            else:
                res["errors"] = "Authentication Failed"
                res["status"] = status.HTTP_403_FORBIDDEN
            return Response({"message": message, "error": res})
        except:
            return Response({"message" : "", "error" : "unknown failure"})

class OutboundSMS(APIView):
    def post(self, request):
        res = {"error" : ""}
        message = ""
        try:
            try:
                req = json.loads(request.body.decode("utf-8"))

            except Exception as e:
                res["details"] = "Invalid request body"
                res["status"] = status.HTTP_405_METHOD_NOT_ALLOWED
                return Response({"message": message, "error": res})
            username = req['username']
            auth_id = req["auth_id"]
            p = Account.objects.filter(username=username).first()
            try:
                result = p.to_Dict()
            except:
                res["errors"] = "Authentication Failed"
                res["status"] = status.HTTP_403_FORBIDDEN
                return Response({"message": "", "error": res})
            if auth_id == result["auth_id"]:
                validation = validators.validate_api(req)
                if not validation["success"]:
                    res["errors"] = validation["errors"]
                else:

                    if updateCount(req["from"],EXPIRE_TIME):
                        retreived_id = result["id"]
                        phone_details = PhoneNumber.objects.filter(
                            account=retreived_id)
                        phone_result = [x.to_Dict() for x in phone_details]
                        for dictionary in phone_result:
                            if dictionary["number"] == str(req["from"]):
                                message = "outbound sms ok"
                                res["error"] = ""

                                if search_cache(req):
                                    message = ""
                                    res["error"] = "sms from {} to {} blocked by STOP request".format(
                                        req["from"], req["to"])
                                    print("MATCHES FOUND")

                                else:
                                    print("NO MATCHES FOUND")
                                break

                            else:
                                res["error"] = "from parameter not found"
                                message = ""
                    else:
                        res["error"] = "limit reached for from {}".format(req["from"])
                        message = ""
            else:
                res["errors"] = "Authentication Failed"
                res["status"] = status.HTTP_403_FORBIDDEN
            return Response({"message": message, "error": res["error"]})
        except:
            return Response({"message" : "", "error" : "unknown failure"})

def search_cache(newData):
    try:
        data = json.loads(r.hgetall("dictionary")["Data"])
        print(data)

        fromData = (data["from"].split(","))

        toData = (data["to"].split(","))
        if str(newData["from"]) in fromData and str(newData["to"]) in toData:
            return True
        return False
    except Exception as e:
        print(str(e))
        return False


def cache(newData, time):
    try:
        try:
            data = json.loads(r.hgetall("dictionary")['Data'])
            print(data)
        except:
            data = {"from":"", "to":""}
        fromData = (data["from"].split(","))
        toData = (data["to"].split(","))
        fromData.append(newData["from"])
        toData.append(newData["to"])
        finalDict = {"Data": json.dumps(
            {"from": ",".join(list(fromData)), "to": ",".join(list(toData))})}
        a = r.hmset("dictionary", finalDict)

        r.expire("dictionary", time)

        return True
    except Exception as e:
        print(str(e))
        return False

def setInitial(phoneNumber,time,now):
    
    newData = {"data":""}
    r.hmset(phoneNumber,newData)
    r.expire(phoneNumber, time)
    
    r.hmset(now+phoneNumber,{"data":''})
    r.expire(now+phoneNumber,time)


def updateCount(phoneNumber,timeExpire):
    try:
        
        now = str(datetime.datetime.now())
        if len(r.hgetall(phoneNumber))==0:
            setInitial(phoneNumber, timeExpire,now)
        times = set((r.hgetall(phoneNumber)["data"]).replace(",","XXXX").split("XXXX"))
        print(times)
        if len(times)==50:
            return False
        newTimes = []
        for time in times:
            if len(r.hgetall(time+str(phoneNumber)))==0 or time=='':
                pass
            else:
            
                newTimes.append(time)
        newTimes.append(now)
        
        
        
        r.hmset(phoneNumber, {"data":",".join(newTimes)})
        r.hmset(now+phoneNumber,{"data":''})
        
        r.expire(now+phoneNumber,timeExpire)
        r.expire(phoneNumber, timeExpire)
        return True
    except Exception as e:
        print(e)
        return False

