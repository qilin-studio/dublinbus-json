import urllib
import json
import re
import pymongo
import pprint

# load json from request
def getjson(request):
    # get file from request
    data = urllib.urlopen(request)

    # Type: dict
    json_data = json.load(data)
    return json_data

# get requests
def getrequest(table, route):
    #Replace user and password with API key
    user = "linqi"
    password = "1710qi2014"
    request = ""
    
    if table == "i":

        #route information
        rturl = "/cgi-bin/rtpi/routeinformation?"
        host = "www.dublinked.ie"
        header = "http://"+user+":"+password+"@"
        rtquery = urllib.urlencode({'routeid': route, 'operator': 'bac', 'format': 'json'})
        #request url
        request = header + host + rturl + rtquery

    elif table == "l":

        #route list information
        rturl = "/cgi-bin/rtpi/routelistinformation?"
        host = "www.dublinked.ie"
        header = "http://"+user+":"+password+"@"
        rtquery = urllib.urlencode({'operator': 'bac', 'format': 'json'})
        #request url
        request = header + host + rturl + rtquery
    
    return request
    

# get route list
routelist_request = getrequest("l", 0)
routelist_json = getjson(routelist_request)
data = routelist_json

routelist = []
print "ROUTE LIST INFORMATION"
print "number of resutls: " + str(data["numberofresults"])
print "last updated: " + str(data["timestamp"])
for i in data["results"]:
    routelist.append(str(i["route"]))

print routelist

result = []

# get each address information and append to a list
for route in routelist:
    routeinfo_request = getrequest("i", route)
    routeinfo_json = getjson(routeinfo_request)
    data = routeinfo_json

    for i in data["results"]:
        for j in i["stops"]:
            #get each info
            stopid = int(j["stopid"])
            address = str(j["shortname"].encode('ascii', 'ignore') + ", " + j["fullname"].encode('ascii', 'ignore'))
            latitude = str(j["latitude"])
            longitude = str(j["longitude"])

            #create a basic doc structure
            stop = {'stopid': stopid, 'address': address, 'latitude': latitude, 'longitude': longitude}

            print stop

            # only add unique bus info
            is_duplicate = False
            for a in result:
                if stop['stopid'] == a['stopid']:
                    is_duplicate = True
            
            if not is_duplicate:
                result.append(stop)

print result 

#save to stopaddress.json
json.dump(result, open("stopaddress.json", "w"))

print "Finished!"


