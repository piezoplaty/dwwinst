import json
import datetime
import time
import dateutil.parser
import sys


originalJson = list()

SAMPLE_JSON_FILE = '/Users/nated/projects/dwwinst/tailOfN2k'
with open(SAMPLE_JSON_FILE, 'rU') as n2kFile:
    for line in n2kFile:
        originalJson.append(json.loads(line)) 

counter = 0
while True:
    #if we reach the end of the file, start over
    if counter == len(originalJson):
        counter = 0
    currentLine = originalJson[counter]
    currentLineTimestamp = dateutil.parser.parse(currentLine["timestamp"])
    currentLine["timestamp"] = datetime.datetime.now().replace(second=currentLineTimestamp.second).isoformat()
    print json.dumps(currentLine)
    sys.stdout.flush()
    counter += 1
    time.sleep(.025)



