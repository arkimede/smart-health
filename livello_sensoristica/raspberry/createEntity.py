import requests, json
import ConfigParser
import io
import sys

NUM_ARG=len(sys.argv)
COMMAND=sys.argv[0] 

if NUM_ARG==6:
   ENTITY_ID=sys.argv[1]
   ENTITY_TYPE=sys.argv[2]
   ENTITY_ATTR=sys.argv[3]
   ENTITY_ATTR_TYPE=sys.argv[4]
   ENTITY_ATTR_VALUE=sys.argv[5]

else:
   print 'Usage: '+COMMAND+' [ENTITY ID] [ENTITY TYPE] [ATTRIBUTE NAME] [ATTRIBUTE TYPE] [ATTRIBUTE VALUE]'
   print
   sys.exit(2)

CONFIG_FILE = "./config.ini"

# Load the configuration file
with open(CONFIG_FILE,'r+') as f:
    sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

CB_HOST=config.get('contextbroker', 'host')
CB_PORT=config.get('contextbroker', 'port')
CB_FIWARE_SERVICE=config.get('contextbroker', 'fiware_service')
CB_AAA=config.get('contextbroker', 'OAuth')
if CB_AAA == "yes":
   TOKEN=config.get('user', 'token')
   TOKEN_SHOW=TOKEN[1:5]+"**********************************************************************"+TOKEN[-5:]
else:
   TOKEN="NULL"
   TOKEN_SHOW="NULL"

CB_URL = "http://"+CB_HOST+":"+CB_PORT
#HEADERS = {'content-type': 'application/json','accept': 'application/json', 'Fiware-Service': CB_FIWARE_SERVICE ,'X-Auth-Token' : TOKEN}
HEADERS = {'content-type': 'application/json','accept': 'application/json','X-Auth-Token' : TOKEN}
HEADERS_SHOW = {'content-type': 'application/json', 'accept': 'application/json' , 'Fiware-Service': CB_FIWARE_SERVICE , 'X-Auth-Token' : TOKEN_SHOW}

PAYLOAD = '{ \
    "contextElements": [ \
        { \
            "type": "'+ENTITY_TYPE+'", \
            "isPattern": "false",  \
            "id": "'+ENTITY_ID+'", \
            "attributes": [ \
            { \
                "name": "'+ENTITY_ATTR+'",  \
                "type": "'+ENTITY_ATTR_TYPE+'", \
                "value": "'+ENTITY_ATTR_VALUE+'" \
            } \
            ] \
        } \
    ], \
    "updateAction": "APPEND" \
}'

URL = CB_URL + '/ngsi10/updateContext'

print "* Asking to "+URL
print "* Headers: "+str(HEADERS_SHOW)
print "* Sending PAYLOAD: "
print json.dumps(json.loads(PAYLOAD), indent=4)
print
print "..."
r = requests.post(URL, data=PAYLOAD, headers=HEADERS)
print
print "* Status Code: "+str(r.status_code)
print "* Response: "
print r.text
print

