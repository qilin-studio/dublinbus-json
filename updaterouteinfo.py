import urllib
import json
import re
import pymongo

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
    user = ""
    password = ""
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

#define several json structures
# outer structure
#routeinfo = {'route': routeid,
#			 'info': []}
# each direction will be put into info list
#direction = {'direction': direction_name,
#             'stops': []}
# each stop wil be put into stops list
#stop = {'stopid': stopid,
#        'address': address}


result = []

# update routeinfo date
print "ROUTE LIST INFORMATION"
print "number of resutls: " + str(data["numberofresults"])
print "last updated: " + str(data["timestamp"])
for i in data["results"]:
    route = str(i["route"])
    info = []
    routeinfo = {'route': route, 'info': info}
    result.append(routeinfo)

print result[:-3]

# get rid of last three results 'GREEN', 'RED', 'XXX'
result = result[:-3]

# insert relevant data
for route in result:
    routeinfo_request = getrequest("i", route['route'])
    routeinfo_json = getjson(routeinfo_request)
    data = routeinfo_json

    for i in data["results"]:
        direction_name = "From " + str(i["origin"]) + " to " + str(i["destination"])
        stops = []
        direction = {'direction': direction_name, 'stops': stops}
        print direction
        route['info'].append(direction)

        for j in i["stops"]:
            stopid = str(j["stopid"])
            address = str(j["shortname"].encode('ascii', 'ignore') + ", " + j["fullname"].encode('ascii', 'ignore'))
            stop = {'stopid': stopid, 'address': address}
            print stop
            stops.append(stop)

print result 

#save to routeinfo.json
json.dump(result, open("routeinfo.json", "w"))

print "Finished!"

"""
routeinfo.json:
[{ 'route': '1',
   'info': [
   {
        'direction': 'From Santry via O'Connell Street to Sandymount',
        'stops': [
        {
            'stopid': '226',
            'address': 'Shanard Road, Shanard Avenue'
        },
        ...
        ]

   },
   ...
   ]   
},
...
]

"""

