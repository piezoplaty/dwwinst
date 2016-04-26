import json
import datetime
import time
import dateutil.parser
import sys


originalJson = list()

SAMPLE_JSON_FILE = '/Users/nated/projects/dwwinst/2016-04-21T02-BoatTelemTest'
with open(SAMPLE_JSON_FILE, 'rU') as n2kFile:
    for line in n2kFile:
        originalJson.append(json.loads(line)) 

counter = 0
while True:
    #if we reach the end of the file, start over
    if counter == len(originalJson):
        counter = 0
    currentLine = originalJson[counter]
    counter += 1
    currentLineTimestamp = dateutil.parser.parse(currentLine["timestamp"])
    currentLine["timestamp"] = datetime.datetime.now().isoformat()
    print json.dumps(currentLine)
    sys.stdout.flush()

    time.sleep(.025)



